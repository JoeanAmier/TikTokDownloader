from typing import TYPE_CHECKING

from browser_cookie3 import (
    chrome,
    chromium,
    opera,
    opera_gx,
    brave,
    edge,
    vivaldi,
    firefox,
    librewolf,
    safari,
    BrowserCookieError,
)

from src.custom import WARNING

if TYPE_CHECKING:
    from src.module import Cookie
    from src.config import Parameter

__all__ = ["Browser"]


class Browser:
    """代码参考：https://github.com/Johnserf-Seed/f2/blob/main/f2/apps/douyin/cli.py"""
    browser = (
        chrome,
        chromium,
        opera,
        opera_gx,
        brave,
        edge,
        vivaldi,
        firefox,
        librewolf,
        safari)

    def __init__(self, parameters: "Parameter", cookie_object: "Cookie"):
        self.console = parameters.console
        self.cookie_object = cookie_object

    def run(self, domain="douyin.com"):
        browser = self.console.input(
            "自动读取指定浏览器的 Cookie 并写入配置文件\n"
            "支持浏览器：1 Chrome, 2 Chromium, 3 Opera, 4 Opera GX, 5 Brave, 6 Edge, 7 Vivaldi, 8 Firefox, 9 LibreWolf, "
            "10 Safari\n"
            "请先关闭对应的浏览器，然后输入浏览器序号：")
        try:
            cookie = self.browser[int(browser) - 1](domain_name=domain)
            cookie = self.__extract_cookie(cookie)
            self.__save_cookie(cookie)
        except ValueError:
            self.console.print("浏览器序号错误，未写入 Cookie！")
        except PermissionError:
            self.console.print(
                "获取 Cookie 失败，请先关闭对应的浏览器，然后输入浏览器序号！",
                style=WARNING)
        except BrowserCookieError:
            self.console.print(
                "获取 Cookie 失败，未找到对应浏览器的 Cookie 数据！",
                style=WARNING)

    @staticmethod
    def __extract_cookie(cookie) -> dict:
        return {i.name: i.value for i in cookie}

    def __save_cookie(self, cookie: dict):
        self.cookie_object.write(cookie)
