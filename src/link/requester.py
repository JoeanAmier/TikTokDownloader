from re import compile
from typing import TYPE_CHECKING

from src.module import capture_error_url
from src.tools import PrivateRetry
from src.tools import base_session

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["Requester"]


class Requester:
    URL = compile(r"(https?://\S+)")

    def __init__(self, params: "Parameter"):
        self.session = base_session(
            params.headers["User-Agent"], params.timeout)
        self.log = params.logger
        self.max_retry = params.max_retry

    async def run(self, text: str, proxy: str = None) -> str:
        urls = self.URL.finditer(text)
        if not urls:
            return ""
        result = []
        for i in urls:
            result.append(await self.request_url(i.group(), proxy))
        return " ".join(i for i in result if i)

    @PrivateRetry.retry
    @capture_error_url
    async def request_url(self, url: str, proxy: str = None) -> str:
        async with self.session.get(url, proxy=proxy) as response:
            return str(response.url)

    async def close(self):
        await self.session.close()
