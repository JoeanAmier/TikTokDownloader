from typing import Coroutine
from typing import TYPE_CHECKING
from typing import Type

from .account import Account
# from src.extract import Extractor
# from src.tools import timestamp
from .template import APITikTok

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["AccountTikTok"]


class AccountTikTok(Account, APITikTok, ):
    post_api = f"{APITikTok.domain}api/post/item_list/"
    favorite_api = f"{APITikTok.domain}api/favorite/item_list/"

    def __init__(self,
                 params: "Parameter",
                 cookie: str | dict = None,
                 proxy: str = None,
                 sec_user_id: str = "",
                 tab="post",
                 earliest="",
                 latest="",
                 pages: int = None,
                 cursor=0,
                 count=35,
                 *args,
                 **kwargs,
                 ):
        super().__init__(
            params,
            cookie,
            proxy,
            sec_user_id,
            tab,
            earliest,
            latest,
            pages,
            cursor,
            count,
            *args,
            **kwargs,
        )
        # self.info = Info(params, sec_user_id, cookie, proxy, )

    async def run(self,
                  referer: str = None,
                  single_page=False,
                  data_key: str = "itemList",
                  error_text="",
                  cursor="cursor",
                  has_more="hasMore",
                  params: dict = None,
                  data: dict = None,
                  method="get",
                  headers: dict = None,
                  proxy: str = None,
                  *args,
                  **kwargs,
                  ):
        self.set_referer(referer)
        match single_page:
            case True:
                await self.run_single(
                    data_key,
                    error_text=error_text or f"获取{self.text}失败",
                    cursor=cursor,
                    has_more=has_more,
                    params=params or self.generate_params(self.favorite),
                    data=data,
                    method=method,
                    headers=headers,
                    proxy=proxy,
                    *args,
                    **kwargs,
                )
                return self.response
            case False:
                await self.run_batch(
                    data_key,
                    error_text=error_text or f"获取{self.text}失败",
                    cursor=cursor,
                    has_more=has_more,
                    params=params or self.generate_params(self.favorite),
                    data=data,
                    method=method,
                    headers=headers,
                    proxy=proxy,
                    *args,
                    **kwargs,
                )
                return self.response, self.earliest, self.latest
        raise ValueError

    async def run_batch(self,
                        data_key: str = "itemList",
                        error_text="",
                        cursor="cursor",
                        has_more="hasMore",
                        params: dict = None,
                        data: dict = None,
                        method="get",
                        headers: dict = None,
                        proxy: str = None,
                        callback: Type[Coroutine] = None,
                        *args,
                        **kwargs,
                        ):
        await super().run_batch(
            data_key=data_key,
            error_text=error_text or f"获取{self.text}失败",
            cursor=cursor,
            has_more=has_more,
            params=params,
            data=data,
            method=method,
            headers=headers,
            proxy=proxy,
            callback=callback,
            *args,
            **kwargs,
        )

    # async def favorite_mode(self):
    #     if not self.favorite:
    #         return
    #     info = Extractor.get_user_info(await self.info.run())
    #     if self.sec_user_id != (s := info.get("sec_uid")):
    #         self.log.error(
    #             f"sec_user_id {self.sec_user_id} 与 {s} 不一致")
    #         self.__generate_temp_data()
    #     else:
    #         self.response.append({"author": info})

    def generate_favorite_params(self) -> dict:
        return self.generate_post_params()

    def generate_post_params(self) -> dict:
        return self.params | {
            "secUid": self.sec_user_id,
            "count": self.count,
            "cursor": self.cursor,
            "coverFormat": "2"
        }
