from datetime import date
from datetime import datetime
from re import compile
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

from src.config import Parameter
from src.custom import (
    PROGRESS
)
from src.custom import wait
from src.extract import Extractor
from src.tools import retry
from src.tools import timestamp

__all__ = [
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

    def __init__(self, params: Parameter, cookie: str = None):
        self.PC_headers, self.black_headers = self.init_headers(params.headers)
        self.ua_code = params.ua_code
        self.log = params.logger
        self.xb = params.xb
        self.console = params.console
        self.proxies = params.proxies
        self.max_retry = params.max_retry
        self.timeout = params.timeout
        self.cookie = params.cookie
        self.cursor = 0
        self.response = []
        self.finished = False
        self.__set_temp_cookie(cookie)

    @staticmethod
    def init_headers(headers: dict) -> tuple:
        return (headers | {
            "Referer": "https://www.douyin.com/", },
                {"User-Agent": headers["User-Agent"]})

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
            if response.text:
                self.log.warning(f"响应内容不是有效的 JSON 格式：{response.text}")
            else:
                self.log.warning("响应内容为空，可能是接口失效或者 Cookie 失效，请尝试更新 Cookie")
            return False

    def deal_url_params(self, params: dict, version=23):
        self.__add_ms_token(params)
        params["X-Bogus"] = self.xb.get_x_bogus(params, self.ua_code, version)

    def __add_ms_token(self, params: dict):
        if isinstance(self.cookie, dict) and "msToken" in self.cookie:
            params["msToken"] = self.cookie["msToken"]

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
            transient=True,
        )

    def __set_temp_cookie(self, cookie: str):
        if cookie:
            self.PC_headers["Cookie"] = cookie


class Share:
    share_link = compile(
        r"\S*?(https://v\.douyin\.com/[^/\s]+)\S*?")
    share_link_tiktok = compile(
        r"\S*?(https://vm\.tiktok\.com/[^/\s]+)\S*?")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
                      "/116.0.0.0 Safari/537.36", }

    def __init__(self, logger, proxies: dict, max_retry=10):
        self.max_retry = max_retry
        self.log = logger
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
            self.log.warning(f"分享链接 {url} 请求数据失败")
            return ""
        return response.url


class Link:
    # 抖音链接
    account_link = compile(
        r"\S*?https://www\.douyin\.com/user/([A-Za-z0-9_-]+)(?:\S*?\bmodal_id=(\d{19}))?")  # 账号主页链接
    account_share = compile(
        r"\S*?https://www\.iesdouyin\.com/share/user/(\S*?)\?\S*?"  # 账号主页分享链接
    )
    works_id = compile(r"\b(\d{19})\b")  # 作品 ID
    works_link = compile(
        r"\S*?https://www\.douyin\.com/(?:video|note)/([0-9]{19})\S*?")  # 作品链接
    works_share = compile(
        r"\S*?https://www\.iesdouyin\.com/share/(?:video|note)/([0-9]{19})/\S*?"
    )  # 作品分享链接
    works_search = compile(
        r"\S*?https://www\.douyin\.com/search/\S+?modal_id=(\d{19})\S*?"
    )  # 搜索作品链接
    works_discover = compile(
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

    # TikTok 链接
    works_link_tiktok = compile(
        r"\S*?https://www\.tiktok\.com/@\S+?/video/(\d{19})\S*?")  # 作品链接

    def __init__(self, params: Parameter):
        self.share = Share(params.logger, params.proxies, params.max_retry)

    def user(self, text: str) -> list:
        urls = self.share.run(text)
        link = [i for i in [i[0]
                            for i in self.account_link.findall(urls)] if i]
        share = self.account_share.findall(urls)
        return link + share

    def works(self, text: str) -> tuple[bool, list]:
        urls = self.share.run(text)
        if u := self.works_link_tiktok.findall(urls):
            return True, u
        link = self.works_link.findall(urls)
        share = self.works_share.findall(urls)
        account = [i for i in [i[1]
                               for i in self.account_link.findall(urls)] if i]
        search = self.works_search.findall(urls)
        discover = self.works_discover.findall(urls)
        return False, link + share + account + search + discover

    def mix(self, text: str) -> tuple:
        urls = self.share.run(text)
        share = self.works_share.findall(urls)
        link = self.works_link.findall(urls)
        search = self.works_search.findall(urls)
        discover = self.works_discover.findall(urls)
        if u := share + link + search + discover:
            return False, u
        link = self.mix_link.findall(urls)
        share = self.mix_share.findall(urls)
        return True, u if (u := link + share) else None, []

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
            pages: int = None,
            cookie: str = None, ):
        super().__init__(params, cookie)
        self.sec_user_id = sec_user_id
        self.api, self.favorite, self.pages = self.check_type(
            tab, pages or params.max_pages)
        self.earliest, self.latest = self.check_date(earliest, latest)
        self.info = Info(params, sec_user_id, cookie)

    def check_type(self, tab: str, pages: int) -> tuple[str, bool, int]:
        if tab == "favorite":
            return self.favorite_api, True, pages
        elif tab != "post":
            self.log.warning(f"tab 参数 {tab} 设置错误，程序将使用默认值: post")
        return self.post_api, False, 99999

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
                self.get_account_data(self.api, finished=True)
                self.early_stop()
                self.pages -= 1
                # break  # 调试代码
        self.summary_works()
        self.favorite_mode()
        return self.response, self.earliest, self.latest

    @retry
    def get_account_data(self, api: str):
        if self.favorite:
            params = {
                "device_platform": "webapp",
                "aid": "6383",
                "channel": "channel_pc_web",
                "sec_user_id": self.sec_user_id,
                "max_cursor": self.cursor,
                "min_cursor": "0",
                "whale_cut_token": "",
                "cut_version": "1",
                "count": "18",
                "publish_video_strategy_type": "2",
                "pc_client_type": "1",
                "version_code": "170400",
                "version_name": "17.4.0",
                "cookie_enabled": "true",
                "platform": "PC",
                "downlink": "10",
            }
        else:
            params = {
                "device_platform": "webapp",
                "aid": "6383",
                "channel": "channel_pc_web",
                "sec_user_id": self.sec_user_id,
                "max_cursor": self.cursor,
                "locate_query": "false",
                "show_live_replay_strategy": "1",
                "need_time_list": "0" if self.cursor else "1",
                "time_list_query": "0",
                "whale_cut_token": "",
                "cut_version": "1",
                "count": "18",
                "publish_video_strategy_type": "2",
                "pc_client_type": "1",
                "version_code": "170400",
                "version_name": "17.4.0",
                "cookie_enabled": "true",
                "platform": "PC",
                "downlink": "10",
            }
        self.deal_url_params(params)
        if not (
                data := self.send_request(
                    api,
                    params=params)):
            self.log.warning("获取账号作品数据失败")
            return False
        try:
            if (data_list := data["aweme_list"]) is None:
                self.log.info("该账号为私密账号，需要使用登录后的 Cookie，且登录的账号需要关注该私密账号")
                self.finished = True
            else:
                self.cursor = data['max_cursor']
                self.deal_item_data(data_list)
                self.finished = not data["has_more"]
            return True
        except KeyError:
            self.log.error(f"账号作品数据响应内容异常: {data}")
            self.finished = True
            return False

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
        temp_data = timestamp()
        self.log.warning(f"获取账号昵称失败，本次运行将临时使用 {temp_data} 作为账号昵称和 UID")
        temp_dict = {
            "author": {
                "nickname": temp_data,
                "uid": temp_data,
            }
        }
        self.response.append(temp_dict)

    def summary_works(self):
        self.log.info(f"当前账号获取作品数量: {len(self.response)}")


class Works(Acquirer):
    item_api = "https://www.douyin.com/aweme/v1/web/aweme/detail/"
    item_api_tiktok = "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/"

    def __init__(self, params: Parameter, item_id: str, tiktok: bool,
                 cookie: str = None, ):
        super().__init__(params, cookie)
        self.id = item_id
        self.tiktok = tiktok

    @retry
    def run(self) -> dict:
        if self.tiktok:
            params = {
                "aweme_id": self.id,
            }
            api = self.item_api_tiktok
            headers = self.Phone_headers
        else:
            params = {
                "device_platform": "webapp",
                "aid": "6383",
                "channel": "channel_pc_web",
                "aweme_id": self.id,
                "pc_client_type": "1",
                "version_code": "190500",
                "version_name": "19.5.0",
                "cookie_enabled": "true",
                "platform": "PC",
                "downlink": "10",
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
            return {}


class Comment(Acquirer):
    comment_api = "https://www.douyin.com/aweme/v1/web/comment/list/"  # 评论API
    comment_api_reply = "https://www.douyin.com/aweme/v1/web/comment/list/reply/"  # 评论回复API

    def __init__(self, params: Parameter, item_id: str, pages: int = None,
                 cookie: str = None, ):
        super().__init__(params, cookie)
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
                self.get_comments_data(self.comment_api, finished=True)
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
                    self.get_comments_data(
                        self.comment_api_reply, i, finished=True)
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

    @retry
    def get_comments_data(self, api: str, reply=""):
        if reply:
            params = {
                "device_platform": "webapp",
                "aid": "6383",
                "channel": "channel_pc_web",
                "item_id": self.item_id,
                "comment_id": reply,
                "whale_cut_token": "",
                "cut_version": "1",
                "cursor": self.cursor,
                "count": "10" if self.cursor else "3",
                "item_type": "0",
                "pc_client_type": "1",
                "version_code": "170400",
                "version_name": "17.4.0",
                "cookie_enabled": "true",
                "platform": "PC",
                "downlink": "10",
            }
            if not self.cursor:
                del params["whale_cut_token"]
            self.deal_url_params(params, 174)
        else:
            params = {
                "device_platform": "webapp",
                "aid": "6383",
                "channel": "channel_pc_web",
                "aweme_id": self.item_id,
                "cursor": self.cursor,
                "count": "20",
                "item_type": "0",
                "insert_ids": "",
                "whale_cut_token": "",
                "cut_version": "1",
                "rcFT": "",
                "pc_client_type": "1",
                "version_code": "170400",
                "version_name": "17.4.0",
                "cookie_enabled": "true",
                "platform": "PC",
                "downlink": "10",
            }
            self.deal_url_params(params)
        if not (
                data := self.send_request(
                    api,
                    params=params)):
            self.log.warning("获取作品评论数据失败")
            return False
        try:
            if not (c := data["comments"]):
                raise KeyError
            self.deal_item_data(c)
            self.cursor = data["cursor"]
            self.finished = not data["has_more"]
            return True
        except KeyError:
            self.log.error(f"作品评论数据响应内容异常: {data}")
            self.finished = True
            return False

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
            works_id: str = None,
            cookie: str = None, ):
        super().__init__(params, cookie)
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
                self._get_mix_data(finished=True)
                # break  # 调试代码
        return self.response

    @retry
    def _get_mix_data(self):
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "mix_id": self.mix_id,
            "cursor": self.cursor,
            "count": "20",
            "pc_client_type": "1",
            "version_code": "170400",
            "version_name": "17.4.0",
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10",
        }
        self.deal_url_params(params)
        if not (
                data := self.send_request(
                    self.mix_api,
                    params=params,
                )):
            self.log.warning("获取合集作品数据失败")
            return False
        try:
            if not (w := data["aweme_list"]):
                raise KeyError
            self.deal_item_data(w)
            self.cursor = data['cursor']
            self.finished = not data["has_more"]
            return True
        except KeyError:
            self.log.error(f"合集数据内容异常: {data}")
            self.finished = True
            return False

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
            sec_user_id=None,
            cookie: str = None, ):
        super().__init__(params, cookie)
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
            "language": "zh-CN",
            "enter_from": "web_live",
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

    @retry
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

    def __init__(self, params: Parameter, sec_user_id: str,
                 cookie: str = None, ):
        super().__init__(params, cookie)
        self.sec_user_id = sec_user_id

    @retry
    def run(self) -> dict:
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "publish_video_strategy_type": "2",
            "source": "channel_pc_web",
            "sec_user_id": self.sec_user_id,
            "personal_center_strategy": "1",
            "pc_client_type": "1",
            "version_code": "170400",
            "version_name": "17.4.0",
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
            return {}


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
            publish_time=0,
            cookie: str = None, ):
        super().__init__(params, cookie)
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
            "from_group_id": "",
            "offset": self.cursor,
            "count": 10 if self.cursor else data.count,
            "pc_client_type": "1",
            "version_code": "170400",
            "version_name": "17.4.0",
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10",
        }
        self.deal_url_params(params, 174 if self.cursor else 23)
        self._get_search_data(
            data.api,
            params,
            "user_list" if type_ == 2 else "data", finished=True)

    def _run_general(self, data: SimpleNamespace, type_: int, *args):
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "search_channel": data.channel,
            "sort_type": self.sort_type,
            "publish_time": self.publish_time,
            "keyword": self.keyword,
            "search_source": "tab_search",
            "query_correct_type": "1",
            "is_filter_search": {True: 1, False: 0}[any((self.sort_type, self.publish_time))],
            "from_group_id": "",
            "offset": self.cursor,
            "count": 10 if self.cursor else data.count,
            "pc_client_type": "1",
            "version_code": "170400" if type_ else "190600",
            "version_name": "17.4.0" if type_ else "19.6.0",
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10",
        }
        self.deal_url_params(params, 174 if self.cursor else 23)
        self._get_search_data(data.api, params, "data", finished=True)

    @retry
    def _get_search_data(self, api: str, params: dict, key: str):
        if not (
                data := self.send_request(
                    api,
                    params=params,
                )):
            self.log.warning("获取搜索数据失败")
            return False
        try:
            self.deal_item_data(data[key])
            self.cursor = data["cursor"]
            self.finished = not data["has_more"]
            return True
        except KeyError:
            self.log.error(f"搜索数据响应内容异常: {data}")
            self.finished = True
            return False


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
        self.time = f"{datetime.now():%Y_%m_%d_%H_%M_%S}"
        for i, j in enumerate(self.board_params):
            self._get_board_data(i, j)
        return self.time, self.response

    @retry
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
            "version_name": "17.4.0",
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10",
        }
        self.deal_url_params(params)
        if not (
                board := self.send_request(
                    self.hot_api,
                    params=params,
                )):
            self.log.warning(f"获取 {data.name} 数据失败")
            return False
        try:
            self.response.append((index, board["data"]["word_list"]))
            return True
        except KeyError:
            self.log.error(f"{data.name} 数据响应内容异常: {board}")
            return False


class Collection(Acquirer):
    collection_api = "https://www.douyin.com/aweme/v1/web/aweme/listcollection/"  # 收藏API
    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "publish_video_strategy_type": "2",
        "pc_client_type": "1",
        "version_code": "170400",
        "version_name": "17.4.0",
        "cookie_enabled": "true",
        "platform": "PC",
        "downlink": "10",
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
                self._get_account_data(finished=True)
                self.pages -= 1
        self._get_owner_data()
        return self.response

    @retry
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
                    method='post')):
            self.log.warning("获取账号收藏数据失败")
            return False
        try:
            self.cursor = data['cursor']
            self.deal_item_data(data["aweme_list"])
            self.finished = not data["has_more"]
            return True
        except KeyError:
            self.log.error(f"账号收藏数据响应内容异常: {data}")
            self.finished = True
            return False

    def _get_owner_data(self):
        if not any(self.response):
            return
        if self.sec_user_id and (
                info := Extractor.get_user_info(
                    self.info.run())):
            self.response.append({"author": info})
        else:
            temp_data = timestamp()
            self.log.warning(f"owner_url 参数未设置 或者 获取账号数据失败，本次运行将临时使用 {
            temp_data} 作为账号昵称和 UID")
            temp_dict = {
                "author": {
                    "nickname": temp_data,
                    "uid": temp_data,
                }
            }
            self.response.append(temp_dict)


class Info(Acquirer):
    info_api = "https://www.douyin.com/aweme/v1/web/im/user/info/"  # 账号简略数据API

    def __init__(
            self,
            params: Parameter,
            sec_user_id: str,
            cookie: str = None):
        super().__init__(params, cookie)
        self.sec_user_id = sec_user_id
        self.params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "pc_client_type": "1",
            "version_code": "170400",
            "version_name": "17.4.0",
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10",
        }

    @retry
    def run(self) -> dict:
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
            return {}
