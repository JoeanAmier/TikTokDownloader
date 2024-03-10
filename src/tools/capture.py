from aiohttp import ClientError
from aiohttp import ContentTypeError

__all__ = ["capture_error_params", ]


def capture_error_params(function):
    async def inner(*args, **kwargs):
        try:
            return await function(*args, **kwargs)
        except (
                ClientError,
                ContentTypeError,
        ) as e:
            if log := kwargs.get("logger"):
                log.error(str(e))
            return None

    return inner
