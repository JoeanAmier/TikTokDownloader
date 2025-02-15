from rich.console import Console

from src.custom import (
    DATA_HEADERS,
    DATA_HEADERS_TIKTOK,
    DOWNLOAD_HEADERS_TIKTOK,
)
from src.encrypt import ABogus
from src.encrypt import XBogus
from src.testers.logger import Logger
from src.tools import create_client


class Params:
    def __init__(self):
        self.cookie = "自行填入抖音 Cookie"
        self.cookie_tiktok = "自行填入 TikTok Cookie"
        self.headers = DATA_HEADERS | {"Cookie": self.cookie}
        self.headers_tiktok = DATA_HEADERS_TIKTOK | {
            "Cookie": self.cookie_tiktok,
        }
        self.headers_download = DOWNLOAD_HEADERS_TIKTOK
        self.logger = Logger()
        self.ab = ABogus()
        self.xb = XBogus()
        self.console = Console()
        self.max_retry = 0
        self.timeout = 5
        self.max_pages = 2
        self.client = create_client(
            timeout=self.timeout,
        )
        self.client_tiktok = create_client(
            timeout=self.timeout,
            proxy="http://127.0.0.1:10809",
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
        await self.client_tiktok.aclose()
