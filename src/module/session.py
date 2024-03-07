from typing import TYPE_CHECKING

from aiohttp import ClientSession
from aiohttp import ClientTimeout

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["Session"]


class Session:
    def __init__(self, params: "Parameter"):
        self.session = ClientSession(headers={
            "User-Agent": params.headers["User-Agent"],
        }, timeout=ClientTimeout(connect=params.timeout), )

    def start(self):
        return self.session

    async def close(self):
        await self.session.close()
