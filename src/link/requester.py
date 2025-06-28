from re import compile
from typing import TYPE_CHECKING

from ..custom import BLANK_HEADERS
from ..custom import wait
from ..tools import Retry, DownloaderError, capture_error_request

if TYPE_CHECKING:
    from httpx import AsyncClient, get, head

    from ..config import Parameter

__all__ = ["Requester"]


class Requester:
    URL = compile(r"(https?://[^\s\"<>\\^`{|}，。；！？、【】《》]+)")
    HEADERS = BLANK_HEADERS

    def __init__(
        self,
        params: "Parameter",
        client: "AsyncClient",
    ):
        self.client = client
        self.log = params.logger
        self.max_retry = params.max_retry
        self.timeout = params.timeout

    async def run(
        self,
        text: str,
        proxy: str = None,
    ) -> str:
        urls = self.URL.finditer(text)
        if not urls:
            return ""
        result = []
        for i in urls:
            result.append(
                await self.request_url(
                    u := i.group(),
                    proxy=proxy,
                )
                or u
            )
            await wait()
        return " ".join(i for i in result if i)

    @Retry.retry
    @capture_error_request
    async def request_url(
        self,
        url: str,
        content="url",
        proxy: str = None,
    ):
        self.log.info(f"URL: {url}", False)
        match (content in {"url", "headers"}, bool(proxy)):
            case True, True:
                response = self.request_url_head_proxy(
                    url,
                    proxy,
                )
            case True, False:
                response = await self.request_url_head(url)
            case False, True:
                response = self.request_url_get_proxy(
                    url,
                    proxy,
                )
            case False, False:
                response = await self.request_url_get(url)
            case _:
                raise DownloaderError
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
                raise DownloaderError

    async def request_url_head(
        self,
        url: str,
    ):
        return await self.client.head(
            url,
        )

    def request_url_head_proxy(
        self,
        url: str,
        proxy: str,
    ):
        return head(
            url,
            headers=self.HEADERS,
            proxy=proxy,
            follow_redirects=True,
            verify=False,
            timeout=self.timeout,
        )

    async def request_url_get(
        self,
        url: str,
    ):
        response = await self.client.get(
            url,
        )
        response.raise_for_status()
        return response

    def request_url_get_proxy(
        self,
        url: str,
        proxy: str,
    ):
        response = get(
            url,
            headers=self.HEADERS,
            proxy=proxy,
            follow_redirects=True,
            verify=False,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response
