from typing import TYPE_CHECKING, Union

from curl_cffi.requests import AsyncSession, Session

from ..custom import IMPERSONATE, TIMEOUT, USERAGENT
from ..tools import DownloaderError
from .capture import capture_error_params
from .retry import Retry

if TYPE_CHECKING:
    from ..record import BaseLogger, LoggerManager
    from ..testers import Logger

__all__ = ["request_params", "create_client"]


def create_client(
    timeout=TIMEOUT,
    headers: dict | None = None,
    proxy: str | None = None,
    impersonate=IMPERSONATE,
    *args,
    **kwargs,
) -> AsyncSession:
    return AsyncSession(
        headers=headers,
        timeout=timeout,
        allow_redirects=True,
        verify=False,
        proxy=proxy,
        impersonate=impersonate,
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
    params: dict | str = "",
    data: dict | str = "",
    useragent=USERAGENT,
    timeout=TIMEOUT,
    headers: dict | None = None,
    resp="headers",
    proxy: str | None = None,
    impersonate=IMPERSONATE,
    **kwargs,
):
    with Session(
        headers=headers
        or {
            "Content-Type": "application/json; charset=utf-8",
            # "Referer": "https://www.douyin.com/"
        },
        allow_redirects=True,
        timeout=timeout,
        verify=False,
        proxy=proxy,
        impersonate=impersonate,
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
    client: Session,
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