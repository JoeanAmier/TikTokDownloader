from http.cookiejar import CookieJar
from types import SimpleNamespace
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
from .format import cookie_jar_to_dict

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
    platform = {
        False: SimpleNamespace(
            domain=("douyin.com",),
            key="cookie"),
        True: SimpleNamespace(
            domain=("tiktok.com",),
            key="cookie_tiktok"),
    }

    def __init__(self, parameters: "Parameter", cookie_object: "Cookie"):
        self.console = parameters.console
        self.cookie_object = cookie_object

    def run(self, tiktok=False):
        browser = self.console.input(
            "自动读取指定浏览器的 Cookie 并写入配置文件\n"
            "支持浏览器：1 Chrome, 2 Chromium, 3 Opera, 4 Opera GX, 5 Brave, 6 Edge, 7 Vivaldi, 8 Firefox, 9 LibreWolf, "
            "10 Safari\n"
            "请关闭所有浏览器，然后输入浏览器序号：")
        try:
            cookie = self.__read_cookie(
                self.browser[int(browser) - 1], tiktok, )
            cookie = cookie_jar_to_dict(cookie)
            self.__save_cookie(cookie, tiktok)
            return True
        except ValueError:
            self.console.print("浏览器序号错误，未写入 Cookie！")
        except PermissionError:
            self.console.print(
                "获取 Cookie 失败，浏览器未完全关闭！",
                style=WARNING)
        except BrowserCookieError:
            self.console.print(
                "获取 Cookie 失败，未找到对应浏览器的 Cookie 数据！",
                style=WARNING)
        return False

    def __read_cookie(self, browser, tiktok: bool):
        platform = self.platform[tiktok]
        cookie = CookieJar()
        cookies = (browser(domain_name=i) for i in platform.domain)
        [cookie.set_cookie(item) for domain in cookies for item in domain]
        return cookie

    def __save_cookie(self, cookie: dict, tiktok: bool):
        self.cookie_object.save_cookie(cookie, self.platform[tiktok].key)
