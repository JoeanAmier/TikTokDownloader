from typing import TYPE_CHECKING

from .template import API

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["Collects", "CollectsDetail", ]


class Collects(API):
    def __init__(self,
                 params: "Parameter",
                 cookie: str = None,
                 proxy: str = None,
                 cursor=0,
                 count=10,
                 *args,
                 **kwargs,
                 ):
        super().__init__(params, cookie, proxy, *args, **kwargs, )
        self.cursor = cursor
        self.count = count
        self.api = f"{self.domain}aweme/v1/web/collects/list/"
        self.text = "收藏夹数据"

    def generate_params(self, ) -> dict:
        return self.params | {
            "cursor": self.cursor,
            "count": self.count,
            "version_code": "170400",
            "version_name": "17.4.0",
        }

    async def run(self,
                  referer: str = "https://www.douyin.com/user/self?showTab=favorite_collection",
                  single_page=False,
                  data_key: str = "collects_list",
                  error_text="当前账号无收藏夹",
                  cursor="cursor",
                  has_more="has_more",
                  params: dict = None,
                  data: dict = None,
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
            error_text,
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


class CollectsDetail(Collects):
    def __init__(self,
                 params: "Parameter",
                 cookie: str = None,
                 proxy: str = None,
                 collects_id: str = "",
                 pages: int = None,
                 cursor=0,
                 count=10,
                 *args,
                 **kwargs,
                 ):
        super().__init__(params, cookie, proxy, cursor, count, *args, **kwargs, )
        self.collects_id = collects_id
        self.pages = pages or params.max_pages
        self.api = f"{self.domain}aweme/v1/web/collects/video/list/"
        self.text = "收藏夹作品数据"

    def generate_params(self, ) -> dict:
        return self.params | {
            "collects_id": self.collects_id,
            "cursor": self.cursor,
            "count": self.count,
            "version_code": "170400",
            "version_name": "17.4.0",
        }

    async def run(self,
                  referer: str = "https://www.douyin.com/user/self?showTab=favorite_collection",
                  single_page=False,
                  data_key: str = "aweme_list",
                  error_text="",
                  cursor="cursor",
                  has_more="has_more",
                  params: dict = None,
                  data: dict = None,
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
            error_text or f"收藏夹 {self.collects_id} 为空",
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


class CollectsMix(Collects):
    pass
