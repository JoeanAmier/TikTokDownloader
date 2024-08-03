from asyncio import run
from typing import Callable
from typing import TYPE_CHECKING
from typing import Union

from src.interface.template import API
from src.testers import Params

if TYPE_CHECKING:
    from src.config import Parameter


class Collection(API):
    def __init__(self,
                 params: Union["Parameter", Params],
                 cookie: str = None,
                 proxy: str = None,
                 sec_user_id: str = "",
                 count=10,
                 cursor=0,
                 pages: int = None,
                 *args,
                 **kwargs,
                 ):
        super().__init__(params, cookie, proxy, *args, **kwargs, )
        self.api = f"{self.domain}aweme/v1/web/aweme/listcollection/"
        self.text = "账号收藏作品数据"
        self.count = count
        self.cursor = cursor
        self.pages = pages or params.max_pages
        self.sec_user_id = sec_user_id

    async def run(self,
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
            error_text or f"获取{self.text}失败",
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

    def generate_params(self, ) -> dict:
        return self.params | {
            "publish_video_strategy_type": "2",
            "version_code": "170400",
            "version_name": "17.4.0",
        }

    def generate_data(self, ) -> dict:
        return {
            "count": self.count,
            "cursor": self.cursor,
        }

    async def request_data(self,
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

    # async def get_owner_data(self):
    #     if not any(self.response):
    #         return
    #     if self.sec_user_id and (
    #             info := Extractor.get_user_info(
    #                 await self.info.run())):
    #         self.response.append({"author": info})
    #     else:
    #         temp_data = timestamp()
    #         self.log.warning(
    #             f"owner_url 参数未设置 或者 获取账号数据失败，本次运行将临时使用 {temp_data} 作为账号昵称和 UID")
    #         temp_dict = {
    #             "author": {
    #                 "nickname": temp_data,
    #                 "uid": temp_data,
    #                 "sec_uid": self.sec_user_id,
    #             }
    #         }
    #         self.response.append(temp_dict)


async def main():
    async with Params() as params:
        c = Collection(params, pages=2, )
        print(await c.run())


if __name__ == "__main__":
    run(main())
