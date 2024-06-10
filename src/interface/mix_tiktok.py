from typing import Callable
from typing import TYPE_CHECKING

from .template import APITikTok

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["MixTikTok"]


class MixTikTok(APITikTok):
    def __init__(self,
                 params: "Parameter",
                 cookie: str = None,
                 proxy: str = None,
                 mix_title: str = None,
                 mix_id: str = None,
                 detail_id: str = None,
                 cursor=0,
                 count=30,
                 *args,
                 **kwargs,
                 ):
        super().__init__(params, cookie, proxy, *args, **kwargs, )
        self.mix_title = mix_title
        self.mix_id = mix_id
        self.detail_id = detail_id  # 未使用
        self.cursor = cursor
        self.count = count
        self.api = f"{self.domain}api/mix/item_list/"
        self.text = "合集作品数据"

    def generate_params(self, ) -> dict:
        return self.params | {
            "count": self.count,
            "cursor": self.cursor,
            "mixId": self.mix_id,
        }

    async def run(self,
                  referer: str = None,
                  single_page=False,
                  data_key: str = "itemList",
                  error_text="",
                  cursor="cursor",
                  has_more="hasMore",
                  params: Callable = lambda: {},
                  data: Callable = lambda: {},
                  method="get",
                  headers: dict = None,
                  proxy: str = None,
                  *args,
                  **kwargs,
                  ):
        return await super().run(
            referer,
            single_page,
            data_key,
            error_text or f"获取{self.text}失败",
            cursor,
            has_more,
            params,
            data,
            method,
            headers,
            proxy,
            *args,
            **kwargs,
        )
