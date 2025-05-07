from typing import TYPE_CHECKING, Callable, Coroutine, Type, Union

from src.extract import Extractor
from src.interface.template import API
from src.translation import _

if TYPE_CHECKING:
    from src.config import Parameter
    from src.testers import Params


class Comment(API):
    def __init__(
        self,
        params: Union["Parameter", "Params"],
        cookie: str = "",
        proxy: str = None,
        detail_id: str = ...,
        pages: int = None,
        cursor: int = 0,
        count: int = 20,
        count_reply: int = 3,
        reply: bool = False,
    ):
        super().__init__(params, cookie, proxy)
        self.params_object = params
        self.cookie = cookie
        self.proxy = proxy
        self.item_id = detail_id
        self.pages = pages or params.max_pages
        self.cursor = cursor
        self.count = count
        self.count_reply = count_reply
        self.api = f"{self.domain}aweme/v1/web/comment/list/"
        self.text = _("作品评论")
        self.current_page = []
        self.progress = None
        self.task_id = None
        self.reply = reply

    def generate_params(
        self,
    ) -> dict:
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

    async def run(
        self,
        referer: str = None,
        single_page=False,
        data_key: str = "comments",
        error_text="",
        cursor="cursor",
        has_more="has_more",
        params: Callable = lambda: {},
        data: Callable = lambda: {},
        method="GET",
        headers: dict = None,
        *args,
        **kwargs,
    ) -> list[dict]:
        return await super().run(
            referer,
            single_page,
            data_key,
            error_text=error_text
            or _("作品 {item_id} 无评论").format(item_id=self.item_id),
            cursor=cursor,
            has_more=has_more,
            data=data,
            params=params,
            method=method,
            headers=headers,
            callback=self.run_reply,
            *args,
            **kwargs,
        )

    async def run_batch(
        self,
        data_key: str = "comments",
        error_text="",
        cursor="cursor",
        has_more="has_more",
        params: Callable = lambda: {},
        data: Callable = lambda: {},
        method="GET",
        headers: dict = None,
        callback: Type[Coroutine] = None,
        *args,
        **kwargs,
    ):
        with self.progress_object() as self.progress:
            self.task_id = self.progress.add_task(
                _("正在获取{text}数据").format(text=self.text),
                total=None,
            )
            await self.update_progress(
                data_key,
                error_text,
                cursor,
                has_more,
                params,
                data,
                method,
                headers,
                callback,
                *args,
                **kwargs,
            )

    async def update_progress(
        self,
        data_key: str = "comments",
        error_text="",
        cursor="cursor",
        has_more="has_more",
        params: Callable = lambda: {},
        data: Callable = lambda: {},
        method="GET",
        headers: dict = None,
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
                *args,
                **kwargs,
            )
            self.pages -= 1
            if callback:
                await callback()

    async def run_reply(
        self,
    ):
        if not self.reply:
            return
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

    def check_response(
        self,
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
            self.log.error(
                _("数据解析失败，请告知作者处理: {data}").format(data=data_dict)
            )
            self.finished = True


class Reply(Comment):
    def __init__(
        self,
        params: Union["Parameter", "Params"],
        cookie: str = "",
        proxy: str = None,
        detail_id: str = ...,
        comment_id: str = ...,
        pages: int = None,
        cursor=0,
        count=3,
        progress=None,
        task_id=None,
    ):
        super().__init__(
            params,
            cookie,
            proxy,
        )
        self.item_id = detail_id
        self.comment_id = comment_id
        self.pages = pages or params.max_pages
        self.cursor = cursor
        self.count = count
        self.api = f"{self.domain}aweme/v1/web/comment/list/reply/"
        self.text = _("作品评论回复")
        self.progress = progress
        self.task_id = task_id

    def generate_params(
        self,
    ) -> dict:
        return self.params | {
            "item_id": self.item_id,
            "comment_id": self.comment_id,
            "cut_version": "1",
            "cursor": self.cursor,
            "count": self.count,
            "item_type": "0",
            "version_code": "170400",
            "version_name": "17.4.0",
            "support_h265": "0",
            "support_dash": "0",
        }

    async def run(
        self,
        referer: str = None,
        single_page=False,
        data_key: str = "comments",
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
        return await super(Comment, self).run(
            referer,
            single_page=single_page,
            data_key=data_key,
            error_text=error_text
            or _("评论 {comment_id} 无回复").format(comment_id=self.comment_id),
            cursor=cursor,
            has_more=has_more,
            params=params,
            data=data,
            method=method,
            headers=headers,
            *args,
            **kwargs,
        )

    async def run_batch(
        self,
        data_key: str = "comments",
        error_text="",
        cursor="cursor",
        has_more="has_more",
        params: Callable = lambda: {},
        data: Callable = lambda: {},
        method="GET",
        headers: dict = None,
        callback: Type[Coroutine] = None,
        *args,
        **kwargs,
    ):
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
            callback,
            *args,
            **kwargs,
        )

    def check_response(
        self,
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


async def test():
    from src.testers import Params

    async with Params() as params:
        i = Comment(
            params,
            detail_id="",
        )
        print(await i.run())
        i = Reply(
            params,
            detail_id="",
            comment_id="",
        )
        print(await i.run())


if __name__ == "__main__":
    from asyncio import run

    run(test())
