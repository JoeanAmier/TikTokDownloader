from json.decoder import JSONDecodeError
from typing import TYPE_CHECKING
from typing import Union

from httpx import HTTPStatusError
from httpx import NetworkError
from httpx import RequestError
from httpx import TimeoutException

if TYPE_CHECKING:
    from src.record import BaseLogger
    from src.record import LoggerManager

__all__ = ["capture_error_params", "capture_error_request", ]


def capture_error_params(function):
    async def inner(logger: Union["BaseLogger", "LoggerManager"], *args, **kwargs):
        try:
            return await function(logger, *args, **kwargs)
        except (
                JSONDecodeError,
                UnicodeDecodeError,
        ):
            logger.error("响应内容不是有效的 JSON 数据")
        except HTTPStatusError as e:
            logger.error(f"响应码异常：{e}")
        except NetworkError as e:
            logger.error(f"网络异常：{e}")
        except TimeoutException as e:
            logger.error(f"请求超时：{e}")
        except RequestError as e:
            logger.error(f"网络异常：{e}")
        return None

    return inner


def capture_error_request(function):
    async def inner(self, *args, **kwargs):
        try:
            return await function(self, *args, **kwargs)
        except (
                JSONDecodeError,
                UnicodeDecodeError
        ):
            self.log.error("响应内容不是有效的 JSON 数据")
        except HTTPStatusError as e:
            self.log.error(f"响应码异常：{e}")
        except NetworkError as e:
            self.log.error(f"网络异常：{e}")
        except TimeoutException as e:
            self.log.error(f"请求超时：{e}")
        except RequestError as e:
            self.log.error(f"网络异常：{e}")
        return None

    return inner
