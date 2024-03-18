from re import compile
from typing import TYPE_CHECKING

from .requester import Requester

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["Extractor"]


class Extractor:
    detail_url = compile("")

    def __init__(self, params: "Parameter"):
        self.requester = Requester(params)

    async def run(self, urls: str, type_="detail") -> list[str] | [bool, list[str]]:
        urls = await self.requester.run(urls)
        match type_:
            case "detail":
                return self.detail(urls)
            case "user":
                return self.user(urls)
            case "mix":
                return self.mix(urls)
            case "live":
                return self.live(urls)
        raise ValueError

    def detail(self, urls: list[str], ) -> list[str]:
        pass

    def user(self, urls: list[str], ) -> list[str]:
        pass

    def mix(self, urls: list[str], ) -> [bool, list[str]]:
        pass

    def live(self, urls: list[str], ) -> [bool, list[str]]:
        pass

    async def close(self):
        await self.requester.close()
