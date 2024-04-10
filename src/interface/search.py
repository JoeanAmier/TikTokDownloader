from types import SimpleNamespace
from typing import TYPE_CHECKING

from src.custom import WARNING
from .template import API

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["Search"]


class Search(API):
    search_params = (
        SimpleNamespace(
            api="https://www.douyin.com/aweme/v1/web/general/search/single/",
            count=15,
            channel="aweme_general",
            type="general",
        ),
        SimpleNamespace(
            api="https://www.douyin.com/aweme/v1/web/search/item/",
            count=20,
            channel="aweme_video_web",
            type="video",
        ),
        SimpleNamespace(
            api="https://www.douyin.com/aweme/v1/web/discover/search/",
            count=12,
            channel="aweme_user_web",
            type="user",
        ),
        SimpleNamespace(
            api="https://www.douyin.com/aweme/v1/web/live/search/",
            count=15,
            channel="aweme_live",
            type="live",
        ),
    )

    def __init__(self,
                 params: "Parameter",
                 cookie: str = None,
                 proxy: str = None,
                 *args,
                 **kwargs,
                 ):
        super().__init__(params, cookie, proxy, *args, **kwargs, )

    def generate_params(self, space: SimpleNamespace, *args, **kwargs) -> dict:
        return self.params

    async def run(self, *args, **kwargs):
        self.console.print("该功能暂不开放！", style=WARNING)
        return self.response
