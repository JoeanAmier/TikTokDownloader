from typing import TYPE_CHECKING
from typing import Union

from src.interface.template import API
from src.testers import Params

if TYPE_CHECKING:
    from src.config import Parameter


class HashTag(API):
    def __init__(self,
                 params: Union["Parameter", Params],
                 cookie: str = None,
                 proxy: str = None,
                 *args,
                 **kwargs,
                 ):
        super().__init__(params, cookie, proxy, *args, **kwargs, )

    async def run(self, *args, **kwargs):
        pass
