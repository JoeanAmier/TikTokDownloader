from typing import TYPE_CHECKING, Union

from src.interface.template import API
from src.tools import DownloaderError

if TYPE_CHECKING:
    from src.config import Parameter
    from src.testers import Params


class Live(API):
    live_api = "https://live.douyin.com/webcast/room/web/enter/"
    live_api_share = "https://webcast.amemv.com/webcast/room/reflow/info/"

    def __init__(
        self,
        params: Union["Parameter", "Params"],
        cookie: str = "",
        proxy: str = None,
        web_rid: str = ...,
        room_id: str = ...,
        sec_user_id: str = "",
    ):
        super().__init__(params, cookie, proxy)
        self.black_headers = params.headers_download
        self.web_rid = web_rid
        self.room_id = room_id
        self.sec_user_id = sec_user_id

    async def run(
        self,
        *args,
        **kwargs,
    ) -> dict:
        if isinstance(self.web_rid, str):
            return await self.with_web_rid()
        elif self.room_id:
            return await self.with_room_id()
        else:
            raise DownloaderError

    async def with_web_rid(self) -> dict:
        self.set_referer("https://live.douyin.com/")
        params = {  # TODO: 参数固定
            "aid": "6383",
            "app_name": "douyin_web",
            "live_id": "1",
            "device_platform": "web",
            "language": "zh-CN",
            "enter_from": "web_share_link",
            "cookie_enabled": "true",
            "screen_width": "1536",
            "screen_height": "864",
            "browser_language": "zh-CN",
            "browser_platform": "Win32",
            "browser_name": "Edge",
            "browser_version": "139.0.0.0",
            "web_rid": self.web_rid,
            # "room_id_str": "",
            "enter_source": "",
            "is_need_double_stream": "false",
            "insert_task_id": "",
            "live_reason": "",
        }
        return await self.request_data(
            self.live_api,
            params,
        )

    async def with_room_id(self) -> dict:
        params = {
            "type_id": "0",
            "live_id": "1",
            "room_id": self.room_id,
            "sec_user_id": self.sec_user_id,
            "app_id": "1128",
        }
        return await self.request_data(
            self.live_api_share,
            params,
            headers=self.black_headers,
        )


async def test():
    from src.testers import Params

    async with Params() as params:
        i = Live(
            params,
            room_id="",
        )
        print(await i.run())


if __name__ == "__main__":
    from asyncio import run

    run(test())
