# ============================================================
# 声明 (Declaration)
#
# 本文件改编自以下项目的 A-Bogus 实现：
#   `https://github.com/Evil0ctal/Douyin_TikTok_Download_API`
#   src/dtk/signing/native/abogus.py
#
# 该项目逆向了抖音 bdms.js (v1.0.1.19-fix.01)。
# 本文件针对 DouK-Downloader 的接口和代码结构进行了适配。
# Portions Copyright (c) Evil0ctal
# 感谢原作者 Evil0ctal 的开源贡献。
# Apache License 2.0: `https://github.com/Evil0ctal/Douyin_TikTok_Download_API/blob/main/LICENSE`
# 协议副本: licenses/Apache-2.0
# ============================================================

from random import Random
from time import time

from .sm3 import sm3_to_array

__all__ = [
    "ABogus",
    "DEFAULT_BROWSER_INFO",
]

# a_bogus 使用的两套字母表：
# s4 编码最终签名，s3 编码进入第三个摘要的 User-Agent
ALPHABETS: dict[str, str] = {
    "s3": "ckdp1h4ZKsUB80/Mfvw36XIgR25+WQAlEi7NLboqYTOPuzmFjJnryx9HVGDaStCe",
    "s4": "Dkdpgh2ZmsQB80/MfvV36XI1R45-WUAlEixNLwoqYTOPuzKFjJnry79HbGcaStCe",
}

# 哈希前附加在 query 与 body 末尾的盐值
SALT = "dhzx"

# 签名头部的两个明文字节（相当于格式魔数）
HEADER_MAGIC: tuple[int, int] = (3, 82)

# "1.0.1.19-fix.01" 解析后的版本块
SDK_VERSION: tuple[int, int, int, int] = (1, 0, 1, 0)

# 载荷密钥（单字节）。该 RC4 并非标准 RC4：S 盒降序初始化、
# 密钥调度使用乘法，用标准 RC4 穷举单字节密钥无法还原
PAYLOAD_KEY = 0xD3

# 2024-07-24T16:00:00Z，其中一个字段自此以双周为单位计数
FORTNIGHT_EPOCH_MS = 1_721_836_800_000

# 抖音网页端的固定标识，随签名与 query 一起发送，两者必须一致
PAGE_ID = 6241
AID = 6383

# fn148 用三个掩码把三个数据字节与一个噪声字节混成四个载体字节；
# 三个掩码按位或为 0xFF，因此第四个字节恰好携带前三个字节让出的比特
NOISE_MASKS: tuple[int, int, int] = (0x91, 0x42, 0x2C)
DATA_MASKS: tuple[int, int, int] = (0x6E, 0xBD, 0xD3)

# 五十个标量字段在载荷中的固定排列顺序（字节码中的原始顺序）
FIELD_ORDER: tuple[str, ...] = (
    "L34", "L44", "L56", "L61", "L73", "L29", "L70", "L45", "L35", "L49",
    "L38", "L66", "L51", "L68", "L28", "L48", "L64", "L47", "L30", "L71",
    "L26", "L55", "L31", "L69", "L59", "L40", "L62", "L63", "L27", "L72",
    "L41", "L74", "L57", "L52", "L42", "L39", "L33", "L67", "L53", "L43",
    "L65", "L46", "L36", "L24", "L60", "L32", "L79", "L80", "L84", "L85",
)  # fmt: skip

# 摘要哨兵：字段取 digest[offset:] 中第一个不等于 sentinel 的字节
CANARIES: tuple[tuple[int, int, int], ...] = ((3, 11, 12), (4, 8, 9), (5, 12, 13))


class DigestChain:
    """一条哈希链的三字节写入位置：slots 为 FIELD_ORDER 名称，
    indices 为直接写入的两个摘要下标，canary 为哨兵三元组"""

    __slots__ = ("slots", "indices", "canary")

    def __init__(
        self,
        slots: tuple[str, str, str],
        indices: tuple[int, int],
        canary: tuple[int, int, int],
    ):
        self.slots = slots
        self.indices = indices
        self.canary = canary


# 三条哈希链（query / body / user_agent）各自贡献的三个字节。
# 每个输入贡献三字节：足以绑定请求内容，又无法反推哈希原文
DIGEST_CHAINS: dict[str, DigestChain] = {
    "query": DigestChain(("L48", "L49", "L51"), (9, 18), CANARIES[0]),
    "body": DigestChain(("L52", "L53", "L55"), (10, 19), CANARIES[1]),
    "user_agent": DigestChain(("L56", "L57", "L59"), (11, 21), CANARIES[2]),
}

# 未被篡改的浏览器环境报告值（六个探针与机器人检测位集）
ENV_FLAGS = 1
DETECT_FLAGS = 14
NR_FLAGS = 0x21
NR_TAG: tuple[int, int, int, int] = (0, 0, 0, 0)

# window.onwheelx._Ax 存在且已锁定——SDK 自装的正常状态
TRIPWIRE_LOCKED = 3

# fn149 的签名次数分桶：6 表示本页签名次数少于 140 次
CALL_BUCKET = 6

# Chrome 桌面端 1080p 屏幕的几何信息（内窗|外窗|可用区|屏幕|平台）。
# 无屏幕信息时的固定默认值优于随机值：随请求变化的几何信息本身就是特征
DEFAULT_BROWSER_INFO = "1536|742|1536|864|1536|864|1536|864|MacIntel"

# 头部第二噪声字节按浏览器家族分桶取值（实测 43 份真实签名均落在 0..38）
_HEADER_NOISE_BANDS: dict[str, int] = {
    "chrome": 0,
    "firefox": 40,
    "safari": 81,
    "edge": 125,
    "huawei": 170,
    "other": 210,
}

# fn145 的绊线探测值：位 1、4、5、7 置位是健康状态
_TRIPWIRE_SET = 0xB2
_TRIPWIRE_FREE = 0x4D


def _family_of(user_agent: str) -> str:
    """fn143 依据 User-Agent 选择的家族分桶。

    顺序很重要：Edge 与华为浏览器均包含 "Chrome"，Chrome 又包含
    "Safari"，SDK 先检测特定名称再检测通用名称
    """
    ua = user_agent.lower()
    for name in ("edg", "huawei", "firefox", "chrome", "safari"):
        if name in ua:
            return {"edg": "edge"}.get(name, name)
    return "other"


def _header_noise(user_agent: str, rng: Random) -> int:
    """fn143：伪装成噪声的浏览器家族报告"""
    base = _HEADER_NOISE_BANDS.get(_family_of(user_agent), _HEADER_NOISE_BANDS["other"])
    return (base + int(rng.random() * 40)) & 0xFF


def _probe_noise(rng: Random) -> int:
    """fn144：超过 109 时强制为奇数，因此 110..240 中有一半不可达"""
    value = int(rng.random() * 240)
    return value + value % 2 + 1 if value > 109 else value


def _tripwire_noise(rng: Random) -> int:
    """fn145："绊线全部存在且已锁定"，叠加真实噪声"""
    return (int(rng.random() * 255) & _TRIPWIRE_FREE) | _TRIPWIRE_SET


def _mask_pair(
    pair: tuple[int, int],
    rng: Random,
    *,
    low: int | None = None,
    high: int | None = None,
) -> list[int]:
    """把两个字节摊到四个字节上，另一半填噪声。

    每个输出字节的一半来自载荷（掩码 0xAA/0x55 交替），一半来自噪声。
    low 与 high 允许调用方提供环境报告值；缺省时为 SDK 的普通噪声抽样
    """
    noise = int(rng.random() * 65535)
    low = noise & 0xFF if low is None else low & 0xFF
    high = (noise >> 8) & 0xFF if high is None else high & 0xFF
    return [
        (low & 0xAA) | (pair[0] & 0x55),
        (low & 0x55) | (pair[0] & 0xAA),
        (high & 0xAA) | (pair[1] & 0x55),
        (high & 0x55) | (pair[1] & 0xAA),
    ]


def _expand_noise(body: bytes, rng: Random) -> bytes:
    """三个数据字节与一个噪声字节混成四个载体字节，
    第四个字节恰好收集前三个让出的比特"""
    out = bytearray()
    for offset in range(0, len(body), 3):
        group = body[offset : offset + 3]
        if len(group) < 3:
            # SDK 的尾部分支：本实现的载荷长度恒为 3 的倍数，仅为对齐字节码保留
            out.append(group[0])
            if len(group) > 1 and group[1]:
                out.append(group[1])
            continue
        noise = int(rng.random() * 1000) & 0xFF
        out.extend(
            (noise & mask) | (byte & data)
            for mask, data, byte in zip(NOISE_MASKS, DATA_MASKS, group, strict=True)
        )
        out.append(
            (group[0] & NOISE_MASKS[0])
            | (group[1] & NOISE_MASKS[1])
            | (group[2] & NOISE_MASKS[2])
        )
    return bytes(out)


def js_bytes(text: str) -> bytes:
    """按 SDK 的 charCodeAt 规则把字符串转为字节。

    非 UTF-8：fn139 逐个读取 UTF-16 码元，低于 U+0100 输出一字节，
    高于则输出两个大端字节——汉字为两字节而 UTF-8 为三字节。
    几何信息长度受校验和覆盖，此处编码错误会使整个签名失效
    """
    out = bytearray()
    units = text.encode("utf-16-le")
    for index in range(0, len(units), 2):
        code = units[index] | (units[index + 1] << 8)
        if code & 0xFF00:
            out.append(code >> 8)
        out.append(code & 0xFF)
    return bytes(out)


def _le_bytes(value: int, count: int) -> list[int]:
    """value 的 count 个小端字节"""
    return [(value >> (8 * index)) & 0xFF for index in range(count)]


def canary(digest: list[int], offset: int, sentinel: int, fallback: int) -> int:
    """digest[offset:] 起第一个不等于 sentinel 的字节"""
    for byte in digest[offset:]:
        if byte != sentinel:
            return byte
    return fallback


def digest_of(text: str) -> list[int]:
    """SM3(SM3(text + SALT))，共 32 个整数"""
    return sm3_to_array(sm3_to_array(text + SALT))


def user_agent_digest(user_agent: str) -> list[int]:
    """第三条链：RC4 加密 User-Agent，base64 编码后做一次 SM3。

    与另两条链不同仅哈希一次；RC4 密钥由环境探针值构成，同一环境恒定
    """
    key = bytes((ENV_FLAGS // 256, ENV_FLAGS % 256, DETECT_FLAGS % 256))
    # 密码学层逐码元推进：以 charCodeAt 未掩码的值读取，后续 base64 掩码到低八位，
    # 因此密钥流每个码元推进一次；UTF-8 会让汉字推进三次，得到不同摘要
    sealed = rc4(key, bytes(byte & 0xFF for byte in js_bytes(user_agent.strip())))
    return sm3_to_array(encode_base64(sealed, "s3"))


def chain_bytes(chain: DigestChain, digest: list[int]) -> tuple[int, int, int]:
    """给定该链自身的摘要，返回该链贡献的三个字节"""
    first, second = chain.indices
    return digest[first], digest[second], canary(digest, *chain.canary)


def rc4(key: bytes, data: bytes) -> bytes:
    """SDK 的 RC4，并非标准 RC4：S 盒降序初始化，密钥调度使用乘法"""
    box = [0] * 256
    for i in range(256):
        box[255 - i] = i
    j = 0
    for i in range(256):
        j = (j * box[i] + j + key[i % len(key)]) % 256
        box[i], box[j] = box[j], box[i]

    out = bytearray(len(data))
    i = j = 0
    for index, byte in enumerate(data):
        i = (i + 1) % 256
        j = (j + box[i]) % 256
        box[i], box[j] = box[j], box[i]
        out[index] = byte ^ box[(box[i] + box[j]) % 256]
    return bytes(out)


def encode_base64(data: bytes, alphabet: str = "s4") -> str:
    """SDK 字母表上的 base64 编码，字面量 "=" 填充"""
    table = ALPHABETS[alphabet]
    out: list[str] = []
    for offset in range(0, len(data), 3):
        chunk = data[offset : offset + 3]
        block = int.from_bytes(chunk + b"\x00" * (3 - len(chunk)), "big")
        digits = [(block >> shift) & 0x3F for shift in (18, 12, 6, 0)]
        out.extend(table[digit] for digit in digits[: len(chunk) + 1])
    out.append("=" * ((4 - len(out) % 4) % 4))
    return "".join(out)


class ABogus:
    """为单一浏览器身份计算 a_bogus。

    除配置外无状态、开销极小。user_agent 必须与请求实际发送的
    User-Agent 一致，签名中的第三条摘要链会与其绑定
    """

    def __init__(
        self,
        user_agent: str,
        *,
        browser_info: str = DEFAULT_BROWSER_INFO,
        page_id: int = PAGE_ID,
        aid: int = AID,
        rng: Random | None = None,
    ) -> None:
        self.user_agent = user_agent
        self.browser_info = browser_info
        self.page_id = page_id
        self.aid = aid
        self._rng = rng or Random()

    def _fields(self, query: str, body: str, now_ms: int) -> dict[str, int]:
        """五十个标量字段，名称与离线解码器打印的一致"""
        digests = {
            "query": digest_of(query),
            "body": digest_of(body),
            "user_agent": user_agent_digest(self.user_agent),
        }

        # ink = Date.now() - 1：SDK 提前一次调用种在原型上的存活检查，
        # ink 不比时钟慢一毫秒的载荷不是完整入口点的产物
        ink = now_ms - 1
        fortnights = (now_ms - FORTNIGHT_EPOCH_MS) // (1000 * 60 * 60 * 24 * 14)
        info_bytes = js_bytes(self.browser_info)
        tail_bytes = js_bytes(f"{(now_ms + 3) & 0xFF},")

        fields: dict[str, int] = {
            "L24": 41,
            "L26": fortnights,
            "L27": CALL_BUCKET,
            # SDK 初始化至今的毫秒数加三：常量 3 表示入口点被即时到达
            "L28": 3,
            "L35": ENV_FLAGS & 0xFF,
            "L36": (ENV_FLAGS // 256) & 0xFF,
            "L38": NR_FLAGS & 0xFF,
            "L39": (NR_FLAGS >> 8) & 0xFF,
            "L66": TRIPWIRE_LOCKED,
            "L79": len(info_bytes) & 0xFF,
            "L80": (len(info_bytes) >> 8) & 0xFF,
            "L84": len(tail_bytes) & 0xFF,
            "L85": (len(tail_bytes) >> 8) & 0xFF,
        }
        for index, byte in enumerate(_le_bytes(now_ms, 6)):
            fields[f"L{29 + index}"] = byte
        for index, byte in enumerate(_le_bytes(DETECT_FLAGS, 4)):
            fields[f"L{44 + index}"] = byte
        for index, byte in enumerate(NR_TAG):
            fields[f"L{40 + index}"] = byte
        for index, byte in enumerate(_le_bytes(ink, 6)):
            fields[f"L{60 + index}"] = byte
        for index, byte in enumerate(_le_bytes(self.page_id, 4)):
            fields[f"L{67 + index}"] = byte
        for index, byte in enumerate(_le_bytes(self.aid, 4)):
            fields[f"L{71 + index}"] = byte
        # 三条哈希链的字节经统一表格写入，避免与解码端漂移
        for name, chain in DIGEST_CHAINS.items():
            written = chain_bytes(chain, digests[name])
            for slot, value in zip(chain.slots, written, strict=True):
                fields[slot] = value
        return fields

    def get_value(
        self,
        query: str,
        *,
        body: str = "",
        content_type: str = "",
        now_ms: int | None = None,
    ) -> str:
        """计算一次请求的 a_bogus 值。

        Args:
            query: 即将发送的 query 字符串，不含 a_bogus 本身。
            body: POST 请求体字符串，GET 留空；body 参与哈希，
                签名时为空而实际发送非空即错误签名。
            content_type: 仅为一条规则存在：请求为 multipart/form-data
                时 SDK 在哈希前置空 body（彼时 body 是 FormData 而非字符串）。
            now_ms: 毫秒时钟，测试时可固定。

        Returns:
            a_bogus 字符串（未做 URL 百分号编码）。

        Note:
            本代算法不对 HTTP 方法做哈希，仅哈希 query 与 body。
        """
        if "multipart/form-data" in content_type.lower():
            body = ""
        now = now_ms if now_ms is not None else int(time() * 1000)
        if now < FORTNIGHT_EPOCH_MS:
            # 一个字段自 2024-07-24 起以双周计数且无法表示负数；
            # 时钟早于纪元说明调用方传了秒而不是毫秒
            raise ValueError(f"clock is before the a_bogus epoch: {now}")
        fields = self._fields(query, body, now)

        # 四个噪声字节中有三个是环境报告而非噪声，仅版本块低字节为自由抽样
        version = _mask_pair(SDK_VERSION[:2], self._rng) + _mask_pair(
            SDK_VERSION[2:],
            self._rng,
            low=_probe_noise(self._rng),
            high=_tripwire_noise(self._rng),
        )

        # 校验和只覆盖版本块与五十个标量
        checksum = 0
        for byte in version:
            checksum ^= byte
        for name in FIELD_ORDER:
            checksum ^= fields[name]

        body_bytes = bytes(fields[name] for name in FIELD_ORDER)
        body_bytes += js_bytes(self.browser_info)
        body_bytes += js_bytes(f"{(now + 3) & 0xFF},")
        body_bytes += bytes((checksum,))

        header = bytes(
            _mask_pair(
                HEADER_MAGIC, self._rng, high=_header_noise(self.user_agent, self._rng)
            )
        )
        frame = _expand_noise(body_bytes, self._rng)
        sealed = rc4(bytes((PAYLOAD_KEY,)), bytes(version) + frame)
        return encode_base64(header + sealed, "s4")
