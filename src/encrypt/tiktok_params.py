"""
TikTok Web 请求签名参数生成器
================================

封装第三方开源项目 `tiktok-web-params <https://github.com/xvhuan/tiktok-web-params>`
（作者 xvhuan，MIT License），提供 TikTok Web 接口所需的
X-Dynosaur / X-Gnarly / X-Bogus 三个签名参数的本地计算能力。

源代码
------
JS 算法来源：
    https://github.com/xvhuan/tiktok-web-params
    原始文件：tiktok-web-params.js
    作者：xvhuan
    协议：MIT

用途限制 / ⚠️ For Learning & Exchange Only
-----------------------------------------
本模块仅供 **学习交流、授权测试、安全研究** 使用。**禁止**：

- 用于绕过 TikTok 或任何平台的风控、限流、反爬措施；
- 用于批量抓取、爬虫、数据挖掘等违反平台《服务条款》的行为；
- 用于任何商业化或未授权场景。

使用者应自行确保其使用场景合法合规，并承担由此产生的一切法律责任。
作者 (xvhuan) 与本项目维护者均不对任何滥用或违规使用承担责任。
"""

from typing import Any
from urllib.parse import quote, urlencode

from ..custom import ROOT, USERAGENT
from ..tools import is_node_available
from .params import Params

__all__ = ["TikTokParams"]

_JS_FILE = ROOT / "static" / "js" / "tiktok-web-params.js"

_DEFAULT_ENV: dict[str, int] = {
    "envcode": 1,
    "ubcode": 0,
    "txr": 11,
    "tfr": 22,
    "ixr": 33,
    "ifr": 44,
}


class TikTokParams(Params):
    """TikTok Web 请求签名参数生成器。

    封装的 JS 算法来源于第三方开源项目
    `xvhuan/tiktok-web-params <https://github.com/xvhuan/tiktok-web-params>`
    （MIT License），本类仅负责加载、调用与返回结果包装。

    ⚠️ 仅供学习交流 / 授权测试 / 安全研究，请勿用于绕过风控、批量抓取或
    违反任何平台服务条款的场景。
    """

    def __init__(self) -> None:
        super().__init__()
        if is_node_available():
            from javascript import require

            self._js = require(str(_JS_FILE.resolve()))
        else:
            self._js = None

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
        计算 TikTok Web 接口的三个签名参数。

        Parameters
        ----------
        query : dict | str
            原始查询字符串或字典。
        data : dict | str | None
            未使用，保留参数。
        method : str
            未使用，保留参数。
        user_agent : str
            请求使用的 User-Agent。
        ms_token : str
            参与签名的 msToken。

        Returns
        -------
        dict
            键为 ``X-Dynosaur`` / ``X-Gnarly`` / ``X-Bogus``。
        """
        if self._js is None:
            return {
                "X-Dynosaur": "",
                "X-Gnarly": "",
                "X-Bogus": "",
            }
        if isinstance(query, dict):
            query = urlencode(
                query,
                safe="=",
                quote_via=quote,
            )
        opts: dict[str, Any] = {
            "ua": user_agent,
            "msToken": ms_token,
            "env": _DEFAULT_ENV,
        }
        result = self._js.signUrl(query, opts)
        x_dynosaur = result["dynosaur"]
        x_gnarly = result["gnarly"]
        x_bogus = result["xbogus"]
        return {
            "X-Dynosaur": x_dynosaur,
            "X-Gnarly": x_gnarly,
            "X-Bogus": x_bogus,
        }

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
            接口基础地址；留空则仅返回 query 字符串。
        query : dict | str
            原始查询字符串或字典。
        data : dict | str | None
            未使用，保留参数。
        method : str
            未使用，保留参数。
        user_agent : str
            User-Agent。
        ms_token : str
            msToken。

        Returns
        -------
        str
            完整 URL 或带签名的 query 字符串。
        """
        if isinstance(query, dict):
            query = urlencode(
                query,
                safe="=",
                quote_via=quote,
            )
        params = self.sign(url, query, data, method, user_agent, ms_token)
        signed_query = "&".join(
            [
                query,
                f"X-Dynosaur={params['X-Dynosaur']}",
                f"X-Bogus={params['X-Bogus']}",
                f"X-Gnarly={params['X-Gnarly']}",
            ]
        )
        # if not url:
        #     return signed_query
        # sep = "&" if "?" in url else "?"
        # return f"{url}{sep}{signed_query}"
        return signed_query
