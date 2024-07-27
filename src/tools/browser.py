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
    # opera_gx,
    # safari,
    vivaldi,
)

from src.custom import WARNING

if TYPE_CHECKING:
    from src.module import Cookie
    from src.config import Parameter
    from typing import Callable

__all__ = ["Browser"]


class Browser:
    browser = (
        arc,
        brave,
        chrome,
        chromium,
        edge,
        firefox,
        librewolf,
        opera,
        # opera_gx,
        # safari,
        vivaldi,
    )
    platform = {
        False: SimpleNamespace(
            name="抖音",
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

    def run(self, tiktok=False):
        browser = self.console.input(
            f"自动读取指定浏览器的 {self.platform[tiktok].name} Cookie 并写入配置文件\n"
            "1. Arc: Linux, macOS, Windows\n"
            "2. Brave: Linux, macOS, Windows\n"
            "3. Chrome: Linux, macOS, Windows\n"
            "4. Chromium: Linux, macOS, Windows\n"
            "5. Edge: Linux, macOS, Windows\n"
            "6. Firefox: Linux, macOS, Windows\n"
            "7. LibreWolf: Linux, macOS, Windows\n"
            "8. Opera: Linux, macOS, Windows\n"
            # "9. Opera GX: macOS, Windows\n"
            # "10. Safari: macOS\n"
            # "11. Vivaldi: Linux, macOS, Windows\n"
            "9. Vivaldi: Linux, macOS, Windows\n"
            "请输入浏览器序号：")
        try:
            cookie = self.__read_cookie(
                self.browser[int(browser) - 1], tiktok, )
            self.__save_cookie(cookie, tiktok)
            return True
        except ValueError:
            self.console.print("浏览器序号输入错误，未写入 Cookie！")
        except RuntimeError:
            self.console.print(
                "读取 Cookie 失败，未找到对应浏览器的 Cookie 数据！",
                style=WARNING)
        return False

    def __read_cookie(self, browser: "Callable", tiktok: bool) -> dict:
        platform = self.platform[tiktok]
        cookies = browser(domains=platform.domain, )
        return {i["name"]: i["value"] for i in cookies}

    def __save_cookie(self, cookie: dict, tiktok: bool):
        self.cookie_object.save_cookie(cookie, self.platform[tiktok].key)
