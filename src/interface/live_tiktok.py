from typing import TYPE_CHECKING
from typing import Union

from src.interface.template import APITikTok
from src.testers import Params

if TYPE_CHECKING:
    from ..config import Parameter


class LiveTikTok(APITikTok):
    live_api = "https://webcast.us.tiktok.com/webcast/room/enter/"

    def __init__(
            self,
            params: Union["Parameter", Params],
            cookie: str = None,
            proxy: str = None,
            room_id=...,
    ):
        super().__init__(
            params,
            cookie,
            proxy,
        )
        self.black_headers = params.headers_download
        self.room_id = room_id

    async def run(
            self,
            *args,
            **kwargs,
    ) -> dict:
        return await self.with_room_id()

    async def with_room_id(self) -> dict:
        return await self.request_data(
            self.live_api,
            self.params,
            method="POST",
            data=self.__generate_room_id_data(),
        )

    def __generate_room_id_data(
            self,
    ) -> dict:
        return {
            "enter_source": "others-others",
            "room_id": self.room_id,
        }


async def test():
    async with Params() as params:
        i = LiveTikTok(
            params,
            room_id="",
        )
        print(await i.run())


if __name__ == "__main__":
    from asyncio import run

    run(test())
