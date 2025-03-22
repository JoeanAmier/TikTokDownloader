from typing import TYPE_CHECKING, Callable, Union

from src.interface.collection import Collection
from src.interface.template import API
from src.translation import _

if TYPE_CHECKING:
    from src.config import Parameter
    from src.testers import Params


class Collects(API):
    def __init__(
        self,
        params: Union["Parameter", "Params"],
        cookie: str = "",
        proxy: str = None,
        cursor=0,
        count=10,
        *args,
        **kwargs,
    ):
        super().__init__(params, cookie, proxy, *args, **kwargs)
        self.cursor = cursor
        self.count = count
        self.api = f"{self.domain}aweme/v1/web/collects/list/"
        self.text = _("收藏夹")

    def generate_params(
        self,
    ) -> dict:
        return self.params | {
            "cursor": self.cursor,
            "count": self.count,
            "version_code": "170400",
            "version_name": "17.4.0",
        }

    async def run(
        self,
        referer: str = "https://www.douyin.com/user/self?showTab=favorite_collection",
        single_page=False,
        data_key: str = "collects_list",
        error_text="",
        cursor="cursor",
        has_more="has_more",
        params: Callable = lambda: {},
        data: Callable = lambda: {},
        method="GET",
        headers: dict = None,
        *args,
        **kwargs,
    ):
        return await super().run(
            referer,
            single_page,
            data_key,
            error_text or _("当前账号无收藏夹"),
            cursor,
            has_more,
            params,
            data,
            method,
            headers,
            *args,
            **kwargs,
        )


class CollectsDetail(Collection, API):
    def __init__(
        self,
        params: Union["Parameter", "Params"],
        cookie: str = "",
        proxy: str = None,
        collects_id: str = ...,
        pages: int = None,
        cursor=0,
        count=10,
        *args,
        **kwargs,
    ):
        super().__init__(params, cookie, proxy, None, *args, **kwargs)
        self.collects_id = collects_id
        self.pages = pages or params.max_pages
        self.api = f"{self.domain}aweme/v1/web/collects/video/list/"
        self.cursor = cursor
        self.count = count
        self.text = _("收藏夹作品")

    def generate_params(
        self,
    ) -> dict:
        return self.params | {
            "collects_id": self.collects_id,
            "cursor": self.cursor,
            "count": self.count,
            "version_code": "170400",
            "version_name": "17.4.0",
        }

    async def run(
        self,
        referer: str = "https://www.douyin.com/user/self?showTab=favorite_collection",
        single_page=False,
        data_key: str = "aweme_list",
        error_text="",
        cursor="cursor",
        has_more="has_more",
        params: Callable = lambda: {},
        data: Callable = lambda: {},
        method="GET",
        headers: dict = None,
        *args,
        **kwargs,
    ):
        await super(Collection, self).run(
            referer,
            single_page,
            data_key,
            error_text
            or _("收藏夹 {collects_id} 为空").format(collects_id=self.collects_id),
            cursor,
            has_more,
            params,
            data,
            method,
            headers,
            *args,
            **kwargs,
        )
        return self.response


class CollectsMix(API):
    def __init__(
        self,
        params: Union["Parameter", "Params"],
        cookie: str = "",
        proxy: str = None,
        cursor=0,
        count=12,
        *args,
        **kwargs,
    ):
        super().__init__(params, cookie, proxy, *args, **kwargs)
        self.cursor = cursor
        self.count = count
        self.api = f"{self.domain}aweme/v1/web/mix/listcollection/"
        self.text = _("收藏合集")

    def generate_params(
        self,
    ) -> dict:
        return self.params | {
            "cursor": self.cursor,
            "count": self.count,
            "version_code": "170400",
            "version_name": "17.4.0",
        }

    async def run(
        self,
        referer: str = "https://www.douyin.com/user/self?showTab=favorite_collection",
        single_page=False,
        data_key: str = "mix_infos",
        error_text="",
        cursor="cursor",
        has_more="has_more",
        params: Callable = lambda: {},
        data: Callable = lambda: {},
        method="GET",
        headers: dict = None,
        proxy: str = None,
        *args,
        **kwargs,
    ):
        return await super().run(
            referer,
            single_page,
            data_key,
            error_text or _("当前账号无收藏合集"),
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
    def __init__(
        self,
        params: Union["Parameter", "Params"],
        cookie: str = "",
        proxy: str = None,
        cursor=0,
        count=12,
        *args,
        **kwargs,
    ):
        super().__init__(
            params,
            cookie,
            proxy,
            *args,
            **kwargs,
        )
        self.cursor = cursor
        self.count = count
        self.api = f"{self.domain}aweme/v1/web/series/collections/"
        self.text = _("收藏短剧")

    async def run(
        self,
        referer: str = "https://www.douyin.com/user/self?showTab=favorite_collection",
        single_page=False,
        data_key: str = "series_infos",
        error_text="",
        cursor="cursor",
        has_more="has_more",
        params: Callable = lambda: {},
        data: Callable = lambda: {},
        method="GET",
        headers: dict = None,
        *args,
        **kwargs,
    ):
        return await super().run(
            referer,
            single_page,
            data_key,
            error_text or _("当前账号无收藏短剧"),
            cursor,
            has_more,
            params,
            data,
            method,
            headers,
            *args,
            **kwargs,
        )


class CollectsMusic(CollectsMix):
    def __init__(
        self,
        params: Union["Parameter", "Params"],
        cookie: str = "",
        proxy: str = None,
        cursor=0,
        count=20,
        *args,
        **kwargs,
    ):
        super().__init__(
            params,
            cookie,
            proxy,
            *args,
            **kwargs,
        )
        self.cursor = cursor
        self.count = count
        self.api = f"{self.domain}aweme/v1/web/music/listcollection/"
        self.text = _("收藏音乐")

    async def run(
        self,
        referer: str = "https://www.douyin.com/user/self?showTab=favorite_collection",
        single_page=False,
        data_key: str = "mc_list",
        error_text="",
        cursor="cursor",
        has_more="has_more",
        params: Callable = lambda: {},
        data: Callable = lambda: {},
        method="GET",
        headers: dict = None,
        *args,
        **kwargs,
    ):
        return await super().run(
            referer,
            single_page,
            data_key,
            error_text or _("当前账号无收藏音乐"),
            cursor,
            has_more,
            params,
            data,
            method,
            headers,
            *args,
            **kwargs,
        )


async def test():
    from src.testers import Params

    async with Params() as params:
        c = Collects(
            params,
        )
        print(await c.run())
        c = CollectsDetail(params, collects_id="")
        print(await c.run())
        c = CollectsMix(
            params,
        )
        print(await c.run())
        c = CollectsMusic(
            params,
        )
        print(await c.run())
        c = CollectsSeries(
            params,
        )
        print(await c.run())


if __name__ == "__main__":
    from asyncio import run

    run(test())
