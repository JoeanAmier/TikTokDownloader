from typing import Any
from typing import TYPE_CHECKING

from aiohttp import ClientError
from aiohttp import ClientSession
from aiohttp import ClientTimeout

from src.custom import TIMEOUT
from src.custom import USERAGENT
from src.custom import WARNING
from src.tools import retry_lite

if TYPE_CHECKING:
    from src.module import ColorfulConsole

__all__ = ["request_post", "request_get"]


@retry_lite
async def request_post(console: "ColorfulConsole", url: str, data: Any = None, useragent=USERAGENT, timeout=TIMEOUT,
                       **kwargs):
    try:
        async with ClientSession(headers={
            "User-Agent": useragent,
        }, timeout=ClientTimeout(connect=timeout), ) as session:
            async with session.post(url, data=data, **kwargs) as response:
                return response.headers
    except ClientError as error:
        console.print(error, style=WARNING)
        return False


@retry_lite
async def request_get(console: "ColorfulConsole", url: str, allow_redirects: bool = True, useragent=USERAGENT,
                      timeout=TIMEOUT,
                      **kwargs):
    try:
        async with ClientSession(headers={
            "User-Agent": useragent,
        }, timeout=ClientTimeout(connect=timeout), ) as session:
            async with session.get(url, allow_redirects=allow_redirects, **kwargs) as response:
                return await response.json()
    except ClientError as error:
        console.print(error, style=WARNING)
        return False
