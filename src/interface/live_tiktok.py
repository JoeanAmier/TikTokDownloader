from typing import TYPE_CHECKING

from .template import APITikTok

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["LiveTikTok"]


class LiveTikTok(APITikTok):
    live_api = "https://webcast.us.tiktok.com/webcast/room/enter/"

    def __init__(self,
                 params: "Parameter",
                 cookie: str = None,
                 proxy: str = None,
                 room_id=None,
                 ):
        super().__init__(params, cookie, proxy, )
        self.black_headers = params.headers_download
        self.room_id = room_id

    async def run(self, *args, **kwargs, ) -> dict:
        return await self.with_room_id()

    async def with_room_id(self) -> dict:
        return await self.request_data(
            self.live_api,
            self.params,
            method="post",
            data=self.__generate_room_id_data(),
        )

    def __generate_room_id_data(self, ) -> dict:
        return {
            "enter_source": "others-others",
            "room_id": self.room_id,
        }
