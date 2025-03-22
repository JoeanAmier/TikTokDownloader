from typing import TYPE_CHECKING

from ..tools import cookie_str_to_dict
from ..translation import _

if TYPE_CHECKING:
    from ..config import Settings
    from ..tools import ColorfulConsole

__all__ = ["Cookie"]


class Cookie:
    STATE_KEY = "sessionid_ss"
    PLATFORM = (
        _("抖音"),
        "TikTok",
    )

    def __init__(self, settings: "Settings", console: "ColorfulConsole"):
        self.settings = settings
        self.console = console

    def run(
        self,
        key="cookie",
        tiktok=0,
    ):
        """提取 Cookie 并写入配置文件"""
        if not (
            cookie := self.console.input(
                _("请粘贴 {platform} Cookie 内容: ").format(
                    platform=self.PLATFORM[tiktok]
                )
            )
        ):
            return False
        self.extract(cookie, key=key)
        return True

    def extract(
        self,
        cookie: str,
        write=True,
        key="cookie",
    ) -> dict:
        cookie_dict = cookie_str_to_dict(cookie)
        self.__check_state(cookie_dict)
        if write:
            self.save_cookie(cookie_dict, key)
            self.console.print(_("写入 Cookie 成功！"))
        return cookie_dict

    def __check_state(self, items: dict) -> None:
        if items.get(self.STATE_KEY):
            self.console.print(_("当前 Cookie 已登录"))
        else:
            self.console.print(_("当前 Cookie 未登录"))

    def save_cookie(self, cookie: dict, key="cookie") -> None:
        data = self.settings.read()
        data[key] = cookie
        self.settings.update(data)
