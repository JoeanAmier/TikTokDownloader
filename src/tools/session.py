from typing import Any
from typing import TYPE_CHECKING
from typing import Union

from aiohttp import ClientSession
from aiohttp import ClientTimeout

from src.custom import TIMEOUT
from src.custom import USERAGENT
from .capture import capture_error_params
from .retry import PrivateRetry

if TYPE_CHECKING:
    from src.record import BaseLogger
    from src.record import LoggerManager

__all__ = ["request_post", "request_get", "base_session"]


def base_session(
        user_agent=USERAGENT,
        timeout=TIMEOUT,
        headers: dict = None,
) -> ClientSession:
    return ClientSession(
        headers=headers or {"User-Agent": user_agent, },
        timeout=ClientTimeout(connect=timeout),
    )


@PrivateRetry.retry_lite
@capture_error_params
async def request_post(logger: Union["BaseLogger", "LoggerManager"],
                       url: str,
                       data: Any = None,
                       useragent=USERAGENT,
                       timeout=TIMEOUT,
                       headers: dict = None,
                       content="headers",
                       proxy: str = None,
                       **kwargs):
    async with ClientSession(headers=headers or {
        "User-Agent": useragent,
    }, timeout=ClientTimeout(connect=timeout), ) as session:
        async with session.post(url, data=data, proxy=proxy, **kwargs) as response:
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


@PrivateRetry.retry_lite
@capture_error_params
async def request_get(logger: Union["BaseLogger", "LoggerManager"],
                      url: str,
                      allow_redirects: bool = True,
                      useragent=USERAGENT,
                      timeout=TIMEOUT,
                      headers: dict = None,
                      content="json",
                      proxy: str = None,
                      **kwargs):
    async with ClientSession(headers=headers or {
        "User-Agent": useragent,
    }, timeout=ClientTimeout(connect=timeout), ) as session:
        async with session.get(url, allow_redirects=allow_redirects, proxy=proxy, **kwargs) as response:
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
