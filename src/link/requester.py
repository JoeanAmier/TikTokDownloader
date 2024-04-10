from re import compile
from typing import TYPE_CHECKING

from src.tools import PrivateRetry
from src.tools import capture_error_request

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["Requester"]


class Requester:
    URL = compile(r"(https?://\S+)")

    def __init__(self, params: "Parameter"):
        self.session = params.session
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
    @capture_error_request
    async def request_url(self, url: str, proxy: str = None, content="url", ) -> str:
        async with self.session.get(url, proxy=proxy) as response:
            match content:
                case "headers":
                    return response.headers
                case "text":
                    return await response.text()
                case "json":
                    return await response.json()
                case "url":
                    return str(response.url)
                case _:
                    raise ValueError
