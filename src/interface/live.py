from typing import TYPE_CHECKING

from .template import API

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["Live"]


class Live(API):
    live_api = "https://live.douyin.com/webcast/room/web/enter/"
    live_api_share = "https://webcast.amemv.com/webcast/room/reflow/info/"

    def __init__(self,
                 params: "Parameter",
                 cookie: str = None,
                 proxy: str = None,
                 web_rid=None,
                 room_id=None,
                 sec_user_id=None,
                 ):
        super().__init__(params, cookie, proxy, )
        self.black_headers = params.headers_download
        self.web_rid = web_rid
        self.room_id = room_id
        self.sec_user_id = sec_user_id

    async def run(self, *args, **kwargs, ) -> dict:
        if self.web_rid:
            return await self.with_web_rid()
        elif self.room_id and self.sec_user_id:
            return await self.with_room_id()
        else:
            raise ValueError(
                "web_rid or room_id and sec_user_id must be provided")

    async def with_web_rid(self) -> dict:
        self.set_referer("https://live.douyin.com/")
        params = {
            "aid": "6383",
            "app_name": "douyin_web",
            "live_id": "1",
            "device_platform": "web",
            "language": "zh-CN",
            "enter_from": "link_share",
            "cookie_enabled": "true",
            "screen_width": "1536",
            "screen_height": "864",
            "browser_language": "zh-CN",
            "browser_platform": "Win32",
            "browser_name": "Edge",
            "browser_version": "123.0.0.0",
            "web_rid": self.web_rid,
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
            "version_code": "99.99.99",
            "app_id": "1128",
        }
        return await self.request_data(
            self.live_api_share,
            params,
            headers=self.black_headers,
            number=12,
        )
