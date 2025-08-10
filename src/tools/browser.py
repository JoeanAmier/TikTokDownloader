from contextlib import suppress
from sys import platform
from types import SimpleNamespace
from typing import TYPE_CHECKING

from rookiepy import (
    arc,
    brave,
    chrome,
    chromium,
    edge,
    firefox,
    librewolf,
    opera,
    opera_gx,
    vivaldi,
)

from ..translation import _

if TYPE_CHECKING:
    from ..config import Parameter
    from ..module import Cookie

__all__ = ["Browser"]


class Browser:
    SUPPORT_BROWSER = {
        "Arc": (arc, "Linux, macOS, Windows"),
        "Chrome": (chrome, "Linux, macOS, Windows"),
        "Chromium": (chromium, "Linux, macOS, Windows"),
        "Opera": (opera, "Linux, macOS, Windows"),
        "OperaGX": (opera_gx, "macOS, Windows"),
        "Brave": (brave, "Linux, macOS, Windows"),
        "Edge": (edge, "Linux, macOS, Windows"),
        "Vivaldi": (vivaldi, "Linux, macOS, Windows"),
        "Firefox": (firefox, "Linux, macOS, Windows"),
        "LibreWolf": (librewolf, "Linux, macOS, Windows"),
    }
    PLATFORM = {
        False: SimpleNamespace(
            name=_("抖音"),
            domain=[
                "douyin.com",
            ],
            key="cookie",
        ),
        True: SimpleNamespace(
            name="TikTok",
            domain=[
                "tiktok.com",
            ],
            key="cookie_tiktok",
        ),
    }

    def __init__(self, parameters: "Parameter", cookie_object: "Cookie"):
        self.console = parameters.console
        self.cookie_object = cookie_object
        self.options = "\n".join(
            (
                f"{i}. {k}: {v[1]}"
                for i, (k, v) in enumerate(
                    self.SUPPORT_BROWSER.items(),
                    start=1,
                )
            )
        )

    def run(
        self,
        tiktok=False,
        select: str = None,
    ):
        if browser := (
            select
            or self.console.input(
                _(
                    "读取指定浏览器的 {platform_name} Cookie 并写入配置文件；\n"
                    "注意：Windows 系统需要以管理员身份运行程序才能读取 Chromium、Chrome、Edge 浏览器 Cookie！\n"
                    "{options}\n"
                    "请输入浏览器名称或序号："
                ).format(
                    platform_name=self.PLATFORM[tiktok].name, options=self.options
                ),
            )
        ):
            if cookie := self.get(
                browser,
                self.PLATFORM[tiktok].domain,
            ):
                self.console.info(
                    _("读取 Cookie 成功！"),
                )
                self.__save_cookie(
                    cookie,
                    tiktok,
                )
            else:
                self.console.warning(
                    _("Cookie 数据为空！"),
                )
        else:
            self.console.print(_("未选择浏览器！"))

    def __save_cookie(self, cookie: dict, tiktok: bool):
        self.cookie_object.save_cookie(cookie, self.PLATFORM[tiktok].key)

    def get(
        self,
        browser: str | int,
        domains: list[str],
    ) -> dict[str, str]:
        if not (browser := self.__browser_object(browser)):
            self.console.warning(
                _("浏览器名称或序号输入错误！"),
            )
            return {}
        try:
            cookies = browser(domains=domains)
            return {i["name"]: i["value"] for i in cookies}
        except RuntimeError:
            self.console.warning(
                _("读取 Cookie 失败，未找到 Cookie 数据！"),
            )
        return {}

    @classmethod
    def __browser_object(cls, browser: str | int):
        with suppress(ValueError):
            browser = int(browser) - 1
        if isinstance(browser, int):
            try:
                return list(cls.SUPPORT_BROWSER.values())[browser][0]
            except IndexError:
                return None
        if isinstance(browser, str):
            try:
                return cls.__match_browser(browser)
            except KeyError:
                return None
        raise TypeError

    @classmethod
    def __match_browser(cls, browser: str):
        for i, j in cls.SUPPORT_BROWSER.items():
            if i.lower() == browser.lower():
                return j[0]


match platform:
    case "darwin":
        from rookiepy import safari

        Browser.SUPPORT_BROWSER |= {
            "Safari": (safari, "macOS"),
        }
    case "linux":
        Browser.SUPPORT_BROWSER.pop("OperaGX")
    case "win32":
        pass
    case _:
        print(_("从浏览器读取 Cookie 功能不支持当前平台！"))
