from json.decoder import JSONDecodeError
from ssl import SSLError
from typing import TYPE_CHECKING, Union

from httpx import HTTPStatusError, NetworkError, RequestError, TimeoutException

from ..translation import _

if TYPE_CHECKING:
    from ..record import BaseLogger, LoggerManager

__all__ = [
    "capture_error_params",
    "capture_error_request",
]


def capture_error_params(function):
    async def inner(logger: Union["BaseLogger", "LoggerManager"], *args, **kwargs):
        try:
            return await function(logger, *args, **kwargs)
        except (
            JSONDecodeError,
            UnicodeDecodeError,
        ):
            logger.error(_("响应内容不是有效的 JSON 数据"))
        except HTTPStatusError as e:
            logger.error(_("响应码异常：{error}").format(error=e))
        except NetworkError as e:
            logger.error(_("网络异常：{error}").format(error=e))
        except TimeoutException as e:
            logger.error(_("请求超时：{error}").format(error=e))
        except (
            RequestError,
            SSLError,
        ) as e:
            logger.error(_("网络异常：{error}").format(error=e))
        return None

    return inner


def capture_error_request(function):
    async def inner(self, *args, **kwargs):
        try:
            return await function(self, *args, **kwargs)
        except (JSONDecodeError, UnicodeDecodeError):
            self.log.error(_("响应内容不是有效的 JSON 数据，请尝试更新 Cookie！"))
        except HTTPStatusError as e:
            self.log.error(_("响应码异常：{error}").format(error=e))
        except NetworkError as e:
            self.log.error(_("网络异常：{error}").format(error=e))
        except TimeoutException as e:
            self.log.error(_("请求超时：{error}").format(error=e))
        except (
            RequestError,
            SSLError,
        ) as e:
            self.log.error(_("网络异常：{error}").format(error=e))
        return None

    return inner
