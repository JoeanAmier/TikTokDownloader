from itertools import chain
from re import compile
from typing import Iterator
from typing import TYPE_CHECKING
from typing import Union
from urllib.parse import parse_qs
from urllib.parse import urlparse

from .requester import Requester

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["Extractor", "ExtractorTikTok"]


class Extractor:
    account_link = compile(
        r"\S*?https://www\.douyin\.com/user/([A-Za-z0-9_-]+)(?:\S*?\bmodal_id=(\d{19}))?")  # 账号主页链接
    account_share = compile(
        r"\S*?https://www\.iesdouyin\.com/share/user/(\S*?)\?\S*?"  # 账号主页分享链接
    )

    detail_id = compile(r"\b(\d{19})\b")  # 作品 ID
    detail_link = compile(
        r"\S*?https://www\.douyin\.com/(?:video|note)/([0-9]{19})\S*?")  # 作品链接
    detail_share = compile(
        r"\S*?https://www\.iesdouyin\.com/share/(?:video|note)/([0-9]{19})/\S*?"
    )  # 作品分享链接
    detail_search = compile(
        r"\S*?https://www\.douyin\.com/search/\S+?modal_id=(\d{19})\S*?"
    )  # 搜索作品链接
    detail_discover = compile(
        r"\S*?https://www\.douyin\.com/discover\S*?modal_id=(\d{19})\S*?"
    )  # 首页作品链接

    mix_link = compile(
        r"\S*?https://www\.douyin\.com/collection/(\d{19})\S*?")  # 合集链接
    mix_share = compile(
        r"\S*?https://www\.iesdouyin\.com/share/mix/detail/(\d{19})/\S*?")  # 合集分享链接

    live_link = compile(r"\S*?https://live\.douyin\.com/([0-9]+)\S*?")  # 直播链接
    live_link_self = compile(
        r"\S*?https://www\.douyin\.com/follow\?webRid=(\d+)\S*?"
    )
    live_link_share = compile(
        r"\S*?https://webcast\.amemv\.com/douyin/webcast/reflow/\S+")

    channel_link = compile(
        r"\S*?https://www\.douyin\.com/channel/\d+?\?modal_id=(\d{19})\S*?")

    def __init__(self, params: "Parameter"):
        self.requester = Requester(params)
        self.proxy = params.proxy

    async def run(self, urls: str,
                  type_="detail") -> Union[list[str], tuple[bool, list[str]]]:
        urls = await self.requester.run(urls, self.proxy)
        match type_:
            case "detail":
                return self.detail(urls)
            case "user":
                return self.user(urls)
            case "mix":
                return self.mix(urls)
            case "live":
                return self.live(urls)
        raise ValueError

    def detail(self, urls: str, ) -> list[str]:
        return self.__extract_detail(urls)

    def user(self, urls: str, ) -> list[str]:
        link = self.extract_info(self.account_link, urls, 1)
        share = self.extract_info(self.account_share, urls, 1)
        # return chain(link, share)
        return list(chain(link, share))

    def mix(self, urls: str, ) -> [bool, list[str]]:
        if detail := self.__extract_detail(urls):
            return False, detail
        link = self.extract_info(self.mix_link, urls, 1)
        share = self.extract_info(self.mix_share, urls, 1)
        return (
            True,
            m) if (
            m := self.__convert_iterator(
                chain(
                    link,
                    share))) else (
            None,
            [])

    def live(self, urls: str, ) -> [bool, list]:
        live_link = self.extract_info(self.live_link, urls, 1)
        live_link_self = self.extract_info(self.live_link_self, urls, 1)
        if live := self.__convert_iterator(chain(live_link, live_link_self)):
            return True, live
        live_link_share = self.extract_info(self.live_link_share, urls, 0)
        return False, self.extract_sec_user_id(live_link_share)

    def __extract_detail(self, urls: str, ) -> list[str]:
        link = self.extract_info(self.detail_link, urls, 1)
        share = self.extract_info(self.detail_share, urls, 1)
        account = self.extract_info(self.account_link, urls, 2)
        search = self.extract_info(self.detail_search, urls, 1)
        discover = self.extract_info(self.detail_discover, urls, 1)
        channel = self.extract_info(self.channel_link, urls, 1)
        # return chain(link, share, account, search, discover, channel)
        return list(chain(link, share, account, search, discover, channel))

    @staticmethod
    def __convert_iterator(data: Iterator) -> list:
        return list(data)

    @staticmethod
    def extract_sec_user_id(urls: Iterator[str]) -> list[list]:
        data = []
        for url in urls:
            url = urlparse(url)
            query_params = parse_qs(url.query)
            data.append([url.path.split("/")[-1],
                         query_params.get("sec_user_id", [""])[0]])
        return data

    @staticmethod
    def extract_info(pattern, urls: str, index=1) -> Iterator[str]:
        result = pattern.finditer(urls)
        return (i.group(index) for i in result) if result else []


class ExtractorTikTok(Extractor):
    secUid = compile(r'"secUid":"([a-zA-Z0-9_-]+)"')

    account_link = compile(r"\S*?(https://www\.tiktok\.com/@[^\s/]+)\S*?")

    detail_link = compile(
        r"\S*?https://www\.tiktok\.com/@[^\s/]+(?:/(?:video|photo)/(\d{19}))?\S*?")  # 作品链接

    def __init__(self, params: "Parameter"):
        super().__init__(params)
        self.proxy = params.proxy_tiktok

    async def run(self, urls: str,
                  type_="detail") -> Union[list[str], tuple[bool, list[str]]]:
        urls = await self.requester.run(urls, self.proxy)
        match type_:
            case "detail":
                return self.detail(urls)
            case "user":
                return await self.user(urls)
            # case "mix":
            #     return self.mix(urls)
            # case "live":
            #     return self.live(urls)
        raise ValueError

    def detail(self, urls: str, ) -> list[str]:
        return self.__extract_detail(urls)

    async def user(self, urls: str, ) -> list[str]:
        link = self.extract_info(self.account_link, urls, 1)
        link = [await self.__get_sec_uid(i) for i in link]
        return list(chain((i for i in link if i), ))

    def __extract_detail(self, urls: str, ) -> list[str]:
        link = self.extract_info(self.detail_link, urls, 1)
        return list(chain(link, ))

    async def __get_sec_uid(self, url: str) -> str:
        html = await self.requester.request_url(url, self.proxy, "text", )
        return self.__extract_sec_uid(html) if html else ""

    def __extract_sec_uid(self, html: str) -> str:
        return m.group(1) if (m := self.secUid.search(html)) else ""
