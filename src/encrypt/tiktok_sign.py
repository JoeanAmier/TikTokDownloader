# ============================================================
# 声明 (Declaration)
#
# 本文件改编自以下项目的 TikTok 签名实现：
#   `https://github.com/Evil0ctal/Douyin_TikTok_Download_API`
#   src/dtk/signing/native/tiktok_sign.py
#
# 该项目逆向了 TikTok 网页端 webmssdk (2.0.0.561, 即 acrawler)。
# 本文件针对 DouK-Downloader 的接口和代码结构进行了适配。
# Portions Copyright (c) Evil0ctal
# 感谢原作者 Evil0ctal 的开源贡献。
# Apache License 2.0: `https://github.com/Evil0ctal/Douyin_TikTok_Download_API/blob/main/LICENSE`
# 协议副本: licenses/Apache-2.0
# ============================================================

from base64 import b64encode
from collections.abc import Iterable
from hashlib import md5
from random import Random
from time import time
from typing import Final

__all__ = [
    "encode_query",
    "sign",
]

MASK32: Final = 0xFFFFFFFF

# 签名参数，顺序由 SDK 决定：
#   <业务 query>&X-Dynosaur=<环境报告>&msToken=<会话>&X-Bogus=1&X-Gnarly=<请求封条>
# X-Gnarly 封印的 query 包含 X-Dynosaur 与 msToken，签发后调序即失效
DYNOSAUR_PARAM: Final = "X-Dynosaur"
MS_TOKEN_PARAM: Final = "msToken"
BOGUS_PARAM: Final = "X-Bogus"
GNARLY_PARAM: Final = "X-Gnarly"

# HTTP 请求上 X-Bogus 为字面量 "1"；16 位 X-Bogus 只出现在
# websocket 握手（frontierSign），HTTP 上发送计算值反而是页面
# 从不发送的参数组合
BOGUS_VALUE: Final = "1"

# 自定义 base64 字母表（相对标准表的位置置换），SDK 字符串表原文
ALPHABET: Final = "u09tbS3UvgDEe6r-ZVMXzLpsAohTn7mdINQlW412GqBjfYiyk8JORCF5/xKHwacP"
_STANDARD: Final = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
_TO_CUSTOM: Final = str.maketrans(_STANDARD, ALPHABET)

# 信封首字节
ENVELOPE_TAG: Final = 0x4B

# ChaCha 状态字 0..3，非教科书 "expand 32-byte k"，来自 SDK 原文
CHACHA_INIT: Final = (1196819126, 600974999, 3863347763, 1451689750)

# FNV-1a 32 位变体：非标准偏移基数，每字节额外乘 33
FNV_OFFSET: Final = 2166136260
FNV_PRIME: Final = 16777619

# 载荷携带的版本号（bundle 2.0.0.561）。这是数据而非装饰：
# 2.0.0.514 携带 "5.3.1"/"2.0.0.514" 与不同字段集
SDK_VERSION: Final = "5.3.2"
SCM_VERSION: Final = "2.0.0.561"

# 载荷上报的环境指纹，取自真实浏览器。这是整个载荷中服务端会校验的
# 仅有的两个值，出错即静默失败：除 /api/post/item_list/ 外的接口
# 仍正常应答，item_list 返回 200 与空 body 及 tt_orcas_res: 1
ENV_CODE: Final = 65
UB_CODE: Final = 8

# X-Dynosaur 字段 0x38，跨 bundle 与环境扰动恒定，是 SDK 内部
# md5 的 hash_state；钉住实测值即安全
VM_STATE_HASH: Final = 0xC46CE353

# Canvas 指纹：-1 表示"无 canvas"，无 2d 上下文的页面即上报此值，
# 是载荷中最明显的机器人特征
CANVAS_HASH: Final = "-1"

# Node 桩环境无法产生、按 "0" 钉住的三个环境字段
WEBGL_HASH: Final = "0"
COMPONENT_VERSION: Final = "0"
DEVICE_HASH: Final = "0"

# SDK 认为自身所在页面的 location.host + location.pathname
PAGE: Final = "www.tiktok.com/"

# SDK 从 1 开始计自己的签名次数并写入四个字段，新页面首次签名为 1
CALL_SEQUENCE_START: Final = 1

# 两个字节数组编码器 (xor_base, add_base, pre_xor, rot, post_add)：
# A 编码除校验和外的所有字段；B 编码校验和与三个标志位
ENCODER_A: Final = (103, 1, None, 2, 1)
ENCODER_B: Final = (102, 0, 165, 1, 0)

# TikTok's browser serializer is not application/x-www-form-urlencoded:
# spaces become ``%20`` (not ``+``), while parentheses, slashes and colons
# remain literal. Keep this canonical encoder next to the signer so callers
# hash and send exactly the same bytes.
_MUST_ESCAPE: Final = {
    " ": "%20",
    '"': "%22",
    "<": "%3C",
    ">": "%3E",
    "`": "%60",
    "#": "%23",
}


def encode_query(pairs: Iterable[tuple[str, str]]) -> str:
    """Serialize query pairs exactly as TikTok Web's browser path does."""

    return "&".join(f"{_escape(key)}={_escape(value)}" for key, value in pairs)


def _escape(text: str) -> str:
    """Percent-escape only characters the browser must escape."""

    out: list[str] = []
    for char in text:
        if char in _MUST_ESCAPE:
            out.append(_MUST_ESCAPE[char])
        elif " " < char <= "~":
            out.append(char)
        else:
            out.extend(f"%{byte:02X}" for byte in char.encode("utf-8"))
    return "".join(out)


# 每个信封内嵌的密钥字数
KEY_WORDS: Final = 12


def hash_state(text: str) -> int:
    """SDK 的 FNV-1a 变体：常规轮之后乘 33"""
    value = FNV_OFFSET
    for byte in text.encode("utf-8"):
        step = ((value ^ byte) * FNV_PRIME) & MASK32
        value = (step + ((step * 32) & MASK32)) & MASK32
    return value


def encode_field(text: str, config: tuple[int, int, int | None, int, int]) -> bytes:
    """单个载荷字段：按位置的字节扰乱，填充后带长度标签。

    输出至少 6 字节，以 0x00 与原始长度结尾，以 (221 + index) 填充。
    单字符字段第 1 字节恒为填充常量，这使 X-Dynosaur 的校验和保持稳定
    """
    xor_base, add_base, pre_xor, rotate, post_add = config
    size = max(len(text) + 2, 6)
    out = bytearray(size)
    for index, char in enumerate(text):
        value = (ord(char) ^ (xor_base + index)) & MASK32
        value = (value + add_base + (170 & index)) % 256
        if pre_xor is not None:
            value ^= pre_xor
        value = ((value << rotate) | (value >> (8 - rotate))) & 0xFF
        out[index] = ((value ^ 187) + post_add) % 256
    for index in range(len(text), size - 2):
        out[index] = (221 + index) & 0xFF
    out[size - 2] = 0
    out[size - 1] = len(text)
    return bytes(out)


def pack_payload(
    fields: dict[int, bytes],
    order: list[int] | None = None,
    *,
    lead_count: bool = False,
) -> bytes:
    """字段铺成平台解析的 TLV 条目（key、0x00、length、value...）"""
    keys = sorted(fields) if order is None else list(order)
    body = b"".join(bytes((key, 0, len(fields[key]))) + fields[key] for key in keys)
    return bytes((len(keys),)) + body if lead_count else body


def _be(value: int, size: int) -> bytes:
    return int(value).to_bytes(size, "big")


def mix_state(timestamp: int, nonce: int, env_code: int) -> int:
    """把两个 32 位值折叠进 16 位，并在高位盖上环境标记"""
    folded = ((timestamp >> 16) ^ (nonce >> 16) ^ timestamp ^ nonce) & 0xFFFF
    return folded | (env_code << 16)


def fold_checksum(values: list[int | str], mode: int) -> int:
    """X-Gnarly 字段值的 XOR 折叠，种子为全 1。

    mode 1 把字符串记为 0，mode 2 取其前四个 UTF-8 字节大端值
    """
    accumulator = MASK32
    for value in values:
        if isinstance(value, str):
            number = (
                0 if mode == 1 else int.from_bytes(value.encode("utf-8")[:4], "big")
            )
        else:
            number = value
        accumulator ^= number & MASK32
    return accumulator & MASK32


def _quarter_round(state: list[int], a: int, b: int, c: int, d: int) -> None:
    state[a] = (state[a] + state[b]) & MASK32
    state[d] ^= state[a]
    state[d] = ((state[d] << 16) | (state[d] >> 16)) & MASK32
    state[c] = (state[c] + state[d]) & MASK32
    state[b] ^= state[c]
    state[b] = ((state[b] << 12) | (state[b] >> 20)) & MASK32
    state[a] = (state[a] + state[b]) & MASK32
    state[d] ^= state[a]
    state[d] = ((state[d] << 8) | (state[d] >> 24)) & MASK32
    state[c] = (state[c] + state[d]) & MASK32
    state[b] ^= state[c]
    state[b] = ((state[b] << 7) | (state[b] >> 25)) & MASK32


def _keystream(state: list[int], rounds: int) -> list[int]:
    """一个 64 字节块。这不是 ChaCha20，差异是关键。

    rounds 计单轮次数且随数据变化（5..20），奇数轮在列轮后退出；
    对角轮第三四元组是 (2, 7, 12, 13)（12 出现两次），系原实现
    缺陷，刻意复现
    """
    working = list(state)
    done = 0
    while done < rounds:
        _quarter_round(working, 0, 4, 8, 12)
        _quarter_round(working, 1, 5, 9, 13)
        _quarter_round(working, 2, 6, 10, 14)
        _quarter_round(working, 3, 7, 11, 15)
        done += 1
        if done >= rounds:
            break
        _quarter_round(working, 0, 5, 10, 15)
        _quarter_round(working, 1, 6, 11, 12)
        _quarter_round(working, 2, 7, 12, 13)
        _quarter_round(working, 3, 4, 13, 14)
        done += 1
    return [(working[i] + state[i]) & MASK32 for i in range(16)]


def _crypt(key: list[int] | tuple[int, ...], rounds: int, payload: bytes) -> bytes:
    """把载荷按小端 uint32 字读入，与密钥流异或。

    计数器在状态字 12，仅在完整 16 字块后递增，尾部不足块使用
    递增后的状态
    """
    state = [*CHACHA_INIT, *(word & MASK32 for word in key)]
    length = len(payload)
    word_count = (length + 3) // 4
    words = [
        int.from_bytes(payload[4 * i : 4 * i + 4].ljust(4, b"\0"), "little")
        for i in range(word_count)
    ]
    offset = 0
    while offset + 16 < word_count:
        block = _keystream(state, rounds)
        state[12] = (state[12] + 1) & MASK32
        for i in range(16):
            words[offset + i] ^= block[i]
        offset += 16
    block = _keystream(state, rounds)
    for i in range(word_count - offset):
        words[offset + i] ^= block[i]
    return b"".join(word.to_bytes(4, "little") for word in words)[:length]


def seal(payload: bytes, key: list[int] | tuple[int, ...]) -> str:
    """加密、把密钥拼回密文、编码。

    拼接位置为 (密钥字节和 + 密文字节和) % (密文长度 + 1)，
    服务端据此回收密钥
    """
    rounds = (sum(word & 0xF for word in key) & 0xF) + 5
    ciphertext = _crypt(key, rounds, payload)
    key_bytes = b"".join(int(word).to_bytes(4, "little") for word in key)
    position = (sum(key_bytes) + sum(ciphertext)) % (len(ciphertext) + 1)
    spliced = ciphertext[:position] + key_bytes + ciphertext[position:]
    raw = bytes((ENVELOPE_TAG,)) + spliced
    return b64encode(raw).decode("ascii").translate(_TO_CUSTOM)


def _random_key(rng: Random) -> tuple[int, ...]:
    return tuple(rng.getrandbits(32) for _ in range(KEY_WORDS))


def _clock_nonce() -> int:
    """取自微秒时钟的 32 位值，与 SDK 的取法一致"""
    return int(time() * 1_000_000) & MASK32


def dynosaur_payload(
    query: str,
    user_agent: str,
    *,
    timestamp: int,
    nonce: int,
    sequence: int = CALL_SEQUENCE_START,
    env_code: int = ENV_CODE,
    ub_code: int = UB_CODE,
) -> bytes:
    """环境报告：25 个 TLV 字段，键 0x20..0x38 升序。

    只有三个字段把报告与请求绑定（均为 hash_state）：0x2B 对空字符串
    （GET 无 body）、0x2E 对 query（仅 query，不含路径）、0x30 对
    User-Agent——签名必须用与请求相同的 UA 计算
    """
    fields: dict[int, bytes] = {
        0x21: encode_field("1", ENCODER_B),
        0x22: encode_field("1", ENCODER_B),
        0x23: encode_field("0", ENCODER_A),
        0x24: encode_field(str(mix_state(timestamp, nonce, env_code)), ENCODER_A),
        0x25: encode_field(str(sequence), ENCODER_A),
        0x26: encode_field(str(env_code), ENCODER_A),
        0x27: encode_field(str(timestamp), ENCODER_A),
        0x28: encode_field(WEBGL_HASH, ENCODER_A),
        0x29: encode_field("0", ENCODER_A),
        0x2A: encode_field(SDK_VERSION, ENCODER_A),
        0x2B: _be(hash_state(""), 4),
        0x2C: encode_field(CANVAS_HASH, ENCODER_A),
        0x2D: encode_field("0", ENCODER_A),
        0x2E: _be(hash_state(query), 4),
        0x2F: encode_field(str(sequence), ENCODER_A),
        0x30: _be(hash_state(user_agent), 4),
        0x31: encode_field(SCM_VERSION, ENCODER_A),
        0x32: encode_field(COMPONENT_VERSION, ENCODER_A),
        0x33: encode_field(DEVICE_HASH, ENCODER_A),
        0x34: encode_field(str(nonce), ENCODER_A),
        0x35: encode_field(PAGE, ENCODER_A),
        0x36: encode_field(str(ub_code), ENCODER_A),
        0x37: encode_field("0", ENCODER_A),
        0x38: _be(VM_STATE_HASH, 4),
        # 占位：下方校验和会覆盖全部字段重新写入 0x20
        0x20: encode_field("0", ENCODER_A),
    }
    checksum = 0
    for key in sorted(fields):
        checksum ^= fields[key][1]
    fields[0x20] = encode_field(str(checksum), ENCODER_B)
    return pack_payload(fields)


def gnarly_fields(
    signed_query: str,
    user_agent: str,
    *,
    body: bytes = b"",
    timestamp: int,
    nonce: int,
    nonce2: int,
    sequence: int = CALL_SEQUENCE_START,
    env_code: int = ENV_CODE,
    ub_code: int = UB_CODE,
) -> dict[int, bytes]:
    """请求封条的字段表，16 项（无 0x07）。

    signed_query 为已追加 &X-Dynosaur=...&msToken=... 的业务 query——
    token 为空时后缀也必须存在，这使该参数成为对整个改写后 URL 的
    封印。两个校验和按固定逻辑顺序折叠
    """
    query_md5 = md5(signed_query.encode("utf-8")).hexdigest()
    body_md5 = md5(body).hexdigest()
    agent_md5 = md5(user_agent.encode("utf-8")).hexdigest()
    mixed = mix_state(timestamp, nonce, env_code)
    covered: list[int | str] = [
        0,
        env_code,
        ub_code,
        query_md5,
        body_md5,
        agent_md5,
        timestamp,
        0,
        nonce,
        SDK_VERSION,
        SCM_VERSION,
        CALL_SEQUENCE_START,
        sequence,
        sequence,
        mixed,
        nonce2,
    ]
    first = fold_checksum(covered, 2)
    second = fold_checksum([*covered, first], 1)
    return {
        0x00: _be(second, 4),
        0x01: _be(env_code, 2),
        0x02: _be(ub_code, 2),
        0x03: query_md5.encode("ascii"),
        0x04: body_md5.encode("ascii"),
        0x05: agent_md5.encode("ascii"),
        0x06: _be(timestamp, 4),
        0x08: _be(nonce, 4),
        0x09: SDK_VERSION.encode("ascii"),
        0x0A: SCM_VERSION.encode("ascii"),
        0x0B: _be(CALL_SEQUENCE_START, 2),
        0x0C: _be(sequence, 2),
        0x0D: _be(sequence, 2),
        0x0E: _be(mixed, 4),
        0x0F: _be(nonce2, 4),
        0x10: _be(first, 4),
    }


def gnarly_payload(
    signed_query: str,
    user_agent: str,
    *,
    body: bytes = b"",
    timestamp: int,
    nonce: int,
    nonce2: int,
    sequence: int = CALL_SEQUENCE_START,
    order: list[int] | None = None,
    env_code: int = ENV_CODE,
    ub_code: int = UB_CODE,
) -> bytes:
    """:func:`gnarly_fields` 打包在一字节字段数之后"""
    fields = gnarly_fields(
        signed_query,
        user_agent,
        body=body,
        timestamp=timestamp,
        nonce=nonce,
        nonce2=nonce2,
        sequence=sequence,
        env_code=env_code,
        ub_code=ub_code,
    )
    return pack_payload(fields, order, lead_count=True)


def sign(
    query: str,
    user_agent: str,
    *,
    ms_token: str = "",
    body: bytes = b"",
    timestamp: int | None = None,
    nonce: int | None = None,
    nonce2: int | None = None,
    sequence: int = CALL_SEQUENCE_START,
    rng: Random | None = None,
    key: list[int] | tuple[int, ...] | None = None,
    key2: list[int] | tuple[int, ...] | None = None,
) -> tuple[str, dict[str, str]]:
    """返回 (query, parameters)：一次 TikTok Web API 请求的完整签名。

    Args:
        query: 业务 query 字符串，为最终发送的字节序（已百分号编码，
            本函数不做转义）；若其中包含 msToken 参数会被摘出并移至
            SDK 的固定位置，不会出现第二份。
        user_agent: 请求使用的 User-Agent，必须与实际发送的一致。
        ms_token: 会话令牌，按原样封入（含空值），绝不伪造——
            TikTok 校验存在时的值、接受其缺席，伪造反而使请求失败。
        body: POST 请求体字节，GET 留空。
        timestamp / nonce / nonce2 / sequence / rng / key / key2: 测试
            注入点，缺省取当前时钟与随机值。

    Returns:
        (signed_query, parameters)：signed_query 为待发送的完整 query
        字符串，哈希字节与发送字节一致，重新编码会破坏封印；
        parameters 为四个签名参数的原始值。
    """
    source = rng or Random()
    stamp = int(time()) if timestamp is None else int(timestamp)
    first_nonce = _clock_nonce() if nonce is None else int(nonce)
    second_nonce = (~_clock_nonce()) & MASK32 if nonce2 is None else int(nonce2)

    # 从 query 字符串摘出 msToken（仅拆分，不解码，字节序不变）
    parts: list[str] = []
    embedded_token = ""
    for part in query.split("&"):
        if not part:
            continue
        name, _, value = part.partition("=")
        if name == MS_TOKEN_PARAM:
            embedded_token = value
            continue
        parts.append(part)
    # A token already present in the query is authoritative. This keeps the
    # bytes signed in sync with a caller that intentionally pins a token.
    token = embedded_token or ms_token
    query = "&".join(parts)

    dynosaur = seal(
        dynosaur_payload(
            query, user_agent, timestamp=stamp, nonce=first_nonce, sequence=sequence
        ),
        key if key is not None else _random_key(source),
    )
    # 封印覆盖追加了 X-Dynosaur 与 msToken 之后的 query，因此二者必须
    # 在 X-Gnarly 计算前拼接；夹在中间的 X-Bogus 不在封印范围内，
    # 这一不对称是平台自身的行为
    sealed_query = f"{query}&{DYNOSAUR_PARAM}={dynosaur}&{MS_TOKEN_PARAM}={token}"
    gnarly = seal(
        gnarly_payload(
            sealed_query,
            user_agent,
            body=body,
            timestamp=stamp,
            nonce=first_nonce,
            nonce2=second_nonce,
            sequence=sequence,
        ),
        key2 if key2 is not None else _random_key(source),
    )
    parameters = {
        DYNOSAUR_PARAM: dynosaur,
        MS_TOKEN_PARAM: token,
        BOGUS_PARAM: BOGUS_VALUE,
        GNARLY_PARAM: gnarly,
    }
    # 原样拼接而非百分号编码：字母表含 "/"，填充为 "="，TikTok 页面
    # 对二者同样不做转义
    signed = f"{sealed_query}&{BOGUS_PARAM}={BOGUS_VALUE}&{GNARLY_PARAM}={gnarly}"
    return signed, parameters
