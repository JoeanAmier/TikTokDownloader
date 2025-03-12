from time import strftime, localtime
from types import SimpleNamespace
from typing import TYPE_CHECKING
from typing import Union

from httpx import get

from src.custom import BLANK_HEADERS
from src.custom import wait
from src.extract import Extractor
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
        self.proxy = proxy or params.proxy_tiktok
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
            timeout=self.timeout,
            follow_redirects=True,
            verify=False,
            proxy=self.proxy,
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
    def __init__(self, params: "Parameter"):
        self.date_format = params.date_format
        self.cleaner = params.CLEANER

    def __clean_description(self, desc: str) -> str:
        return self.cleaner.clear_spaces(self.cleaner.filter(desc))

    def __format_date(
        self,
        data: int,
    ) -> str:
        return strftime(
            self.date_format,
            localtime(data or None),
        )

    def run(self, data: dict) -> dict:
        item = {}
        data = Extractor.generate_data_object(data)
        self.extract_detail_tiktok(item, data)
        self.extract_music_tiktok(item, data)
        self.extract_author_tiktok(item, data)
        self.extract_statistics_tiktok(item, data)
        return item

    def extract_detail_tiktok(
        self,
        item: dict,
        data: SimpleNamespace,
    ) -> None:
        item["id"] = Extractor.safe_extract(data, "id")
        item["desc"] = (
            self.__clean_description(Extractor.safe_extract(data, "title"))
            or item["id"]
        )
        item["create_time"] = self.__format_date(
            Extractor.safe_extract(data, "create_time")
        )
        item["type"] = _("视频")
        item["downloads"] = Extractor.safe_extract(data, "hdplay")
        item["dynamic_cover"] = Extractor.safe_extract(data, "ai_dynamic_cover")
        item["static_cover"] = Extractor.safe_extract(data, "origin_cover")

    def extract_author_tiktok(
        self,
        item: dict,
        data: SimpleNamespace,
    ) -> None:
        item["uid"] = Extractor.safe_extract(data, "author.id")
        item["nickname"] = Extractor.safe_extract(data, "author.nickname")
        item["unique_id"] = Extractor.safe_extract(data, "author.unique_id")

    def extract_music_tiktok(
        self,
        item: dict,
        data: SimpleNamespace,
    ) -> None:
        item["music_author"] = Extractor.safe_extract(data, "music_info.author")
        item["music_title"] = Extractor.safe_extract(data, "music_info.title")
        item["music_url"] = Extractor.safe_extract(data, "music")

    @staticmethod
    def extract_statistics_tiktok(
        item: dict,
        data: SimpleNamespace,
    ) -> None:
        for i in Extractor.statistics_keys:
            item[i] = Extractor.safe_extract(
                data,
                i,
                -1,
            )


async def test():
    async with Params() as params:
        i = DetailTikTokUnofficial(
            params,
            detail_id="",
        )
        if data := await i.run():
            print(DetailTikTokExtractor(params).run(data))


if __name__ == "__main__":
    from asyncio import run

    run(test())
