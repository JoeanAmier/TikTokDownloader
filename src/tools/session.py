from typing import TYPE_CHECKING, Union

from httpx import AsyncClient, AsyncHTTPTransport, Client, HTTPTransport

from ..custom import TIMEOUT, USERAGENT
from ..tools import DownloaderError
from .capture import capture_error_params
from .retry import Retry

if TYPE_CHECKING:
    from ..record import BaseLogger, LoggerManager
    from ..testers import Logger

__all__ = ["request_params", "create_client"]


def create_client(
    user_agent=USERAGENT,
    timeout=TIMEOUT,
    headers: dict = None,
    proxy: str = None,
    *args,
    **kwargs,
) -> AsyncClient:
    return AsyncClient(
        headers=headers
        or {
            "User-Agent": user_agent,
        },
        timeout=timeout,
        follow_redirects=True,
        verify=False,
        mounts={
            "http://": AsyncHTTPTransport(proxy=proxy),
            "https://": AsyncHTTPTransport(proxy=proxy),
        },
        *args,
        **kwargs,
    )


async def request_params(
    logger: Union[
        "BaseLogger",
        "LoggerManager",
        "Logger",
    ],
    url: str,
    method: str = "POST",
    params: dict | str = None,
    data: dict | str = None,
    useragent=USERAGENT,
    timeout=TIMEOUT,
    headers: dict = None,
    resp="headers",
    proxy: str = None,
    **kwargs,
):
    with Client(
        headers=headers
        or {
            "User-Agent": useragent,
            "Content-Type": "application/json; charset=utf-8",
            # "Referer": "https://www.douyin.com/"
        },
        follow_redirects=True,
        timeout=timeout,
        verify=False,
        mounts={
            "http://": HTTPTransport(proxy=proxy),
            "https://": HTTPTransport(proxy=proxy),
        },
    ) as client:
        return await request(
            logger,
            client,
            method,
            url,
            resp,
            params=params,
            data=data,
            **kwargs,
        )


@Retry.retry_lite
@capture_error_params
async def request(
    logger: Union[
        "BaseLogger",
        "LoggerManager",
        "Logger",
    ],
    client: Client,
    method: str,
    url: str,
    resp="json",
    **kwargs,
):
    response = client.request(method, url, **kwargs)
    response.raise_for_status()
    match resp:
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
        case "response":
            return response
        case _:
            raise DownloaderError
