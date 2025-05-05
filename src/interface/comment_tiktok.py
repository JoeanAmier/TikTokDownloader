from typing import TYPE_CHECKING
from typing import Union

from src.interface.comment import Comment, Reply
from src.interface.template import APITikTok
from src.translation import _

if TYPE_CHECKING:
    from src.config import Parameter
    from src.testers import Params


class CommentTikTok(Comment, APITikTok):
    def __init__(
        self,
        params: Union["Parameter", "Params"],
        cookie: str = "",
        proxy: str = None,
        detail_id: str = ...,
        pages: int = None,
        cursor=0,
        count=20,
        count_reply=3,
    ):
        super().__init__(
            params, cookie, proxy, detail_id, pages, cursor, count, count_reply
        )
        self.api = f"{self.domain}api/comment/list/"
        self.text = _("作品评论")

    def generate_params(
        self,
    ) -> dict:
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
    def __init__(
        self,
        params: Union["Parameter", "Params"],
        cookie: str = "",
        proxy: str = None,
        detail_id: str = "",
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
            detail_id,
            comment_id,
            pages,
            cursor,
            count,
            progress,
            task_id,
        )
        self.api = f"{self.domain}api/comment/list/reply/"

    def generate_params(
        self,
    ) -> dict:
        return self.params | {
            "comment_id": self.comment_id,
            "count": self.count,
            "cursor": self.cursor,
            "fromWeb": "1",
            "from_page": "video",
            "item_id": self.item_id,
        }


async def test():
    from src.testers import Params

    async with Params() as params:
        i = CommentTikTok(
            params,
            detail_id="",
        )
        print(await i.run())
        i = ReplyTikTok(
            params,
            detail_id="",
            comment_id="",
        )
        print(await i.run())


if __name__ == "__main__":
    from asyncio import run

    run(test())
