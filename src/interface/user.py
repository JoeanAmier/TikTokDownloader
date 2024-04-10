from typing import TYPE_CHECKING

from src.custom import WARNING
from .template import API

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["User"]


class User(API):
    def __init__(self,
                 params: "Parameter",
                 cookie: str = None,
                 proxy: str = None,
                 *args,
                 **kwargs,
                 ):
        super().__init__(params, cookie, proxy, *args, **kwargs, )

    async def run(self, *args, **kwargs):
        self.console.print("该功能暂不开放！", style=WARNING)
