from typing import TYPE_CHECKING

from src.tools import cookie_str_to_dict

if TYPE_CHECKING:
    from src.config import Settings
    from src.tools import ColorfulConsole

__all__ = ["Cookie"]


class Cookie:

    def __init__(self, settings: "Settings", console: "ColorfulConsole"):
        self.settings = settings
        self.console = console

    def run(self, key="cookie"):
        """提取 Cookie 并写入配置文件"""
        if not (
                cookie := self.console.input(
                    "请粘贴 Cookie 内容: ")):
            return
        self.extract(cookie, key=key)

    def extract(self, cookie: str, write=True, key="cookie", ) -> dict:
        cookie_dict = cookie_str_to_dict(cookie)
        self.__check_state(cookie_dict)
        if write:
            self.save_cookie(cookie_dict, key)
            self.console.print("写入 Cookie 成功！")
        return cookie_dict

    def __check_state(self, items: dict) -> None:
        if items.get("sessionid_ss"):
            self.console.print("当前 Cookie 已登录")
        else:
            self.console.print("当前 Cookie 未登录")

    def save_cookie(self, cookie: dict, key="cookie") -> None:
        data = self.settings.read()
        data[key] = cookie
        self.settings.update(data)
