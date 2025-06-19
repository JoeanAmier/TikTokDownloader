from typing import TYPE_CHECKING
from ..tools import cookie_str_to_dict
from ..translation import _
from re import compile
from pyperclip import paste

if TYPE_CHECKING:
    from ..config import Settings
    from ..tools import ColorfulConsole

__all__ = ["Cookie"]


class Cookie:
    PATTERN = compile(r"[!#$%&'*+\-.^_`|~0-9A-Za-z]+=([^;\s][^;]*)")
    STATE_KEY = "sessionid_ss"
    PLATFORM_KEY = {
        False: "cookie",
        True: "cookie_tiktok",
    }

    def __init__(self, settings: "Settings", console: "ColorfulConsole"):
        self.settings = settings
        self.console = console
        self.PLATFORM_NAME = {
            False: _("抖音"),
            True: "TikTok",
        }

    def run(
        self,
        tiktok=False,
    ) -> bool:
        """提取 Cookie 并写入配置文件"""
        if self.validate_cookie_minimal(cookie := paste()):
            self.extract(
                cookie,
                key=self.PLATFORM_KEY[tiktok],
                platform=self.PLATFORM_NAME[tiktok],
            )
            return True
        self.console.warning(_("当前剪贴板的内容不是有效的 Cookie 内容！"))
        return False

    def extract(
        self,
        cookie: str,
        write=True,
        key="cookie",
        platform: str = ...,
    ) -> dict:
        cookie_dict = cookie_str_to_dict(cookie)
        self.__check_state(
            cookie_dict,
            platform,
        )
        if write:
            self.save_cookie(cookie_dict, key)
            self.console.print(
                _(f"写入 {platform} Cookie 成功！").format(platform=platform)
            )
        return cookie_dict

    def __check_state(self, items: dict, platform: str) -> None:
        if items.get(self.STATE_KEY):
            self.console.print(
                _(f"当前 {platform} Cookie 已登录").format(platform=platform)
            )
        else:
            self.console.print(
                _(f"当前 {platform} Cookie 未登录").format(platform=platform)
            )

    def save_cookie(self, cookie: dict, key="cookie") -> None:
        data = self.settings.read()
        data[key] = cookie
        self.settings.update(data)

    @classmethod
    def validate_cookie_minimal(cls, cookie_str: str) -> bool:
        """
        只检查整个字符串中是否存在 key=value 子串，
        且 key 和 value 都非空。
        返回 True 或 False。
        """
        if not isinstance(cookie_str, str):
            return False
        return bool(cls.PATTERN.search(cookie_str))
