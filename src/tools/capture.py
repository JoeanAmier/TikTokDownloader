from asyncio import TimeoutError
from typing import TYPE_CHECKING
from typing import Union

from aiohttp import ClientError
from aiohttp import ContentTypeError

if TYPE_CHECKING:
    from src.record import BaseLogger
    from src.record import LoggerManager

__all__ = ["capture_error_params", "capture_error_request", ]


def capture_error_params(function):
    async def inner(logger: Union["BaseLogger", "LoggerManager"], *args, **kwargs):
        try:
            return await function(logger, *args, **kwargs)
        except ClientError as e:
            logger.error(f"网络异常：{e}")
        except ContentTypeError as e:
            logger.error(f"响应内容异常：{e}")
        except TimeoutError as e:
            logger.error(f"请求超时：{e}")
        return None

    return inner


def capture_error_request(function):
    async def inner(self, *args, **kwargs):
        try:
            return await function(self, *args, **kwargs)
        except ClientError as e:
            self.log.error(f"网络异常：{e}")
        except ContentTypeError as e:
            self.log.error(f"响应内容异常：{e}")
        except TimeoutError as e:
            self.log.error(f"请求超时：{e}")
        return None

    return inner
