from typing import TYPE_CHECKING, Callable, Union

from src.interface.template import API
from src.translation import _

if TYPE_CHECKING:
    from src.config import Parameter
    from src.testers import Params


class Collection(API):
    def __init__(
        self,
        params: Union["Parameter", "Params"],
        cookie: str = "",
        proxy: str = None,
        sec_user_id: str = "",
        count=10,
        cursor=0,
        pages: int = None,
        *args,
        **kwargs,
    ):
        super().__init__(params, cookie, proxy, *args, **kwargs)
        self.api = f"{self.domain}aweme/v1/web/aweme/listcollection/"
        self.text = _("账号收藏作品")
        self.count = count
        self.cursor = cursor
        self.pages = pages or params.max_pages
        self.sec_user_id = sec_user_id

    async def run(
        self,
        referer: str = "",
        single_page=False,
        data_key: str = "aweme_list",
        error_text="",
        cursor="cursor",
        has_more="has_more",
        params: Callable = lambda: {},
        data: Callable = lambda: {},
        method="POST",
        headers: dict = None,
        *args,
        **kwargs,
    ):
        await super().run(
            referer or f"{self.domain}user/self?showTab=favorite_collection",
            single_page,
            data_key,
            error_text,
            cursor,
            has_more,
            params,
            data,
            method,
            headers,
            *args,
            **kwargs,
        )
        # await self.get_owner_data()
        return self.response

    def generate_params(
        self,
    ) -> dict:
        return self.params | {
            "publish_video_strategy_type": "2",
            "version_code": "170400",
            "version_name": "17.4.0",
        }

    def generate_data(
        self,
    ) -> dict:
        return {
            "count": self.count,
            "cursor": self.cursor,
        }

    async def request_data(
        self,
        url: str,
        params: dict = None,
        data: dict = None,
        method="GET",
        headers: dict = None,
        encryption="GET",
        finished=False,
        *args,
        **kwargs,
    ):
        return await super().request_data(
            url,
            params,
            data,
            method,
            headers,
            encryption,
            finished,
            *args,
            **kwargs,
        )


async def test():
    from src.testers import Params

    async with Params() as params:
        c = Collection(
            params,
            pages=1,
        )
        print(await c.run())


if __name__ == "__main__":
    from asyncio import run

    run(test())
