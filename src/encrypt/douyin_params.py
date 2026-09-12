# ============================================================
# 声明 (Declaration)
#
# 本文件改编自以下项目的 a_bogus 与 x-secsdk-web-signature 签名实现：
#   `https://github.com/Evil0ctal/Douyin_TikTok_Download_API`
#   src/dtk/signing/native/abogus.py
#   src/dtk/signing/native/websign.py
#
#   - A-Bogus: 该项目逆向了抖音 bdms.js (v1.0.1.19-fix.01)。
#   - WebSign: 该项目逆向了抖音 secsdk（runtime_bundler_34.js,
#     @byted/secsdk-strategy v1.0.40, project-id="34"）的 webSignUrl。
# 本文件针对 DouK-Downloader 的接口和代码结构进行了适配。
# Portions Copyright (c) Evil0ctal
# 感谢原作者 Evil0ctal 的开源贡献。
# Apache License 2.0: `https://github.com/Evil0ctal/Douyin_TikTok_Download_API/blob/main/LICENSE`
# 协议副本: licenses/Apache-2.0
# ============================================================

from urllib.parse import parse_qsl, quote, unquote, urlencode, urlsplit

from ..custom import USERAGENT
from .aBogus import ABogus
from .params import Params
from .websign import UIFID_PARAM
from .websign import normalize_query as _websign_normalize_query
from .websign import sign as web_sign

__all__ = ["DouYinParams"]


# ============================================================
# 抖音签名保护接口列表
#
# 抖音并非对所有接口做签名保护：其网页 SDK（runtime_bundler_34.js）
# 的 webSign 策略在 config.protectedHost["www.douyin.com"].GET 中
# 声明了需要附加 x-secsdk-web-signature 的确切路径，列表照此复制。
# 实测（2026-09-08，每接口 8 次请求，纯 Python 签名）：
#
#     /aweme/v1/web/user/profile/other/   未保护   8/8 返回数据
#     /aweme/v1/web/comment/list/         未保护   8/8 返回数据
#     /aweme/v1/web/aweme/detail/         受保护   3/8，其余 403 Uifid Not Found
#     /aweme/v1/web/aweme/post/           受保护   3/8，其余 403 Uifid Not Found
#
# POST 列表是 GET 列表的子集，故不区分请求方法：将仅 POST 的路径
# 按 GET 同样对待，最多多算一次签名，不会被平台拒绝。
# ============================================================

DOUYIN_SIGNED_PATHS: frozenset[str] = frozenset(
    {
        "/aweme/v1/web/aweme/detail/",
        "/aweme/v1/web/aweme/post/",
        "/aweme/v1/web/aweme/favorite/",
        "/aweme/v1/web/aweme/listcollection/",
        "/aweme/v1/web/mix/aweme/",
        "/aweme/v1/web/tab/feed/",
        "/aweme/v1/web/mix/list/",
        "/aweme/v1/web/music/aweme/",
        "/aweme/v1/web/music/list/",
        "/aweme/v1/web/mix/detail/",
        "/aweme/v1/web/mix/listcollection/",
        "/aweme/v1/web/music/detail/",
        "/aweme/v1/web/collects/list/",
        "/aweme/v1/web/collects/video/list/",
    }
)


def _is_sign_protected(
    url: str,
) -> bool:
    """平台按精确路径（含末尾斜杠）匹配，其余接口原样发送"""

    path = urlsplit(url).path or "/"

    if not path.startswith("/"):
        path = "/" + path

    if not path.endswith("/"):
        path += "/"

    return path in DOUYIN_SIGNED_PATHS


def _data_to_string(
    data: dict | str | None,
) -> str:
    """请求体的字符串形式，与传输层的实际发送字节保持一致。

    传输层以表单形式发送字典（curl_cffi data=dict），因此此处
    同样以 urlencode 序列化；字符串按原样参与哈希
    """

    if data is None:
        return ""

    if isinstance(data, str):
        return data

    if isinstance(data, dict):
        return urlencode(
            data,
            doseq=True,
        )

    raise TypeError(f"data 类型错误: {type(data)!r}")


def _normalize_query(
    query: dict | str | None,
) -> str:
    """Serialize mappings once and canonicalize raw query strings."""

    if query is None:
        return ""

    if isinstance(query, dict):
        return urlencode(query, doseq=True)

    if isinstance(query, str):
        return urlencode(
            parse_qsl(query, keep_blank_values=True),
            doseq=True,
        )

    raise TypeError(f"query 类型错误: {type(query)!r}")


def _get_query_value(
    query: str,
    name: str,
) -> str:
    # WebSign's native path decodes percent escapes but deliberately keeps a
    # literal ``+`` in the value.
    for part in query.split("&"):
        if not part:
            continue
        key, _, value = part.partition("=")
        if unquote(key) == name:
            return unquote(value)
    return ""


class DouYinParams(Params):
    """
    TikTokDownloader 抖音参数实现。

    sign():

        只计算 a_bogus

    sign_url():

        a_bogus
            ↓
        完整 query
            ↓
        命中签名保护接口且 query 含 uifid 时
        追加 timestamp 与 x-secsdk-web-signature
            ↓
        返回最终 query
    """

    def __init__(self):
        super().__init__()

    # --------------------------------------------------------
    # ABogus
    # --------------------------------------------------------

    def _get_a_bogus(
        self,
        query: str,
        data: dict | str | None,
        user_agent: str,
    ) -> str:
        return ABogus(
            user_agent,
        ).get_value(
            query,
            body=_data_to_string(data),
        )

    # --------------------------------------------------------
    # sign
    # --------------------------------------------------------

    def sign(
        self,
        url: str = "",
        query: dict | str = "",
        data: dict | str | None = None,
        method: str = "",
        user_agent: str = USERAGENT,
        ms_token: str = "",
    ) -> dict[str, str]:

        query = _normalize_query(query)

        a_bogus = self._get_a_bogus(
            query,
            data,
            user_agent,
        )

        return {"a_bogus": a_bogus}

    # --------------------------------------------------------
    # sign_url
    # --------------------------------------------------------

    def sign_url(
        self,
        url: str = "",
        query: dict | str = "",
        data: dict | str | None = None,
        method: str = "",
        user_agent: str = USERAGENT,
        ms_token: str = "",
    ) -> str:

        # ================================================
        # 1. 规范化业务 query
        # ================================================

        query = _normalize_query(query)

        # 受保护接口使用 WebSign 的规范 query 表示计算 A-Bogus。
        # 普通接口不经过 WebSign，使用业务 query 表示。
        protected = bool(url and _is_sign_protected(url))
        uifid = _get_query_value(query, UIFID_PARAM) if protected else ""
        if uifid:
            query = _websign_normalize_query(query)

        a_bogus = self._get_a_bogus(
            query,
            data,
            user_agent,
        )

        # s4 字母表包含 "/" 与 "=" 填充，发送前需百分号编码
        signed_query = f"{query}&a_bogus={quote(a_bogus, safe='')}"

        # ================================================
        # 2. WebSign（仅受保护且带 UIFID 的接口）
        # ================================================

        if not uifid:
            return signed_query

        # 追加 timestamp 与 x-secsdk-web-signature；签名覆盖其前面的
        # 完整 query（含 a_bogus）。
        return web_sign(
            signed_query,
            uifid,
        )[0]
