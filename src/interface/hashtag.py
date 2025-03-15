from typing import TYPE_CHECKING
from typing import Union

from src.interface.template import API

# from src.translation import _

if TYPE_CHECKING:
    from src.config import Parameter
    from src.testers import Params


class HashTag(API):
    def __init__(
        self,
        params: Union["Parameter", "Params"],
        cookie: str = "",
        proxy: str = None,
        *args,
        **kwargs,
    ):
        super().__init__(params, cookie, proxy, *args, **kwargs)

    async def run(self, *args, **kwargs):
        pass


async def test():
    from src.testers import Params

    async with Params() as params:
        i = HashTag(
            params,
        )
        print(await i.run())


if __name__ == "__main__":
    from asyncio import run

    run(test())
