from typing import Coroutine, Type
from typing import TYPE_CHECKING

from src.extract import Extractor
from .template import API

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["Comment", "Reply", ]


class Comment(API):
    def __init__(self,
                 params: "Parameter",
                 cookie: str | dict = None,
                 proxy: str = None,
                 item_id: str = "",
                 pages: int = None,
                 cursor=0,
                 count=20,
                 count_reply=3,
                 ):
        super().__init__(params, cookie, proxy, )
        self.params_object = params
        self.cookie = cookie
        self.proxy = proxy
        self.item_id = item_id
        self.pages = pages or params.max_pages
        self.cursor = cursor
        self.count = count
        self.count_reply = count_reply
        self.api = f"{self.domain}aweme/v1/web/comment/list/"
        self.text = "作品评论数据"
        self.current_page = []
        self.progress = None
        self.task_id = None

    def generate_params(self, ) -> dict:
        return self.params | {
            "aweme_id": self.item_id,
            "cursor": self.cursor,
            "count": self.count,
            "item_type": "0",
            "insert_ids": "",
            "whale_cut_token": "",
            "cut_version": "1",
            "rcFT": "",
            "version_code": "170400",
            "version_name": "17.4.0",
        }

    async def run(self,
                  referer: str = None,
                  single_page=False,
                  data_key: str = "comments",
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
                  ) -> list[dict]:
        return await super().run(
            referer,
            single_page,
            data_key,
            error_text=error_text or f"作品 {self.item_id} 无评论",
            cursor=cursor,
            has_more=has_more,
            data=data,
            method=method,
            headers=headers,
            proxy=proxy,
            callback=self.run_reply,
            *args,
            **kwargs,
        )

    async def run_batch(self,
                        data_key: str = "comments",
                        error_text="",
                        cursor="cursor",
                        has_more="has_more",
                        params: dict = None,
                        data: dict = None,
                        method="get",
                        headers: dict = None,
                        proxy: str = None,
                        callback: Type[Coroutine] = None,
                        *args,
                        **kwargs, ):
        with self.progress_object() as self.progress:
            self.task_id = self.progress.add_task(
                f"正在获取{self.text}", total=None)
            await self.update_progress(
                data_key,
                error_text,
                cursor,
                has_more,
                params,
                data,
                method,
                headers,
                proxy,
                callback,
                *args,
                **kwargs,
            )

    async def update_progress(self,
                              data_key: str = "comments",
                              error_text="",
                              cursor="cursor",
                              has_more="has_more",
                              params: dict = None,
                              data: dict = None,
                              method="get",
                              headers: dict = None,
                              proxy: str = None,
                              callback: Type[Coroutine] = None,
                              *args,
                              **kwargs,
                              ):
        while not self.finished and self.pages > 0:
            self.progress.update(self.task_id)
            await self.run_single(
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
            self.pages -= 1
            if callback:
                await callback()
            # TODO: 调试代码，待注释
            break

    async def run_reply(self, ):
        reply_ids = Extractor.extract_reply_ids(self.current_page)
        for reply_id in reply_ids:
            reply = Reply(
                self.params_object,
                self.cookie,
                self.proxy,
                self.item_id,
                reply_id,
                self.pages,
                cursor=0,
                count=self.count_reply,
                progress=self.progress,
                task_id=self.task_id,
            )
            self.response.extend(await reply.run())
            if (p := reply.pages) > 1:
                self.pages = p
            else:
                break
            # TODO: 调试代码，待注释
            break

    def check_response(self,
                       data_dict: dict,
                       data_key: str,
                       error_text="",
                       cursor="cursor",
                       has_more="has_more",
                       *args,
                       **kwargs,
                       ):
        try:
            if not (d := data_dict[data_key]):
                self.log.info(error_text)
                self.finished = True
            else:
                self.cursor = data_dict[cursor]
                self.current_page = d
                self.append_response(d)
                self.finished = not data_dict[has_more]
        except KeyError:
            self.log.error(f"数据解析失败，请告知作者处理: {data_dict}")
            self.finished = True


class Reply(Comment):
    def __init__(self,
                 params: "Parameter",
                 cookie: str | dict = None,
                 proxy: str = None,
                 item_id: str = "",
                 comment_id: str = "",
                 pages: int = None,
                 cursor=0,
                 count=3,
                 progress=None,
                 task_id=None,
                 ):
        super().__init__(params, cookie, proxy, )
        self.item_id = item_id
        self.comment_id = comment_id
        self.pages = pages or params.max_pages
        self.cursor = cursor
        self.count = count
        self.api = f"{self.domain}aweme/v1/web/comment/list/reply/"
        self.text = "作品评论回复数据"
        self.progress = progress
        self.task_id = task_id

    def generate_params(self, ) -> dict:
        return self.params | {
            "item_id": self.item_id,
            "comment_id": self.comment_id,
            "cut_version": "1",
            "cursor": self.cursor,
            "count": self.count,
            "item_type": "0",
            "version_code": "170400",
            "version_name": "17.4.0",
        }

    async def run(self,
                  referer: str = None,
                  single_page=False,
                  data_key: str = "comments",
                  error_text="",
                  cursor="cursor",
                  has_more="has_more",
                  params: dict = None,
                  data: dict = None,
                  method="get",
                  headers: dict = None,
                  proxy: str = None,
                  *args, **kwargs, ):
        return await super(Comment, self).run(
            referer,
            single_page=single_page,
            data_key=data_key,
            error_text=error_text or f"评论 {self.comment_id} 无回复",
            cursor=cursor,
            has_more=has_more,
            params=params,
            data=data,
            method=method,
            headers=headers,
            proxy=proxy,
            *args,
            **kwargs,
        )

    async def run_batch(self,
                        data_key: str = "comments",
                        error_text="",
                        cursor="cursor",
                        has_more="has_more",
                        params: dict = None,
                        data: dict = None,
                        method="get",
                        headers: dict = None,
                        proxy: str = None,
                        callback: Type[Coroutine] = None,
                        *args,
                        **kwargs, ):
        if not self.progress:
            return await super(Comment, self).run_batch(
                data_key,
                error_text,
                cursor,
                has_more,
                params,
                data,
                method,
                headers,
                proxy,
                callback,
                *args,
                **kwargs,
            )
        return await self.update_progress(
            data_key,
            error_text,
            cursor,
            has_more,
            params,
            data,
            method,
            headers,
            proxy,
            callback,
            *args,
            **kwargs,
        )

    def check_response(self,
                       data_dict: dict,
                       data_key: str,
                       error_text="",
                       cursor="cursor",
                       has_more="has_more",
                       *args,
                       **kwargs,
                       ):
        return super(Comment, self).check_response(
            data_dict,
            data_key,
            error_text,
            cursor,
            has_more,
            *args,
            **kwargs,
        )
