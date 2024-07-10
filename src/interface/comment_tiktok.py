from asyncio import run
from typing import TYPE_CHECKING
from typing import Union

from src.interface.comment import Comment, Reply
from src.interface.template import APITikTok
from src.testers import Params

if TYPE_CHECKING:
    from src.config import Parameter


class CommentTikTok(Comment, APITikTok):
    def __init__(self,
                 params: Union["Parameter", Params],
                 cookie: str | dict = None,
                 proxy: str = None,
                 item_id: str = ...,
                 pages: int = None,
                 cursor=0,
                 count=20,
                 count_reply=3,
                 ):
        super().__init__(params, cookie, proxy, item_id, pages, cursor, count, count_reply)
        self.api = f"{self.domain}api/comment/list/"

    def generate_params(self, ) -> dict:
        return self.params | {
            "aweme_id": self.item_id,
            "count": self.count,
            "cursor": self.cursor,
            "enter_from": "tiktok_web",
            "is_non_personalized": "false",
            "fromWeb": "1",
            "from_page": "video",
        }


class ReplyTikTok(Reply, CommentTikTok, APITikTok):
    def __init__(self,
                 params: Union["Parameter", Params],
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
        super().__init__(
            params,
            cookie,
            proxy,
            item_id,
            comment_id,
            pages,
            cursor,
            count,
            progress,
            task_id)
        self.api = f"{self.domain}api/comment/list/reply/"

    def generate_params(self, ) -> dict:
        return self.params | {
            "comment_id": self.comment_id,
            "count": self.count,
            "cursor": self.cursor,
            "fromWeb": "1",
            "from_page": "video",
            "item_id": self.item_id,
        }


async def main():
    async with Params() as params:
        c = CommentTikTok(params, item_id="7360156187515456775", )
        print(await c.run())


if __name__ == "__main__":
    run(main())
