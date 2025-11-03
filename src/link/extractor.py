from re import compile
from typing import TYPE_CHECKING, Union
from urllib.parse import parse_qs, unquote, urlparse

from .requester import Requester

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["Extractor", "ExtractorTikTok"]


class Extractor:
    WEB_RID = compile(r"\\\"webRid\\\":\\\"(\d+?)\\\"")

    account_link = compile(
        r"\S*?https://www\.douyin\.com/user/([A-Za-z0-9_-]+)(?:\S*?\bmodal_id=(\d{19}))?"
    )  # 账号主页链接
    account_share = compile(
        r"\S*?https://www\.iesdouyin\.com/share/user/(\S*?)\?\S*?"  # 账号主页分享链接
    )

    detail_id = compile(r"\b(\d{19})\b")  # 作品 ID
    detail_link = compile(
        r"\S*?https://www\.douyin\.com/(?:video|note|slides)/([0-9]{19})\S*?"
    )  # 作品链接
    detail_share = compile(
        r"\S*?https://www\.iesdouyin\.com/share/(?:video|note|slides)/([0-9]{19})/\S*?"
    )  # 作品分享链接
    detail_search = compile(
        r"\S*?https://www\.douyin\.com/search/\S+?modal_id=(\d{19})\S*?"
    )  # 搜索作品链接
    detail_discover = compile(
        r"\S*?https://www\.douyin\.com/discover\S*?modal_id=(\d{19})\S*?"
    )  # 首页作品链接

    mix_link = compile(
        r"\S*?https://www\.douyin\.com/collection/(\d{19})\S*?"
    )  # 合集链接
    mix_share = compile(
        r"\S*?https://www\.iesdouyin\.com/share/mix/detail/(\d{19})/\S*?"
    )  # 合集分享链接

    live_link = compile(r"\S*?https://live\.douyin\.com/([0-9]+)\S*?")  # 直播链接
    live_link_self = compile(r"\S*?https://www\.douyin\.com/follow\?webRid=(\d+)\S*?")
    live_link_share = compile(
        r"\S*?https://webcast\.amemv\.com/douyin/webcast/reflow/\S+"
    )

    channel_link = compile(
        r"\S*?https://www\.douyin\.com/channel/\d+?\?modal_id=(\d{19})\S*?"
    )

    def __init__(
        self,
        params: "Parameter",
        tiktok=False,
    ):
        self.requester = Requester(
            params,
            params.client_tiktok if tiktok else params.client,
            params.headers_tiktok if tiktok else params.headers,
        )

    async def run(
        self,
        text: str,
        type_="detail",
        proxy: str = None,
    ) -> Union[list[str], tuple[bool, list[str]], str]:
        text = await self.requester.run(
            text,
            proxy,
        )
        match type_:
            case "detail":
                return self.detail(text)
            case "user":
                return self.user(text)
            case "mix":
                return self.mix(text)
            case "live":
                return await self.live(text)
            case "":
                return text
        raise ValueError

    async def get_html_data(
        self,
        url: str,
        pattern,
        index=1,
    ) -> str:
        html = await self.requester.request_url(
            url,
            "text",
        )
        data = pattern.search(html or "")
        return data.group(index) if data else ""

    def detail(
        self,
        urls: str,
    ) -> list[str]:
        return self.__extract_detail(urls)

    def user(
        self,
        urls: str,
    ) -> list[str]:
        link = self.extract_info(self.account_link, urls, 1)
        share = self.extract_info(self.account_share, urls, 1)
        return link + share

    def mix(
        self,
        urls: str,
    ) -> tuple[bool, list[str]]:
        if detail := self.__extract_detail(urls):
            return False, detail
        link = self.extract_info(self.mix_link, urls, 1)
        share = self.extract_info(self.mix_share, urls, 1)
        return (True, m) if (m := link + share) else (None, [])

    async def live(
        self,
        urls: str,
    ) -> list[str]:
        live_link = self.extract_info(self.live_link, urls, 1)
        live_link_self = self.extract_info(self.live_link_self, urls, 1)
        live_link_share = self.extract_info(self.live_link_share, urls, 0)
        live_link_share = [
            await self.get_html_data(i, self.WEB_RID) for i in live_link_share
        ]
        return live_link + live_link_self + live_link_share

    def __extract_detail(
        self,
        urls: str,
    ) -> list[str]:
        link = self.extract_info(self.detail_link, urls, 1)
        share = self.extract_info(self.detail_share, urls, 1)
        account = self.extract_info(self.account_link, urls, 2)
        search = self.extract_info(self.detail_search, urls, 1)
        discover = self.extract_info(self.detail_discover, urls, 1)
        channel = self.extract_info(self.channel_link, urls, 1)
        return link + share + account + search + discover + channel

    @staticmethod
    def extract_sec_user_id(urls: list[str]) -> list[list]:
        data = []
        for url in urls:
            url = urlparse(url)
            query_params = parse_qs(url.query)
            data.append(
                [url.path.split("/")[-1], query_params.get("sec_user_id", [""])[0]]
            )
        return data

    @staticmethod
    def extract_info(pattern, urls: str, index=1) -> list[str]:
        result = pattern.finditer(urls)
        return [i for i in (i.group(index) for i in result) if i] if result else []


class ExtractorTikTok(Extractor):
    SEC_UID = compile(r'"secUid":"([a-zA-Z0-9_-]+)"')
    ROOD_ID = compile(r'"roomId":"(\d+)"')
    MIX_ID = compile(r'"canonical":"\S+?(\d{19})"')

    account_link = compile(r"\S*?(https://www\.tiktok\.com/@[^\s/]+)\S*?")

    detail_link = compile(
        r"\S*?https://www\.tiktok\.com/@[^\s/]+/(?!playlist|collection)(?:(?:video|photo)/(\d{19}))?\S*?"
    )  # 作品链接

    mix_link = compile(
        r"\S*?https://www\.tiktok\.com/@\S+/(?:playlist|collection)/(.+?)-(\d{19})\S*?"
    )  # 合集链接

    live_link = compile(r"\S*?https://www\.tiktok\.com/@[^\s/]+/live\S*?")  # 直播链接

    def __init__(self, params: "Parameter"):
        super().__init__(
            params,
            True,
        )

    async def run(
        self,
        text: str,
        type_="detail",
        proxy: str = None,
    ) -> Union[
        list[str],
        tuple[bool, list[str], list[str | None]],
        str,
    ]:
        text = await self.requester.run(
            text,
            proxy,
        )
        match type_:
            case "detail":
                return await self.detail(text)
            case "user":
                return await self.user(text)
            case "mix":
                return await self.mix(text)
            case "live":
                return await self.live(text)
            case "":
                return text
        raise ValueError

    async def detail(
        self,
        urls: str,
    ) -> list[str]:
        return self.__extract_detail(urls)

    async def user(
        self,
        urls: str,
    ) -> list[str]:
        link = self.extract_info(self.account_link, urls, 1)
        link = [await self.get_html_data(i, self.SEC_UID) for i in link]
        return [i for i in link if i]

    def __extract_detail(
        self,
        urls: str,
        index=1,
    ) -> list[str]:
        link = self.extract_info(self.detail_link, urls, index)
        return link

    async def mix(
        self,
        urls: str,
    ) -> tuple[bool, list[str], list[str | None]]:
        detail = self.__extract_detail(urls, index=0)
        detail = [await self.get_html_data(i, self.MIX_ID) for i in detail]
        detail = [i for i in detail if i]
        mix = self.extract_info(self.mix_link, urls, 2)
        title = [unquote(i) for i in self.extract_info(self.mix_link, urls, 1)]
        return True, detail + mix, [None for _ in detail] + title

    async def live(
        self,
        urls: str,
    ) -> list[str]:
        link = self.extract_info(self.live_link, urls, 0)
        link = [await self.get_html_data(i, self.ROOD_ID) for i in link]
        return [i for i in link if i]
