from re import compile
from typing import TYPE_CHECKING

# from ..custom import PHONE_HEADERS
from ..custom import wait
from ..tools import PrivateRetry
from ..tools import TikTokDownloaderError
from ..tools import capture_error_request

if TYPE_CHECKING:
    from ..config import Parameter
    from httpx import AsyncClient

__all__ = ["Requester"]


class Requester:
    URL = compile(r"(https?://\S+)")

    def __init__(self, params: "Parameter", client: "AsyncClient", ):
        self.client = client
        self.log = params.logger
        self.max_retry = params.max_retry

    async def run(self, text: str, ) -> str:
        urls = self.URL.finditer(text)
        if not urls:
            return ""
        result = []
        for i in urls:
            result.append(await self.request_url(u := i.group(), ) or u)
            await wait()
        return " ".join(i for i in result if i)

    @PrivateRetry.retry
    @capture_error_request
    async def request_url(self, url: str, content="url", ):
        self.log.info(f"URL: {url}", False)
        if content in {"url", "headers"}:
            response = await self.request_url_head(url)
        else:
            response = await self.request_url_get(url)
        self.log.info(f"Response URL: {response.url}", False)
        self.log.info(f"Response Code: {response.status_code}", False)
        # 记录请求体数据会导致日志文件体积过大，仅在必要时记录
        # self.log.info(f"Response Content: {response.content}", False)
        self.log.info(f"Response Headers: {dict(response.headers)}", False)
        match content:
            case "text":
                return response.text
            case "content":
                return response.content
            case "json":
                return response.json()
            case "headers":
                return response.headers
            case "url":
                return str(response.url)
            case _:
                raise TikTokDownloaderError

    async def request_url_head(self, url: str, ):
        return await self.client.head(url, )

    async def request_url_get(self, url: str, ):
        response = await self.client.get(url, )
        response.raise_for_status()
        return response
