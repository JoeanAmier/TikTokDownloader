from configparser import ConfigParser, NoSectionError, NoOptionError

from rich.console import Console

from src.custom import (
    DATA_HEADERS,
    DATA_HEADERS_TIKTOK,
    DOWNLOAD_HEADERS_TIKTOK,
)
from src.custom import PROJECT_ROOT
from src.encrypt import ABogus
from src.encrypt import XBogus
from src.testers.logger import Logger
from src.tools import Cleaner
from src.tools import create_client


class Params:
    CONFIG = PROJECT_ROOT.joinpath("test_cookie.ini")
    CLEANER = Cleaner()

    def __init__(self):
        self.cookie_str = ""
        self.cookie_str_tiktok = ""
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
        self.ab = ABogus()
        self.xb = XBogus()
        self.console = Console()
        self.max_retry = 0
        self.timeout = 5
        self.max_pages = 2
        self.date_format = "%Y-%m-%d %H:%M:%S"
        self.client = create_client(
            timeout=self.timeout,
        )
        self.client_tiktok = create_client(
            timeout=self.timeout,
            proxy="http://127.0.0.1:10809",
        )

    def create_ini(self):
        self.config["dy"] = {
            "cookie": "",
        }
        self.config["tk"] = {
            "cookie": "",
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
            self.cookie_str_tiktok = self.config.get(
                "tk",
                "cookie",
            )
        except (NoSectionError, NoOptionError) as e:
            print(f"读取 Cookie 错误: {e}")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
        await self.client_tiktok.aclose()


async def test():
    async with Params() as params:
        print(params.cookie_str)
        print(params.cookie_str_tiktok)


if __name__ == "__main__":
    from asyncio import run

    run(test())
