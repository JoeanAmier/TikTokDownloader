from typing import TYPE_CHECKING
from typing import Union

from httpx import get

from src.custom import BLANK_HEADERS
from src.custom import wait
from src.testers import Params
from src.tools import Retry
from src.tools import capture_error_request
from src.translation import _

if TYPE_CHECKING:
    from src.config import Parameter
    from src.testers import Params


class DetailTikTokUnofficial:
    def __init__(
        self,
        params: Union["Parameter", "Params"],
        proxy: str = None,
        detail_id: str = ...,
        *args,
        **kwargs,
    ):
        self.headers = BLANK_HEADERS
        self.log = params.logger
        self.console = params.console
        self.api = "https://www.tikwm.com/api/"
        self.proxy = proxy
        self.max_retry = params.max_retry
        self.timeout = params.timeout
        self.detail_id = detail_id
        self.text = _("作品")

    async def run(
        self,
    ) -> dict:
        data = await self.request_data_get()
        data = self.check_response(data)
        return data

    @Retry.retry
    @capture_error_request
    async def request_data_get(
        self,
    ):
        response = get(
            self.api,
            params={"url": self.detail_id, "hd": "1"},
            headers=self.headers,
        )
        response.raise_for_status()
        await wait()
        return response.json()

    def check_response(
        self,
        data: dict,
    ):
        try:
            if data["msg"] == "success" and data["data"]:
                return data["data"]
            raise KeyError
        except KeyError:
            self.log.error(_("数据解析失败，请告知作者处理: {data}").format(data=data))


class DetailTikTokExtractor:
    def __str__(self): ...


async def test():
    async with Params() as params:
        i = DetailTikTokUnofficial(
            params,
            detail_id="",
        )
        print(await i.run())


if __name__ == "__main__":
    from asyncio import run

    run(test())
