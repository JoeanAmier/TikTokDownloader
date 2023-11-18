from datetime import date
from datetime import datetime
from re import compile
from time import time
from types import SimpleNamespace
from urllib.parse import parse_qs
from urllib.parse import quote
from urllib.parse import urlencode
from urllib.parse import urlparse

from requests import exceptions
from requests import request
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)

from src.Configuration import Parameter
from src.Customizer import (
    WARNING,
    PROGRESS
)
from src.Customizer import wait
from src.DataExtractor import Extractor

__all__ = [
    "retry",
    "Link",
    "Account",
    "Works",
    "Live",
    "Comment",
    "Mix",
    "User",
    "Hot",
    "Search",
    "Collection",
]


def retry(function):
    """发生错误时尝试重新执行，装饰的函数需要返回布尔值"""

    def inner(self, *args, **kwargs):
        finished = kwargs.pop("finished", False)
        for i in range(self.max_retry):
            if result := function(self, *args, **kwargs):
                return result
            self.console.print(f"正在尝试第 {i + 1} 次重试！", style=WARNING)
        if not (result := function(self, *args, **kwargs)) and finished:
            self.finished = True
        return result

    return inner


class Acquirer:
    Phone_headers = {
        'User-Agent': 'com.ss.android.ugc.trill/494+Mozilla/5.0+(Linux;+Android+12;+2112123G+Build/SKQ1.211006.001;+wv)'
                      '+AppleWebKit/537.36+(KHTML,+like+Gecko)+Version/4.0+Chrome/107.0.5304.105+Mobile+Safari/537.36'}
    # 抖音 API
    mix_list_api = "https://www.douyin.com/aweme/v1/web/mix/listcollection/"  # 合集列表API
    feed_api = "https://www.douyin.com/aweme/v1/web/tab/feed/"  # 推荐页API
    spotlight_api = "https://www.douyin.com/aweme/v1/web/im/spotlight/relation/"  # 关注账号API
    familiar_api = "https://www.douyin.com/aweme/v1/web/familiar/feed/"  # 朋友作品推荐API
    follow_api = "https://www.douyin.com/aweme/v1/web/follow/feed/"  # 关注账号作品推荐API
    history_api = "https://www.douyin.com/aweme/v1/web/history/read/"  # 观看历史API
    following_api = "https://www.douyin.com/aweme/v1/web/user/following/list/"  # 关注列表API

    # TikTok API
    recommend_api = "https://www.tiktok.com/api/recommend/item_list/"  # 推荐页API
    home_tiktok_api = "https://www.tiktok.com/api/post/item_list/"  # 发布页API
    user_tiktok_api = "https://www.tiktok.com/api/user/detail/"  # 账号数据API
    related_tiktok_api = "https://www.tiktok.com/api/related/item_list/"  # 猜你喜欢API
    comment_tiktok_api = "https://www.tiktok.com/api/comment/list/"  # 评论API
    reply_tiktok_api = "https://www.tiktok.com/api/comment/list/reply/"  # 评论回复API

    def __init__(self, params: Parameter):
        self.PC_headers, self.black_headers = self.init_headers(params.headers)
        self.ua_code = params.ua_code
        self.log = params.logger
        self.xb = params.xb
        self.console = params.console
        self.proxies = params.proxies
        self.max_retry = params.max_retry
        self.timeout = params.timeout
        self.cursor = 0
        self.response = []
        self.finished = False

    @staticmethod
    def init_headers(headers: dict) -> tuple:
        return (headers | {
            "Referer": "https://www.douyin.com/", },
                {"User-Agent": headers["User-Agent"]})

    @retry
    def send_request(
            self,
            url: str,
            params=None,
            method='get',
            headers=None,
            **kwargs) -> dict | bool:
        try:
            response = request(
                method,
                url,
                params=params,
                proxies=self.proxies,
                timeout=self.timeout,
                headers=headers or self.PC_headers, **kwargs)
            wait()
        except (
                exceptions.ProxyError,
                exceptions.SSLError,
                exceptions.ChunkedEncodingError,
                exceptions.ConnectionError,
        ):
            self.log.warning(f"网络异常，请求 {url}?{urlencode(params)} 失败")
            return False
        except exceptions.ReadTimeout:
            self.log.warning(f"网络异常，请求 {url}?{urlencode(params)} 超时")
            return False
        try:
            return response.json()
        except exceptions.JSONDecodeError:
            self.log.warning(f"响应内容不是有效的 JSON 格式：{response.text}")
            return False

    def deal_url_params(self, params: dict, version=23):
        xb = self.xb.get_x_bogus(params, self.ua_code, version)
        params["X-Bogus"] = xb

    def deal_item_data(
            self,
            data: list[dict],
            start: int = None,
            end: int = None):
        for i in data[start:end]:
            self.response.append(i)

    def progress_object(self):
        return Progress(
            TextColumn(
                "[progress.description]{task.description}",
                style=PROGRESS,
                justify="left"),
            "•",
            BarColumn(
                bar_width=20),
            "•",
            TimeElapsedColumn(),
            console=self.console,
        )


class Share:
    share_link = compile(
        r".*?(https://v\.douyin\.com/[A-Za-z0-9]+?/).*?")
    share_link_tiktok = compile(
        r".*?(https://vm\.tiktok\.com/[a-zA-Z0-9]+/).*?")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
                      "/116.0.0.0 Safari/537.36", }

    def __init__(self, console, proxies: dict, max_retry=10):
        self.max_retry = max_retry
        self.console = console
        self.proxies = proxies

    def run(self, text: str) -> str:
        if (u := self.share_link.findall(text)) or (
                u := self.share_link_tiktok.findall(text)):
            return " ".join(self.get_url(i) for i in u)
        return text

    @retry
    def get_url(self, url: str) -> str:
        try:
            response = request(
                "get",
                url,
                timeout=10,
                proxies=self.proxies,
                headers=self.headers, )
            wait()
        except (
                exceptions.ProxyError,
                exceptions.SSLError,
                exceptions.ChunkedEncodingError,
                exceptions.ConnectionError,
                exceptions.ReadTimeout,
        ):
            return ""
        return response.url


class Link:
    # 抖音链接
    account_link = compile(
        r".*?https://www\.douyin\.com/user/([a-zA-z0-9-_]+)(?:\?modal_id=([0-9]{19}))?.*?")  # 账号主页链接
    account_share = compile(
        r".*?https://www\.iesdouyin\.com/share/user/(.*?)\?.*?"  # 账号主页分享短链
    )
    works_link = compile(
        r".*?https://www\.douyin\.com/(?:video|note)/([0-9]{19}).*?")  # 作品链接
    works_share = compile(
        r".*?https://www\.iesdouyin\.com/share/(?:video|note)/([0-9]{19})/.*?"
    )  # 作品分享短链
    mix_link = compile(
        r".*?https://www\.douyin\.com/collection/(\d{19}).*?")  # 合集链接
    live_link = compile(r".*?https://live\.douyin\.com/([0-9]+).*?")  # 直播链接
    live_link_self = compile(
        r".*?https://www\.douyin\.com/follow\?webRid=(\d+).*?"
    )
    live_link_share = compile(
        r"https://webcast\.amemv\.com/douyin/webcast/reflow/\S+")

    # TikTok 链接
    works_link_tiktok = compile(
        r".*?https://www\.tiktok\.com/@.+/video/(\d+).*?")  # 作品链接

    def __init__(self, params: Parameter):
        self.share = Share(params.console, params.proxies, params.max_retry)

    def user(self, text: str) -> list:
        urls = self.share.run(text)
        if u := self.account_link.findall(urls):
            return [i[0] for i in u]
        elif u := self.account_share.findall(urls):
            return u
        return []

    def works(self, text: str) -> tuple:
        urls = self.share.run(text)
        if u := self.works_link.findall(urls):
            tiktok = False
        elif u := self.works_link_tiktok.findall(urls):
            tiktok = True
        elif u := self.works_share.findall(urls):
            tiktok = False
        elif u := self.account_link.findall(urls):
            tiktok = False
            u = [i[1] for i in u]
        else:
            return None, []
        return tiktok, u

    def mix(self, text: str) -> tuple:
        urls = self.share.run(text)
        if u := self.works_share.findall(urls):
            return False, u
        elif u := self.works_link.findall(urls):
            return False, u
        elif u := self.mix_link.findall(urls):
            return True, u
        return None, []

    def live(self, text: str) -> tuple:
        urls = self.share.run(text)
        if u := self.live_link.findall(urls):
            return True, u
        elif u := self.live_link_self.findall(urls):
            return True, u
        elif u := self.live_link_share.findall(urls):
            return False, self.extract_sec_user_id(u)
        return None, []

    @staticmethod
    def extract_sec_user_id(urls: list[str]) -> list[list]:
        data = []
        for url in urls:
            url = urlparse(url)
            query_params = parse_qs(url.query)
            data.append([url.path.split("/")[-1],
                         query_params.get("sec_user_id", [""])[0]])
        return data


class Account(Acquirer):
    post_api = "https://www.douyin.com/aweme/v1/web/aweme/post/"
    favorite_api = "https://www.douyin.com/aweme/v1/web/aweme/favorite/"

    def __init__(
            self,
            params: Parameter,
            sec_user_id: str,
            tab="post",
            earliest="",
            latest="",
            pages: int = None, ):
        super().__init__(params)
        self.sec_user_id = sec_user_id
        self.api, self.favorite, self.pages = self.check_type(
            tab, pages or params.max_pages)
        self.earliest, self.latest = self.check_date(earliest, latest)
        self.info = Info(params, sec_user_id)

    def check_type(self, tab: str, pages: int) -> tuple[str, bool, int]:
        if tab == "favorite":
            return self.favorite_api, True, pages
        return self.post_api, False, 99999

    @staticmethod
    def check_tab(tab: str) -> bool:
        return tab in {"favorite", "post"}

    def check_date(self, start: str, end: str) -> tuple[date, date]:
        return self.check_earliest(start), self.check_latest(end)

    def check_earliest(self, date_: str) -> date:
        if not date_:
            return date(2016, 9, 20)
        try:
            earliest = datetime.strptime(
                date_, "%Y/%m/%d")
            self.log.info(f"作品最早发布日期: {date_}")
            return earliest.date()
        except ValueError:
            self.log.warning(f"作品最早发布日期 {date_} 无效")
            return date(2016, 9, 20)

    def check_latest(self, date_: str) -> date:
        if not date_:
            return date.today()
        try:
            latest = datetime.strptime(date_, "%Y/%m/%d").date()
            self.log.info(f"作品最晚发布日期: {date_}")
            return latest
        except ValueError:
            self.log.warning(f"作品最晚发布日期无效 {date_}")
            return date.today()

    def run(self) -> tuple[list[dict], date, date]:
        with self.progress_object() as progress:
            task_id = progress.add_task(
                "正在获取账号主页数据", total=None)
            while not self.finished and self.pages > 0:
                progress.update(task_id)
                self.get_account_data(self.api)
                self.early_stop()
                self.pages -= 1
                # break  # 调试代码
        self.summary_works()
        self.favorite_mode()
        return self.response, self.earliest, self.latest

    def get_account_data(self, api: str):
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "sec_user_id": self.sec_user_id,
            "max_cursor": self.cursor,
            "count": "18",
            "version_code": "170400",
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10",
        }
        self.deal_url_params(params)
        if not (
                data := self.send_request(
                    api,
                    params=params,
                    finished=True)):
            self.log.warning("获取账号作品数据失败")
            return
        try:
            if (data_list := data["aweme_list"]) is None:
                self.log.info("该账号为私密账号，需要使用登录后的 Cookie，且登录的账号需要关注该私密账号")
                self.finished = True
            else:
                self.cursor = data['max_cursor']
                self.deal_item_data(data_list)
                self.finished = not data["has_more"]
        except KeyError:
            self.log.error(f"账号作品数据响应内容异常: {data}")
            self.finished = True

    def early_stop(self):
        """如果获取数据的发布日期已经早于限制日期，就不需要再获取下一页的数据了"""
        if not self.favorite and self.earliest > datetime.fromtimestamp(
                max(self.cursor / 1000, 0)).date():
            self.finished = True

    def favorite_mode(self):
        if not self.favorite:
            return
        info = Extractor.get_user_info(self.info.run())
        if self.sec_user_id != (s := info.get("sec_uid")):
            self.log.error(
                f"sec_user_id {self.sec_user_id} 与 {s} 不一致")
            self.generate_temp_data()
        else:
            self.response.append({"author": info})

    def generate_temp_data(self):
        fake_data = self.temp_data()
        self.log.warning(f"获取账号昵称失败，本次运行将临时使用 {fake_data} 作为账号昵称和 UID")
        fake_dict = {
            "author": {
                "nickname": fake_data,
                "uid": fake_data,
            }
        }
        self.response.append(fake_dict)

    @staticmethod
    def temp_data() -> str:
        return str(time())[:10]

    def summary_works(self):
        self.log.info(f"当前账号获取作品数量: {len(self.response)}")


class Works(Acquirer):
    item_api = "https://www.douyin.com/aweme/v1/web/aweme/detail/"
    item_api_tiktok = "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/"

    def __init__(self, params: Parameter, item_id: str, tiktok: bool):
        super().__init__(params)
        self.id = item_id
        self.tiktok = tiktok

    def run(self) -> dict:
        if self.tiktok:
            params = {
                "aweme_id": self.id,
            }
            api = self.item_api_tiktok
            headers = self.Phone_headers
        else:
            params = {
                "aweme_id": self.id,
                "aid": "6383",
                "version_code": "170400",
                "cookie_enabled": "true",
                "platform": "PC",
                "downlink": "10"
            }
            api = self.item_api
            self.deal_url_params(params)
            headers = None
        if not (
                data := self.send_request(
                    api,
                    params=params,
                    headers=headers,
                )):
            self.log.warning("获取作品数据失败")
            return {}
        try:
            return data["aweme_list"][0] if self.tiktok else data["aweme_detail"] or {}
        except (KeyError, IndexError):
            self.log.error(f"作品数据响应内容异常: {data}")


class Comment(Acquirer):
    comment_api = "https://www.douyin.com/aweme/v1/web/comment/list/"  # 评论API
    comment_api_reply = "https://www.douyin.com/aweme/v1/web/comment/list/reply/"  # 评论回复API

    def __init__(self, params: Parameter, item_id: str, pages: int = None):
        super().__init__(params)
        self.item_id = item_id
        self.pages = pages or params.max_pages
        self.all_data = None
        self.reply_ids = None

    def run(self, extractor: Extractor, recorder, source=False) -> list[dict]:
        with self.progress_object() as progress:
            task_id = progress.add_task(
                "正在获取作品评论数据", total=None)
            while not self.finished and self.pages > 0:
                progress.update(task_id)
                self.get_comments_data(self.comment_api)
                self.pages -= 1
                # break  # 调试代码
        self.all_data, self.reply_ids = extractor.run(
            self.response, recorder, "comment", source=source)
        self.response = []
        with self.progress_object() as progress:
            task_id = progress.add_task(
                "正在获取评论回复数据", total=None)
            for i in self.reply_ids:
                self.finished = False
                self.cursor = 0
                while not self.finished and self.pages > 0:
                    progress.update(task_id)
                    self.get_comments_data(self.comment_api_reply, i)
                    self.pages -= 1
                    # break  # 调试代码
        self.all_data.extend(
            self._check_reply_ids(
                *
                extractor.run(
                    self.response,
                    recorder,
                    "comment",
                    source=source)))
        return self.all_data

    def get_comments_data(self, api: str, reply=""):
        if reply:
            params = {
                "device_platform": "webapp",
                "aid": "6383",
                "channel": "channel_pc_web",
                "item_id": self.item_id,
                "comment_id": reply,
                "cursor": self.cursor,
                "count": "10" if self.cursor else "3",  # 每次返回数据的数量
                "version_code": "170400",
                "cookie_enabled": "true",
                "platform": "PC",
                "downlink": "10",
            }
            self.deal_url_params(params, 174)
        else:
            params = {
                "device_platform": "webapp",
                "aid": "6383",
                "channel": "channel_pc_web",
                "aweme_id": self.item_id,
                "cursor": self.cursor,
                "count": "20",
                "version_code": "170400",
                "cookie_enabled": "true",
                "platform": "PC",
                "downlink": "10",
            }
            self.deal_url_params(params)
        if not (
                data := self.send_request(
                    api,
                    params=params,
                    finished=True)):
            self.log.warning("获取作品评论数据失败")
            return
        try:
            if not (c := data["comments"]):
                raise KeyError
            self.deal_item_data(c)
            self.cursor = data["cursor"]
            self.finished = not data["has_more"]
        except KeyError:
            self.log.error(f"作品评论数据响应内容异常: {data}")
            self.finished = True

    @staticmethod
    def _check_reply_ids(data: list[dict], ids: list) -> list[dict]:
        if ids:
            raise ValueError
        return data


class Mix(Acquirer):
    mix_api = "https://www.douyin.com/aweme/v1/web/mix/aweme/"  # 合集API

    def __init__(
            self,
            params: Parameter,
            mix_id: str = None,
            works_id: str = None):
        super().__init__(params)
        self.works = Works(params, item_id=works_id, tiktok=False)
        self.mix_id = mix_id
        self.works_id = works_id

    def run(self) -> list:
        self._get_mix_id()
        if not self.mix_id:
            return []
        with self.progress_object() as progress:
            task_id = progress.add_task(
                "正在获取合集作品数据", total=None)
            while not self.finished:
                progress.update(task_id)
                self._get_mix_data()
                # break  # 调试代码
        return self.response

    def _get_mix_data(self):
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "mix_id": self.mix_id,
            "cursor": self.cursor,
            "count": "20",
            "version_code": "170400",
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10",
        }
        self.deal_url_params(params)
        if not (
                data := self.send_request(
                    self.mix_api,
                    params=params,
                    finished=True,
                )):
            self.log.warning("获取合集作品数据失败")
            return
        try:
            if not (w := data["aweme_list"]):
                raise KeyError
            self.deal_item_data(w)
            self.cursor = data['cursor']
            self.finished = not data["has_more"]
        except KeyError:
            self.log.error(f"合集数据内容异常: {data}")
            self.finished = True

    def _get_mix_id(self):
        if not self.mix_id:
            self.mix_id = Extractor.extract_mix_id(self.works.run())


class Live(Acquirer):
    live_api = "https://live.douyin.com/webcast/room/web/enter/"
    live_api_share = "https://webcast.amemv.com/webcast/room/reflow/info/"

    def __init__(
            self,
            params: Parameter,
            web_rid=None,
            room_id=None,
            sec_user_id=None):
        super().__init__(params)
        self.PC_headers["Referer"] = "https://live.douyin.com/"
        self.web_rid = web_rid
        self.room_id = room_id
        self.sec_user_id = sec_user_id

    def run(self) -> dict:
        if self.web_rid:
            return self.with_web_rid()
        elif self.room_id:
            return self.with_room_id()
        else:
            return {}

    def with_web_rid(self) -> dict:
        params = {
            "aid": "6383",
            "app_name": "douyin_web",
            "device_platform": "web",
            "version_code": "170400",
            "cookie_enabled": "true",
            "web_rid": self.web_rid,
        }
        api = self.live_api
        self.deal_url_params(params)
        return self.get_live_data(api, params)

    def with_room_id(self) -> dict:
        params = {
            "type_id": "0",
            "live_id": "1",
            "room_id": self.room_id,
            "sec_user_id": self.sec_user_id,
            "version_code": "99.99.99",
            "app_id": "1128",
        }
        api = self.live_api_share
        headers = self.black_headers
        self.deal_url_params(params, 174)
        return self.get_live_data(api, params, headers)

    def get_live_data(
            self,
            api: str,
            params: dict,
            headers: dict = None) -> dict:
        if not (
                data := self.send_request(
                    api,
                    params=params,
                    headers=headers,
                )):
            self.log.warning("获取直播数据失败")
            return {}
        return data or {}


class User(Acquirer):
    user_api = "https://www.douyin.com/aweme/v1/web/user/profile/other/"  # 账号详细数据API

    def __init__(self, params: Parameter, sec_user_id: str):
        super().__init__(params)
        self.sec_user_id = sec_user_id

    def run(self):
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "source": "channel_pc_web",
            "sec_user_id": self.sec_user_id,
            "version_code": "170400",
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10",
        }
        self.deal_url_params(params)
        if not (
                data := self.send_request(
                    self.user_api,
                    params=params,
                )):
            self.log.warning("获取账号数据失败")
            return {}
        try:
            return data["user"] or {}
        except KeyError:
            self.log.error(f"账号数据响应内容异常: {data}")


class Search(Acquirer):
    search_params = (
        SimpleNamespace(
            api="https://www.douyin.com/aweme/v1/web/general/search/single/",
            count=15,
            channel="aweme_general",
            type="general",
        ),
        SimpleNamespace(
            api="https://www.douyin.com/aweme/v1/web/search/item/",
            count=20,
            channel="aweme_video_web",
            type="video",
        ),
        SimpleNamespace(
            api="https://www.douyin.com/aweme/v1/web/discover/search/",
            count=12,
            channel="aweme_user_web",
            type="user",
        ),
        SimpleNamespace(
            api="https://www.douyin.com/aweme/v1/web/live/search/",
            count=15,
            channel="aweme_live",
            type="live",
        ),
    )

    def __init__(
            self,
            params: Parameter,
            keyword: str,
            tab=0,
            page=1,
            sort_type=0,
            publish_time=0):
        super().__init__(params)
        self.keyword = keyword
        self.tab = tab
        self.page = page
        self.sort_type = sort_type
        self.publish_time = publish_time

    def run(self):
        data = self.search_params[self.tab]
        self.PC_headers["Referer"] = (
            f"https://www.douyin.com/search/{
            quote(
                self.keyword)}?" f"source=switch_tab&type={
            data.type}")
        if self.tab in {2, 3}:
            deal = self._run_user_live
        elif self.tab in {0, 1}:
            deal = self._run_general
        else:
            raise ValueError
        with self.progress_object() as progress:
            task_id = progress.add_task(
                "正在获取搜索结果数据", total=None)
            while not self.finished and self.page > 0:
                progress.update(task_id)
                deal(data, self.tab)
                self.page -= 1
        return self.response

    def _run_user_live(self, data: SimpleNamespace, type_: int):
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "search_channel": data.channel,
            "keyword": self.keyword,
            "search_source": "switch_tab",
            "query_correct_type": "1",
            "is_filter_search": "0",
            "offset": self.cursor,
            "count": 10 if self.cursor else data.count,
            "pc_client_type": "1",
            "version_code": "170400",
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "7.7",
        }
        self.deal_url_params(params, 174 if self.cursor else 23)
        self._get_search_data(
            data.api,
            params,
            "user_list" if type_ == 2 else "data")

    def _run_general(self, data: SimpleNamespace, *args):
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "search_channel": data.channel,
            "sort_type": self.sort_type,
            "publish_time": self.publish_time,
            "keyword": self.keyword,
            "search_source": "switch_tab",
            "query_correct_type": "1",
            "is_filter_search": {True: 1, False: 0}[any((self.sort_type, self.publish_time))],
            "offset": self.cursor,
            "count": 10 if self.cursor else data.count,
            "pc_client_type": "1",
            "version_code": "170400",
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "7.7",
        }
        self.deal_url_params(params, 174 if self.cursor else 23)
        self._get_search_data(data.api, params, "data")

    def _get_search_data(self, api: str, params: dict, key: str):
        if not (
                data := self.send_request(
                    api,
                    params=params,
                    finished=True,
                )):
            self.log.warning("获取搜索数据失败")
            return
        try:
            self.deal_item_data(data[key])
        except KeyError:
            self.log.error(f"搜索数据响应内容异常: {data}")
            self.finished = True


class Hot(Acquirer):
    hot_api = "https://www.douyin.com/aweme/v1/web/hot/search/list/"  # 热榜API
    board_params = (
        SimpleNamespace(
            name="抖音热榜",
            type=0,
            sub_type="",
        ),
        SimpleNamespace(
            name="娱乐榜",
            type=2,
            sub_type=2,
        ),
        SimpleNamespace(
            name="社会榜",
            type=2,
            sub_type=4,
        ),
        SimpleNamespace(
            name="挑战榜",
            type=2,
            sub_type="hotspot_challenge",
        ),
    )

    def __init__(self, params: Parameter):
        super().__init__(params)
        del self.PC_headers["Cookie"]
        self.time = None

    def run(self):
        self.time = datetime.now().strftime("%Y-%m-%d %H.%M.%S")
        for i, j in enumerate(self.board_params):
            self._get_board_data(i, j)
        return self.time, self.response

    def _get_board_data(self, index: int, data: SimpleNamespace):
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "detail_list": "1",
            "source": "6",
            "board_type": data.type,
            "board_sub_type": data.sub_type,
            "pc_client_type": "1",
            "version_code": "170400",
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "1.4",
        }
        self.deal_url_params(params)
        if not (
                board := self.send_request(
                    self.hot_api,
                    params=params,
                )):
            self.log.warning(f"获取 {data.name} 数据失败")
            return
        try:
            self.response.append((index, board["data"]["word_list"]))
        except KeyError:
            self.log.error(f"{data.name} 数据响应内容异常: {board}")


class Collection(Acquirer):
    collection_api = "https://www.douyin.com/aweme/v1/web/aweme/listcollection/"  # 收藏API
    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "publish_video_strategy_type": "2",
        "pc_client_type": "1",
        "version_code": "170400",
        "cookie_enabled": "true",
        "platform": "PC",
        "downlink": "5.45",
    }

    def __init__(self, params: Parameter, sec_user_id: str,
                 pages: int = None, ):
        super().__init__(params)
        self.pages = pages or params.max_pages
        self.sec_user_id = bool(sec_user_id)
        self.info = Info(params, sec_user_id)

    def run(self):
        with self.progress_object() as progress:
            task_id = progress.add_task(
                "正在获取账号收藏数据", total=None)
            while not self.finished and self.pages > 0:
                progress.update(task_id)
                self._get_account_data()
                self.pages -= 1
        self._get_owner_data()
        return self.response

    def _get_account_data(self):
        params = self.params.copy()
        self.deal_url_params(params)
        form = {
            "count": "10",
            "cursor": self.cursor,
        }
        if not (
                data := self.send_request(
                    self.collection_api,
                    params=params,
                    data=form,
                    method='post',
                    finished=True)):
            self.log.warning("获取账号收藏数据失败")
            return
        try:
            self.cursor = data['cursor']
            self.deal_item_data(data["aweme_list"])
            self.finished = not data["has_more"]
        except KeyError:
            self.log.error(f"账号收藏数据响应内容异常: {data}")
            self.finished = True

    def _get_owner_data(self):
        if self.sec_user_id and (
                info := Extractor.get_user_info(
                    self.info.run())):
            self.response.append({"author": info})
        else:
            temp_data = Account.temp_data()
            self.log.warning(f"owner_url 参数未设置 或者 获取账号数据失败，本次运行将临时使用 {
            temp_data} 作为账号昵称和 UID")
            fake_data = {
                "author": {
                    "nickname": temp_data,
                    "uid": temp_data,
                }
            }
            self.response.append(fake_data)


class Info(Acquirer):
    info_api = "https://www.douyin.com/aweme/v1/web/im/user/info/"  # 账号简略数据API

    def __init__(self, params: Parameter, sec_user_id: str):
        super().__init__(params)
        self.sec_user_id = sec_user_id
        self.params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "version_code": "170400",
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10",
        }

    def run(self):
        self.deal_url_params(self.params)
        form = {
            "sec_user_ids": f'["{self.sec_user_id}"]'
        }
        if not (
                data := self.send_request(
                    self.info_api,
                    params=self.params,
                    method='post',
                    data=form,
                )):
            self.log.warning("获取账号数据失败")
            return {}
        try:
            return data["data"][0] or {}
        except (KeyError, IndexError, TypeError):
            self.log.error(f"账号数据响应内容异常: {data}")
