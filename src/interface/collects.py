from typing import TYPE_CHECKING

from .template import API

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = [
    "Collects",
    "CollectsDetail",
    "CollectsSeries",
    "CollectsMix",
    "CollectsMusic",
]


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


class CollectsDetail(API):
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


class CollectsMix(API):
    def __init__(self,
                 params: "Parameter",
                 cookie: str = None,
                 proxy: str = None,
                 cursor=0,
                 count=12,
                 *args,
                 **kwargs,
                 ):
        super().__init__(params, cookie, proxy, *args, **kwargs, )
        self.cursor = cursor
        self.count = count
        self.api = f"{self.domain}aweme/v1/web/mix/listcollection/"
        self.text = "收藏合集数据"

    def generate_params(self, ) -> dict:
        return self.params | {
            "cursor": self.cursor,
            "count": self.count,
            "update_version_code": "170400",
            "version_code": "170400",
            "version_name": "17.4.0",
        }

    async def run(self,
                  referer: str = "https://www.douyin.com/user/self?showTab=favorite_collection",
                  single_page=False,
                  data_key: str = "mix_infos",
                  error_text="当前账号无收藏合集",
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


class CollectsSeries(CollectsMix):
    def __init__(self,
                 params: "Parameter",
                 cookie: str = None,
                 proxy: str = None,
                 cursor=0,
                 count=12,
                 *args,
                 **kwargs,
                 ):
        super().__init__(params, cookie, proxy, *args, **kwargs, )
        self.cursor = cursor
        self.count = count
        self.api = f"{self.domain}aweme/v1/web/series/collections/"
        self.text = "收藏短剧数据"

    async def run(self,
                  referer: str = "https://www.douyin.com/user/self?showTab=favorite_collection",
                  single_page=False,
                  data_key: str = "series_infos",
                  error_text="当前账号无收藏短剧",
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


class CollectsMusic(CollectsMix):
    def __init__(self,
                 params: "Parameter",
                 cookie: str = None,
                 proxy: str = None,
                 cursor=0,
                 count=20,
                 *args,
                 **kwargs,
                 ):
        super().__init__(params, cookie, proxy, *args, **kwargs, )
        self.cursor = cursor
        self.count = count
        self.api = f"{self.domain}aweme/v1/web/music/listcollection/"
        self.text = "收藏音乐数据"

    async def run(self,
                  referer: str = "https://www.douyin.com/user/self?showTab=favorite_collection",
                  single_page=False,
                  data_key: str = "mc_list",
                  error_text="当前账号无收藏音乐",
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
