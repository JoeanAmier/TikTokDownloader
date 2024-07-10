# from typing import Callable
from typing import TYPE_CHECKING
from typing import Union

from src.interface.template import API
from src.testers import Params

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["Slides"]


class Slides(API):
    def __init__(self,
                 params: Union["Parameter", Params],
                 cookie: str = None,
                 proxy: str = None,
                 slides_id: str | list | tuple = ...,
                 ):
        super().__init__(params, cookie, proxy, )
        self.slides_id = slides_id
        self.api = f"{self.short_domain}web/api/v2/aweme/slidesinfo/"
        self.text = "作品数据"

    async def run(self, *args, **kwargs):
        pass
