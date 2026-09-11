# ============================================================
# 声明 (Declaration)
#
# 本文件的 X-Dynosaur / X-Gnarly 为纯 Python 实现，整理自
# (Apache-2.0 License):
#   https://github.com/mlkt/Douyin_TikTok_Download_API
#
#   该项目对 TikTok 网页端 webmssdk (2.0.0.561) 的独立逆向，
#   并经 Node 运行原版 SDK 逐字节对照验证，详见
#   src/encrypt/tiktok_sign.py
#
# 用途限制 / ⚠️ For Learning & Exchange Only
# -----------------------------------------
# 本模块仅供学习交流、授权测试、安全研究使用，禁止用于绕过
# TikTok 或任何平台的风控措施、批量抓取等违反平台服务条款的行为。
# ============================================================

from urllib.parse import urlencode

from ..custom import USERAGENT
from .params import Params
from .tiktok_sign import sign as tiktok_sign

__all__ = ["TikTokParams"]


class TikTokParams(Params):
    """TikTok Web 请求签名参数生成器。

    封装的算法为对 TikTok 网页端 webmssdk 的独立逆向成果
    （Apache-2.0，见 src/encrypt/tiktok_sign.py），本类仅负责
    调用与结果包装。

    ⚠️ 仅供学习交流 / 授权测试 / 安全研究，请勿用于绕过风控、批量
    抓取或违反任何平台服务条款的场景。
    """

    def __init__(self) -> None:
        super().__init__()

    def sign(
        self,
        url: str = "",
        query: dict | str = "",
        data: dict | str | None = None,
        method: str = "",
        user_agent: str = USERAGENT,
        ms_token: str = "",
    ) -> dict[str, str]:
        """
        计算 TikTok Web 接口的四个签名参数。

        Parameters
        ----------
        query : dict | str
            原始查询字符串或字典，为最终发送的字节序。
        data : dict | str | None
            POST 请求体；字典以表单形式序列化后参与封印。
        method : str
            未使用，保留参数。
        user_agent : str
            请求使用的 User-Agent，必须与实际发送的一致。
        ms_token : str
            参与签名的 msToken；query 中已包含时以 query 为准。

        Returns
        -------
        dict
            键为 ``X-Dynosaur`` / ``msToken`` / ``X-Bogus`` / ``X-Gnarly``。
        """
        _, parameters = tiktok_sign(
            _query_to_string(query),
            user_agent,
            ms_token=ms_token,
            body=_data_to_bytes(data),
        )
        return parameters

    def sign_url(
        self,
        url: str = "",
        query: dict | str = "",
        data: dict | str | None = None,
        method: str = "",
        user_agent: str = USERAGENT,
        ms_token: str = "",
    ) -> str:
        """
        Parameters
        ----------
        url : str
            接口基础地址；签名层不拼接 URL，由传输层组合。
        query : dict | str
            原始查询字符串或字典，为最终发送的字节序。
        data : dict | str | None
            POST 请求体。
        method : str
            未使用，保留参数。
        user_agent : str
            User-Agent。
        ms_token : str
            msToken。

        Returns
        -------
        str
            带完整签名的 query 字符串：

            ``<业务 query>&X-Dynosaur=..&msToken=..&X-Bogus=1&X-Gnarly=..``

            参数顺序与封印范围均由 SDK 决定，签发后不可调序。
        """
        signed_query, _ = tiktok_sign(
            _query_to_string(query),
            user_agent,
            ms_token=ms_token,
            body=_data_to_bytes(data),
        )
        return signed_query


def _query_to_string(
    query: dict | str | None,
) -> str:

    if query is None:
        return ""

    if isinstance(query, str):
        return query

    if isinstance(query, dict):
        return urlencode(
            query,
            doseq=True,
        )

    raise TypeError(f"query 类型错误: {type(query)!r}")


def _data_to_bytes(
    data: dict | str | None,
) -> bytes:
    """请求体的字节形式，与传输层的实际发送字节保持一致。"""

    if data is None:
        return b""

    if isinstance(data, str):
        return data.encode("utf-8")

    if isinstance(data, dict):
        return urlencode(
            data,
            doseq=True,
        ).encode("utf-8")

    raise TypeError(f"data 类型错误: {type(data)!r}")
