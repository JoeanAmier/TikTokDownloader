# ============================================================
# 声明 (Declaration)
#
# 本文件算法整理自 (Apache-2.0 License):
#   https://github.com/mlkt/Douyin_TikTok_Download_API
#   src/dtk/signing/native/websign.py
#
# 该项目对抖音 secsdk（runtime_bundler_34.js, @byted/secsdk-strategy
# v1.0.40, project-id="34"）webSignUrl 的独立逆向：
#
#     signature = md5("{uifid}_{timestamp}_{SALT}_{query}")
#
# 盐值为字节码字符串表第 39 号字符串，随 project 变化。
# 签名是四个输入的纯函数，无 nonce、无会话状态。
# ============================================================

from hashlib import md5
from time import time

__all__ = [
    "SALT",
    "SIGNATURE_PARAM",
    "UIFID_PARAM",
    "TIMESTAMP_PARAM",
    "sign",
]

# douyin_web 项目的盐值
SALT = "A96D855A08C0A9707F8BEF0D9A527E4E"

SIGNATURE_PARAM = "x-secsdk-web-signature"
UIFID_PARAM = "uifid"
TIMESTAMP_PARAM = "timestamp"


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
    hashed = (
        f"{query}&{TIMESTAMP_PARAM}={stamp}" if query else f"{TIMESTAMP_PARAM}={stamp}"
    )
    signature = md5(f"{uifid}_{stamp}_{SALT}_{hashed}".encode()).hexdigest()
    return f"{hashed}&{SIGNATURE_PARAM}={signature}", signature
