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

from never_jscore import Context

from ..custom import ROOT, USERAGENT

__all__ = ["TikTokWebParams"]

_JS_FILE = ROOT / "static" / "js" / "tiktok-web-params.js"

_DEFAULT_ENV: dict[str, int] = {
    "envcode": 1,
    "ubcode": 0,
    "txr": 11,
    "tfr": 22,
    "ixr": 33,
    "ifr": 44,
}


def _load_js() -> str:
    return _JS_FILE.read_text(encoding="utf-8")


class TikTokWebParams:
    """TikTok Web 请求签名参数生成器。

    封装的 JS 算法来源于第三方开源项目
    `xvhuan/tiktok-web-params <https://github.com/xvhuan/tiktok-web-params>`
    （MIT License），本类仅负责加载、调用与返回结果包装。

    ⚠️ 仅供学习交流 / 授权测试 / 安全研究，请勿用于绕过风控、批量抓取或
    违反任何平台服务条款的场景。
    """

    def __init__(self) -> None:
        self._ctx = Context()
        self._ctx.compile(_load_js())

    def sign(
        self,
        query: str,
        user_agent: str = USERAGENT,
        ms_token: str = "",
    ) -> dict[str, str]:
        """
        调用 JS 中的 signUrl()，返回含 X-Dynosaur / X-Gnarly / X-Bogus 的字典。

        Parameters
        ----------
        query : str
            URL 查询字符串（如 "aid=1988&count=2"）。
        user_agent : str
            User-Agent。
        ms_token : str
            msToken，可为空字符串。

        Returns
        -------
        dict
            至少包含 ``X-Dynosaur`` / ``X-Gnarly`` / ``X-Bogus`` / ``msToken``。
        """
        opts: dict[str, Any] = {
            "ua": user_agent,
            "msToken": ms_token,
            "env": _DEFAULT_ENV,
        }
        result = self._ctx.call("signUrl", [query, opts])
        return {
            "X-Dynosaur": result.get("dynosaur", ""),
            "X-Gnarly": result.get("gnarly", ""),
            "X-Bogus": result.get("xbogus", ""),
            "msToken": ms_token,
        }

    def sign_url(
        self,
        base_url: str,
        query: str,
        user_agent: str = USERAGENT,
        ms_token: str = "",
    ) -> str:
        """
        便捷方法：传入基础 URL 和查询参数，返回拼好三个签名参数的完整 URL。

        Parameters
        ----------
        base_url : str
            基础 URL，例如 ``"https://www.tiktok.com/api/feed"``。
        query : str
            查询参数。
        user_agent : str
            User-Agent。
        ms_token : str
            msToken。

        Returns
        -------
        str
            形如 ``base_url?query&X-Dynosaur=...&msToken=...&X-Bogus=...&X-Gnarly=...``。
        """
        params = self.sign(query, user_agent, ms_token)
        sep = "&" if ("?" in base_url or query) else "?"
        return (
            f"{base_url}{sep}{query}"
            f"&X-Dynosaur={params['X-Dynosaur']}"
            f"&msToken={ms_token}"
            f"&X-Bogus={params['X-Bogus']}"
            f"&X-Gnarly={params['X-Gnarly']}"
        )
