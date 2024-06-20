from typing import Any
from typing import TYPE_CHECKING
from typing import Union

from httpx import AsyncClient
from httpx import Client

from src.custom import TIMEOUT
from src.custom import USERAGENT
from src.tools import TikTokDownloaderError
from .capture import capture_error_params
from .retry import PrivateRetry

if TYPE_CHECKING:
    from src.record import BaseLogger
    from src.record import LoggerManager

__all__ = ["request_post", "request_get", "create_client"]


def create_client(
        user_agent=USERAGENT,
        timeout=TIMEOUT,
        headers: dict = None,
        *args,
        **kwargs,
) -> AsyncClient:
    return AsyncClient(
        headers=headers or {"User-Agent": user_agent, },
        timeout=timeout,
        follow_redirects=True,
        *args,
        **kwargs,
    )


async def request_post(
        logger: Union["BaseLogger", "LoggerManager"],
        url: str,
        data: Any = None,
        useragent=USERAGENT,
        timeout=TIMEOUT,
        headers: dict = None,
        content="headers",
        **kwargs,
):
    with Client(
            headers=headers or {
                "User-Agent": useragent,
            },
            timeout=timeout,
            **kwargs,
    ) as client:
        return await request(
            logger,
            client,
            "POST",
            url,
            content,
            data=data,
        )


async def request_get(
        logger: Union["BaseLogger", "LoggerManager"],
        url: str,
        data: Any = None,
        useragent=USERAGENT,
        timeout=TIMEOUT,
        headers: dict = None,
        content="headers",
        **kwargs,
):
    with Client(
            headers=headers or {
                "User-Agent": useragent,
            },
            timeout=timeout,
            **kwargs,
    ) as client:
        return await request(
            logger,
            client,
            "GET",
            url,
            content,
            data=data,
        )


@PrivateRetry.retry_lite
@capture_error_params
async def request(logger: Union["BaseLogger", "LoggerManager"],
                  client: Client,
                  method: str,
                  url: str,
                  content="json",
                  **kwargs):
    response = client.request(method, url, **kwargs)
    match content:
        case "headers":
            return response.headers
        case "text":
            return response.text
        case "content":
            return response.content
        case "json":
            return response.json()
        case "url":
            return str(response.url)
        case _:
            raise TikTokDownloaderError
