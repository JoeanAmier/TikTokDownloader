from aiohttp import ClientError
from aiohttp import ContentTypeError

__all__ = ["capture_error_url", ]


def capture_error_url(function):
    async def inner(self, *args, **kwargs):
        try:
            return await function(self, *args, **kwargs)
        except (
                ClientError,
                ContentTypeError,
        ) as e:
            self.log.error(str(e))
            return None

    return inner
