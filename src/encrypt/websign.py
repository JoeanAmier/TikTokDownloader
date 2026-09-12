# ============================================================
# 声明 (Declaration)
#
# 本文件改编自以下项目的 WebSign 实现：
#   `https://github.com/Evil0ctal/Douyin_TikTok_Download_API`
#   src/dtk/signing/native/websign.py
#
# 该项目逆向了抖音 secsdk（runtime_bundler_34.js, @byted/secsdk-strategy
# v1.0.40, project-id="34"）的 webSignUrl。
# 本文件针对 DouK-Downloader 的接口和代码结构进行了适配。
# Portions Copyright (c) Evil0ctal
# 感谢原作者 Evil0ctal 的开源贡献。
# Apache License 2.0: `https://github.com/Evil0ctal/Douyin_TikTok_Download_API/blob/main/LICENSE`
# 协议副本: licenses/Apache-2.0
# ============================================================

from hashlib import md5
from time import time
from urllib.parse import quote, unquote

__all__ = [
    "SALT",
    "SIGNATURE_PARAM",
    "UIFID_PARAM",
    "TIMESTAMP_PARAM",
    "normalize_query",
    "sign",
]

# douyin_web 项目的盐值
SALT = "A96D855A08C0A9707F8BEF0D9A527E4E"

SIGNATURE_PARAM = "x-secsdk-web-signature"
UIFID_PARAM = "uifid"
TIMESTAMP_PARAM = "timestamp"


def _query_pairs(query: str) -> list[tuple[str, str]]:
    """Decode encoded query bytes while preserving literal ``+`` signs."""

    pairs: list[tuple[str, str]] = []
    for part in query.split("&"):
        if not part:
            continue
        name, _, value = part.partition("=")
        pairs.append((unquote(name), unquote(value)))
    return pairs


def _encode_pairs(pairs: list[tuple[str, str]]) -> str:
    """Serialize pairs with the native WebSign percent-encoding rules."""

    return "&".join(
        f"{quote(name, safe='*-._')}={quote(value, safe='*-._')}"
        for name, value in pairs
    )


def normalize_query(query: str) -> str:
    """Return the canonical query byte sequence emitted by WebSign."""
    return _encode_pairs(_query_pairs(query))


def sign(
    query: str,
    uifid: str,
    *,
    timestamp: int | None = None,
) -> tuple[str, str]:
    """对 query 追加访客时间戳并计算 x-secsdk-web-signature。

    Args:
        query: 待签名的完整 query 字符串，为最终发送的字节序，
            必须已包含 uifid 参数（SDK 亦将其保持原位，重复追加会
            产生不同的预映像从而被平台拒绝）。签名覆盖该字符串与
            timestamp 参数，不含签名参数本身。
        uifid: 访客 ID，签名的绑定对象。
        timestamp: 秒级时间戳，测试时可固定；缺省取当前时间。

    Returns:
        (signed_query, signature)：signed_query 以
        ``&x-secsdk-web-signature={signature}`` 结尾，可原样发送。
    """
    stamp = str(int(time() if timestamp is None else timestamp))
    # 预映像中的 query 即发送字节序本身：签名覆盖的字节与发送的字节一致
    pairs = _query_pairs(query)
    if not any(name == UIFID_PARAM for name, _ in pairs):
        pairs.append((UIFID_PARAM, uifid))
    pairs.append((TIMESTAMP_PARAM, stamp))
    hashed = _encode_pairs(pairs)
    signature = md5(f"{uifid}_{stamp}_{SALT}_{hashed}".encode()).hexdigest()
    return f"{hashed}&{SIGNATURE_PARAM}={signature}", signature
