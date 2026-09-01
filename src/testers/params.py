from configparser import ConfigParser, NoOptionError, NoSectionError

from src.config import Parameter
from src.custom import (
    DATA_HEADERS,
    DATA_HEADERS_TIKTOK,
    DOWNLOAD_HEADERS_TIKTOK,
    IMPERSONATE,
    USERAGENT,
    VOLUME,
)
from src.encrypt import DouYinParams, TikTokParams
from src.testers.logger import Logger
from src.tools import Cleaner, ColorfulConsole, create_client


class Params:
    CONFIG = VOLUME.joinpath("test_cookie.ini")
    CLEANER = Cleaner()

    def __init__(self):
        self.cookie_str = ""
        self.cookie_str_tiktok = ""
        self.uifid = ""
        self.msToken = ""
        self.msToken_tiktok = ""
        self.config = ConfigParser(
            interpolation=None,
        )
        self.read_ini()
        self.headers = DATA_HEADERS | {"Cookie": self.cookie_str}
        self.headers_tiktok = DATA_HEADERS_TIKTOK | {
            "Cookie": self.cookie_str_tiktok,
        }
        self.headers_download = DOWNLOAD_HEADERS_TIKTOK
        self.logger = Logger()
        self.douyin_params = DouYinParams()
        self.tiktok_params = TikTokParams()
        self.console = ColorfulConsole()
        self.max_retry = 0
        self.timeout = 5
        self.max_pages = 2
        self.proxy = None
        self.proxy_tiktok = "http://127.0.0.1:10808"
        self.date_format = "%Y-%m-%d %H:%M:%S"
        self.impersonate = IMPERSONATE
        self.impersonate_tiktok = IMPERSONATE
        self.user_agent = USERAGENT
        self.user_agent_tiktok = USERAGENT
        self.client = create_client(
            timeout=self.timeout,
            proxy=self.proxy,
            impersonate=self.impersonate,
        )
        self.client_tiktok = create_client(
            timeout=self.timeout,
            proxy=self.proxy_tiktok,
            impersonate=self.impersonate,
        )
        self.douyin_params, self.tiktok_params = (
            Parameter.check_objects_from_external_py(self.console)
        )

    def create_ini(self):
        self.config["dy"] = {
            "cookie": "",
            "uifid": "",
            "msToken": "",
        }
        self.config["tk"] = {
            "cookie": "",
            "msToken": "",
        }
        with self.CONFIG.open("w", encoding="utf-8") as configfile:
            self.config.write(configfile)

    def read_ini(self):
        if not self.config.read(self.CONFIG):
            self.create_ini()
            return
        try:
            self.cookie_str = self.config.get(
                "dy",
                "cookie",
            )
            self.uifid = self.config.get(
                "dy",
                "uifid",
            )
            self.msToken = self.config.get(
                "dy",
                "msToken",
            )
            self.cookie_str_tiktok = self.config.get(
                "tk",
                "cookie",
            )
            self.msToken_tiktok = self.config.get(
                "tk",
                "msToken",
            )
        except (NoSectionError, NoOptionError) as e:
            print(f"读取 Cookie 错误: {e}")
        if not self.cookie_str:
            print("警告: 抖音 Cookie 为空！")
        if not self.cookie_str_tiktok:
            print("警告: TikTok Cookie 为空！")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.close()
        await self.client_tiktok.close()


async def test():
    async with Params() as params:
        print(params.cookie_str)
        print(params.cookie_str_tiktok)


if __name__ == "__main__":
    from asyncio import run

    run(test())
