# from typing import Callable
from typing import TYPE_CHECKING
from typing import Union

from src.interface.template import API
from src.translation import _

if TYPE_CHECKING:
    from src.config import Parameter
    from src.testers import Params

__all__ = ["Slides"]


class Slides(API):
    def __init__(
        self,
        params: Union["Parameter", "Params"],
        cookie: str = "",
        proxy: str = None,
        slides_id: str | list | tuple = ...,
    ):
        super().__init__(params, cookie, proxy)
        self.slides_id = slides_id
        self.api = f"{self.short_domain}web/api/v2/aweme/slidesinfo/"
        self.text = _("作品")

    async def run(self, *args, **kwargs):
        pass


async def test():
    from src.testers import Params

    async with Params() as params:
        i = Slides(
            params,
            slides_id="",
        )
        print(await i.run())


if __name__ == "__main__":
    from asyncio import run

    run(test())
