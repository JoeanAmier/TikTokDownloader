import random
import re
import time
from datetime import date
from datetime import datetime
from urllib.parse import urlencode
from urllib.parse import urlparse

import requests

from src.Parameter import MsToken
from src.Parameter import TtWid
from src.Parameter import XBogus
from src.Recorder import LoggerManager
from src.StringCleaner import Cleaner


def sleep():
    """避免频繁请求"""
    time.sleep(random.randrange(15, 55, 5) * 0.1)


def reset(function):
    """重置数据"""

    def inner(self, *args, **kwargs):
        if not isinstance(self.url, bool):
            self.id_ = None
        self.data = None
        self.comment = []
        self.reply = []
        self.mix_total = []
        self.mix_data = []
        self.cursor = 0
        self.max_cursor = 0
        self.list = []  # 未处理的数据
        self.name = None  # 账号昵称
        self.video_data = []  # 视频ID数据
        self.image_data = []  # 图集ID数据
        self.finish = False  # 是否获取完毕
        return function(self, *args, **kwargs)

    return inner


def check_cookie(function):
    """检查是否设置了Cookie"""

    def inner(self, *args, **kwargs):
        if self.cookie:
            return function(self, *args, **kwargs)
        print("未设置Cookie！")
        return False

    return inner


def retry(max_num=10):
    """发生错误时尝试重新执行，装饰的函数需要返回布尔值"""

    def inner(function):
        def execute(self, *args, **kwargs):
            for i in range(max_num):
                if r := function(self, *args, **kwargs):
                    return r

        return execute

    return inner


class UserData:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        'referer': 'https://www.douyin.com/',
    }
    share = re.compile(
        r".*?(https://v\.douyin\.com/[A-Za-z0-9]+?/).*?")  # 分享短链
    account_link = re.compile(
        r"^https://www\.douyin\.com/user/([a-zA-z0-9-_]+)(?:\?modal_id=([0-9]{19}))?.*$")  # 账号链接
    works_link = re.compile(
        r"^https://www\.douyin\.com/(?:video|note)/([0-9]{19})$")  # 作品链接
    live_link = re.compile(r"^https://live\.douyin\.com/([0-9]+)")  # 直播链接
    live_api = "https://live.douyin.com/webcast/room/web/enter/"  # 直播API
    comment_api = "https://www.douyin.com/aweme/v1/web/comment/list/"  # 评论API
    reply_api = "https://www.douyin.com/aweme/v1/web/comment/list/reply/"  # 评论回复API
    collection_api = "https://www.douyin.com/aweme/v1/web/aweme/listcollection/"  # 收藏API
    mix_api = "https://www.douyin.com/aweme/v1/web/mix/aweme/"  # 合集API
    mix_list_api = "https://www.douyin.com/aweme/v1/web/mix/listcollection/"  # 合集列表API
    info_api = "https://www.douyin.com/aweme/v1/web/im/user/info/"  # 账号简略数据API
    feed_api = "https://www.douyin.com/aweme/v1/web/tab/feed/"  # 推荐页API
    user_api = "https://www.douyin.com/aweme/v1/web/user/profile/other/"  # 账号详细数据API
    hot_api = "https://www.douyin.com/aweme/v1/web/hot/search/list/"  # 热点API
    spotlight_api = "https://www.douyin.com/aweme/v1/web/im/spotlight/relation/"  # 关注账号API
    familiar_api = "https://www.douyin.com/aweme/v1/web/familiar/feed/"  # 朋友作品推荐API
    follow_api = "https://www.douyin.com/aweme/v1/web/follow/feed/"  # 关注账号作品推荐API
    history_api = "https://www.douyin.com/aweme/v1/web/history/read/"  # 观看历史API
    clean = Cleaner()  # 过滤非法字符
    xb = XBogus()  # 加密参数对象
    max_comment = 256  # 评论字数限制

    def __init__(self, log: LoggerManager):
        self.log = log  # 日志记录对象
        self.data = None  # 数据记录对象，仅评论抓取调用
        self._cookie = False  # 是否设置了Cookie
        self.id_ = None  # sec_uid or item_ids
        self.comment = []  # 评论数据
        self.cursor = 0  # 评论和合集使用
        self.reply = []  # 评论回复的ID列表
        self.mix_total = []  # 合集作品数据
        self.mix_data = []  # 合集作品数据未处理JSON
        self.max_cursor = 0  # 发布页和喜欢页使用
        self.has_more = 0  # 下一页分页标志
        self.list = []  # 未处理的数据
        self.name = None  # 账号昵称
        self.video_data = []  # 视频ID数据
        self.image_data = []  # 图集ID数据
        self.finish = False  # 是否获取完毕
        self.favorite = False  # 喜欢页下载模式
        self._earliest = None  # 最早发布时间
        self._latest = None  # 最晚发布时间
        self._url = None  # 账号链接
        self._api = None  # 批量下载类型
        self._proxies = None  # 代理
        self._time = None  # 创建时间格式

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if self.share.match(value):
            self._url = value
            self.log.info(f"当前账号链接: {value}", False)
        elif len(s := self.account_link.findall(value)) == 1:
            self._url = True
            self.id_ = s[0][0]
            self.log.info(f"当前账号链接: {value}", False)
        else:
            self.log.warning(f"无效的账号链接: {value}")

    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, value):
        if value == "post":
            self._api = f"https://www.douyin.com/aweme/v1/web/aweme/{value}/"
            self.favorite = False
        elif value == "favorite":
            self._api = f"https://www.douyin.com/aweme/v1/web/aweme/{value}/"
            self.favorite = True
        else:
            self.log.warning(f"批量下载类型错误！必须设置为“post”或者“favorite”，错误值: {value}")

    @property
    def cookie(self):
        return self._cookie

    @cookie.setter
    def cookie(self, cookie: str):
        if not cookie:
            return
        if isinstance(cookie, str):
            self.headers["Cookie"] = cookie
            for i in (MsToken.get_ms_token(), TtWid.get_TtWid(),):
                self.headers["Cookie"] += f"; {i}"
            self._cookie = True

    @property
    def earliest(self):
        return self._earliest

    @earliest.setter
    def earliest(self, value):
        if not value:
            self._earliest = date(2016, 9, 20)
            return
        try:
            self._earliest = datetime.strptime(
                value, "%Y/%m/%d").date()
            self.log.info(f"作品最早发布日期: {value}")
        except ValueError:
            self.log.warning("作品最早发布日期无效")

    @property
    def latest(self):
        return self._latest

    @latest.setter
    def latest(self, value):
        if not value:
            self._latest = date.today()
            return
        try:
            self._latest = datetime.strptime(value, "%Y/%m/%d").date()
            self.log.info(f"作品最晚发布日期: {value}")
        except ValueError:
            self.log.warning("作品最晚发布日期无效")

    @property
    def proxies(self):
        return self._proxies

    @proxies.setter
    def proxies(self, value):
        if value and isinstance(value, str):
            test = {
                "http": value,
                "https": value,
                "ftp": value
            }
            try:
                response = requests.get(
                    "https://www.baidu.com/", proxies=test, timeout=10)
                if response.status_code == 200:
                    self.log.info("代理测试通过")
                    self._proxies = test
                    return
            except requests.exceptions.ReadTimeout:
                self.log.warning("代理测试超时")
            except requests.exceptions.ProxyError:
                self.log.warning("代理测试失败")
        self._proxies = {
            "http": None,
            "https": None,
            "ftp": None,
        }

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        if value:
            try:
                _ = time.strftime(value, time.localtime())
                self._time = value
                self.log.info(f"时间格式设置成功: {value}", False)
            except ValueError:
                self.log.warning(f"时间格式错误: {value}，将使用默认时间格式(年-月-日 时.分.秒)")
                self._time = "%Y-%m-%d %H.%M.%S"
        else:
            self.log.warning("错误的时间格式，将使用默认时间格式(年-月-日 时.分.秒)")
            self._time = "%Y-%m-%d %H.%M.%S"

    @retry(max_num=5)
    def get_id(self, value="sec_user_id", url=""):
        """获取账号ID或者作品ID"""
        if self.id_:
            self.log.info(f"{url} {value}: {self.id_}", False)
            return True
        url = url or self.url
        try:
            response = requests.get(
                url,
                headers=self.headers,
                proxies=self.proxies,
                timeout=10)
            sleep()
        except requests.exceptions.ReadTimeout:
            return False
        if response.status_code == 200:
            params = urlparse(response.url)
            url_list = params.path.rstrip("/").split("/")
            self.id_ = url_list[-1] or url_list[-2]
            self.log.info(f"{url} {value}: {self.id_}", False)
            return True
        else:
            self.log.error(
                f"{url} 响应码异常：{response.status_code}，获取 {value} 失败")
            return False

    def deal_params(self, params: dict) -> dict:
        xb = self.xb.get_x_bogus(urlencode(params))
        params["X-Bogus"] = xb
        return params

    @retry(max_num=5)
    def get_user_data(self):
        """获取账号作品数据"""
        params = {
            "aid": "6383",
            "sec_user_id": self.id_,
            "count": "35",
            "max_cursor": self.max_cursor,
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10",
        }
        params = self.deal_params(params)
        try:
            response = requests.get(
                self.api,
                params=params,
                headers=self.headers,
                proxies=self.proxies,
                timeout=10)
            sleep()
        except requests.exceptions.ReadTimeout:
            self.log.error("获取账号作品数据超时")
            return False
        if response.status_code == 200:
            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                self.log.error("账号作品数据返回内容异常！疑似接口失效", False)
                return False
            try:
                self.max_cursor = data['max_cursor']
                self.list = data["aweme_list"]
                self.has_more = data["has_more"]
                return True
            except KeyError:
                self.log.error(f"账号作品数据响应内容异常: {data}", False)
                return False
        else:
            self.log.error(f"响应码异常：{response.status_code}，获取账号作品数据失败")
            return False

    def deal_data(self):
        """对账号作品进行分类"""
        if self.has_more == 0:
            self.log.info("该账号的资源信息获取结束")
            self.finish = True

        # 该分页无数据
        if len(self.list) == 0:
            return
        # 该分页有数据
        if len(self.list) > 0:
            self.name = self.clean.filter(self.list[0]["author"]["nickname"])
            for item in self.list:
                if item["images"]:
                    self.image_data.append(
                        [item["create_time"], item])
                else:
                    self.video_data.append(
                        [item["create_time"], item])

    def summary(self):
        """汇总账号作品数量"""
        self.log.info(f"账号 {self.name} 的视频总数: {len(self.video_data)}")
        for i in self.video_data:
            self.log.info(
                f"视频: {i['aweme_id']} {i['video']['play_addr']['uri']}", False)
        self.log.info(f"账号 {self.name} 的图集总数: {len(self.image_data)}")
        for i in self.image_data:
            self.log.info(f"图集: {i['aweme_id']}", False)

    @retry(max_num=5)
    def get_nickname(self):
        """喜欢页下载模式需要额外发送请求获取账号昵称"""
        params = {
            "aid": "6383",
            "sec_user_id": self.id_,
            "count": "35",
            "max_cursor": 0,
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10",
        }
        params = self.deal_params(params)
        try:
            response = requests.get(
                self.api.replace("favorite", "post"),
                params=params,
                headers=self.headers,
                proxies=self.proxies,
                timeout=10)
            sleep()
        except requests.exceptions.ReadTimeout:
            self.name = str(time.time())[:10]
            self.log.warning(
                f"请求超时，获取账号昵称失败，本次运行将默认使用当前时间戳作为帐号昵称: {self.name}")
            return False
        if response.status_code == 200:
            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                self.name = str(time.time())[:10]
                self.log.warning(
                    f"数据接口返回内容异常，获取账号昵称失败，本次运行将默认使用当前时间戳作为帐号昵称: {self.name}")
                return False
            try:
                self.name = self.clean.filter(
                    data["aweme_list"][0]["author"]["nickname"]) or str(
                    time.time())[
                                                                    :10]
                return True
            except KeyError:
                self.name = str(time.time())[:10]
                self.log.warning(
                    f"响应内容异常，获取账号昵称失败，本次运行将默认使用当前时间戳作为帐号昵称: {self.name}")
                return False
        else:
            self.name = str(time.time())[:10]
            self.log.warning(
                f"响应码异常：{response.status_code}，获取账号昵称失败，本次运行将默认使用当前时间戳作为帐号昵称: {self.name}")
            return False

    def early_stop(self):
        """如果获取数据的发布日期已经早于限制日期，就不需要再获取下一页的数据了"""
        if not self.favorite:
            return
        if self.earliest > datetime.fromtimestamp(
                self.max_cursor / 1000).date():
            self.finish = True

    def get_user_id(self, index=0):
        if index and not all(
                (self.api,
                 self.url,
                 self.earliest,
                 self.latest,)):
            self.log.warning("请检查账号链接、批量下载类型、最早发布日期、最晚发布日期是否正确")
            return False
        self.get_id()
        if not self.id_:
            self.log.error("获取账号 sec_user_id 失败")
            return False
        return True

    @reset
    @check_cookie
    def run(self, index: int):
        """批量下载模式"""
        self.log.info(f"正在获取第 {index} 个账号数据")
        if not self.get_user_id(index):
            return False
        while not self.finish:
            self.get_user_data()
            self.deal_data()
            self.early_stop()
        if self.favorite:
            self.get_nickname()
        if not self.name:
            self.log.error(f"获取第 {index} 个账号数据失败，请稍后重试")
            return False
        self.date_filters()
        self.summary()
        self.log.info(f"获取第 {index} 个账号数据成功")
        return True

    @reset
    @check_cookie
    def run_alone(self, text: str):
        """单独下载模式"""
        url = self.check_url(text)
        if not url:
            self.log.warning(f"无效的作品链接: {url}")
            return False
        self.get_id("aweme_id", url)
        return self.id_ or False

    def check_url(self, url: str):
        if len(s := self.works_link.findall(url)) == 1:
            self.id_ = s[0]
            return url
        elif len(s := self.share.findall(url)) == 1:
            return s[0]
        elif len(s := self.account_link.findall(url)) == 1:
            if s := s[0][1]:
                self.id_ = s
                return url
        return False

    def date_filters(self):
        """筛选发布时间"""
        earliest_date = self.earliest
        latest_date = self.latest
        filtered = []
        for item in self.video_data:
            date_ = datetime.fromtimestamp(item[0]).date()
            if earliest_date <= date_ <= latest_date:
                filtered.append(item[1])
        self.video_data = filtered
        filtered = []
        for item in self.image_data:
            date_ = datetime.fromtimestamp(item[0]).date()
            if earliest_date <= date_ <= latest_date:
                filtered.append(item[1])
        self.image_data = filtered

    def get_live_id(self, link: str):
        """检查直播链接并返回直播ID"""
        return s[0] if len(s := self.live_link.findall(link)) == 1 else None

    @check_cookie
    def get_live_data(self, link: str):
        id_ = self.get_live_id(link)
        if not id_:
            self.log.warning(f"直播链接格式错误: {link}")
            return False
        params = {
            "aid": "6383",
            "device_platform": "web",
            "web_rid": id_
        }
        params = self.deal_params(params)
        try:
            response = requests.get(
                self.live_api,
                headers=self.headers,
                params=params,
                timeout=10,
                proxies=self.proxies)
            sleep()
            return r if (r := response.json()) else False
        except requests.exceptions.ReadTimeout:
            self.log.warning("获取直播数据超时")
            return False
        except requests.exceptions.JSONDecodeError:
            self.log.warning("直播数据内容格式错误")
            return False

    def deal_live_data(self, data):
        try:
            if data["data"]["data"][0]["status"] == 4:
                self.log.info("当前直播已结束")
                return None
            nickname = self.clean.filter(
                data["data"]["data"][0]["owner"]["nickname"])
            title = self.clean.filter(data["data"]["data"][0]["title"])
            url = data["data"]["data"][0]["stream_url"]["flv_pull_url"]
            cover = data["data"]["data"][0]["cover"]["url_list"][0]
            return nickname, title, url, cover
        except KeyError as e:
            self.log.error(f"发生错误: {e}, 数据: {data}")
            return None

    @reset
    @check_cookie
    def run_comment(self, id_: str, data):
        self.data = data
        while not self.finish:
            self.get_comment(id_, self.comment_api)
            self.deal_comment()
        self.log.info("开始获取楼中楼评论数据")
        for item in self.reply:
            self.finish = False
            self.cursor = 0
            while not self.finish:
                self.get_comment(id_, self.reply_api, item)
                self.deal_comment()

    @retry(max_num=5)
    def get_comment(self, id_: str, api: str, reply=""):
        """获取评论数据"""
        if reply:
            params = {
                "aid": "6383",
                "item_id": id_,
                "comment_id": reply,
                "cursor": self.cursor,
                "count": "3",  # 每次返回数据的数量
                "cookie_enabled": "true",
                "platform": "PC",
            }
        else:
            params = {
                "aid": "6383",
                "aweme_id": id_,
                "cursor": self.cursor,
                "count": "20",
                "cookie_enabled": "true",
                "platform": "PC", }
        params = self.deal_params(params)
        try:
            response = requests.get(
                api,
                params=params,
                headers=self.headers,
                proxies=self.proxies,
                timeout=10)
            sleep()
        except requests.exceptions.ReadTimeout:
            self.log.error("获取评论数据超时")
            return False
        if response.status_code == 200:
            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                self.log.error("评论数据返回内容异常！疑似接口失效", False)
                return False
            try:
                self.comment = data["comments"]
                self.cursor = data["cursor"]
                return True
            except KeyError:
                self.log.error(f"评论数据内容异常: {data}", False)
                return False
        else:
            self.log.error(f"响应码异常：{response.status_code}，获取评论数据失败")
            return False

    def deal_comment(self):
        if not self.comment:
            self.log.info("评论数据获取结束")
            self.finish = True
            return
        for item in self.comment:
            """数据格式: 采集时间, 评论ID, 评论时间, 用户昵称, IP归属地, 评论内容, 评论图片, 点赞数量, 回复数量, 回复ID"""
            collection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            create_time = time.strftime(
                self.time,
                time.localtime(
                    item["create_time"]))
            ip_label = item["ip_label"]
            text = item["text"][:self.max_comment]
            if images := item.get("image_list", False):
                images = images[0]["origin_url"]["url_list"][0]  # 图片链接
            else:
                images = "#"
            nickname = item["user"]["nickname"]
            digg_count = str(item["digg_count"])
            cid = item["cid"]
            reply_comment_total = item.get("reply_comment_total", -1)
            if reply_comment_total > 0:
                self.reply.append(cid)
            reply_comment_total = str(reply_comment_total)
            reply_id = item["reply_id"]
            result = [
                collection_time,
                cid,
                create_time,
                nickname,
                ip_label,
                text,
                images,
                digg_count,
                reply_comment_total,
                reply_id]
            self.log.info("评论: " + ", ".join(result))
            self.data.save(result)

    @reset
    @check_cookie
    def run_mix(self, data):
        info = self.get_mix_id(data)
        if not info:
            return False
        while not self.finish:
            self.get_mix_data(info[0])
            self.deal_mix_data()
        self.log.info("合集作品数据提取结束")
        # 如果合集名称去除非法字符后为空字符串，则使用当前时间戳作为合集标识
        return f"合集_{self.clean.filter(info[1]) or str(time.time())[:10]}"

    @staticmethod
    def get_mix_id(data):
        data = data.get("mix_info", False)
        return (data["mix_id"], data["mix_name"]) if data else data

    @retry(max_num=5)
    def get_mix_data(self, id_):
        """获取合集作品数据"""
        params = {"aid": "6383",
                  "mix_id": id_,
                  "cursor": self.cursor,
                  "count": "20",
                  "cookie_enabled": "true",
                  "platform": "PC", }
        params = self.deal_params(params)
        try:
            response = requests.get(
                self.mix_api,
                params=params,
                headers=self.headers,
                proxies=self.proxies,
                timeout=10)
            sleep()
        except requests.exceptions.ReadTimeout:
            self.log.error("获取合集作品数据超时")
            return False
        if response.status_code == 200:
            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                self.log.error("合集作品数据返回内容异常！疑似接口失效", False)
                return False
            try:
                self.cursor = data['cursor']
                self.mix_data = data["aweme_list"]
                self.finish = not data["has_more"]
                return True
            except KeyError:
                self.log.error(f"合集作品数据内容异常: {data}", False)
                return False
        else:
            self.log.error(f"响应码异常：{response.status_code}，获取合集作品数据失败")
            return False

    def deal_mix_data(self):
        for item in self.mix_data:
            self.mix_total.append(item)

    @reset
    @check_cookie
    def run_user(self):
        if not self.get_user_id():
            return False
        return self.deal_user(data) if (
            data := self.get_user_info()) else False

    @retry(max_num=5)
    def get_user_info(self):
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "sec_user_id": self.id_,
            "cookie_enabled": "true",
            "platform": "PC",
        }
        params = self.deal_params(params)
        try:
            response = requests.get(
                self.user_api,
                params=params,
                headers=self.headers,
                proxies=self.proxies,
                timeout=10)
            sleep()
        except requests.exceptions.ReadTimeout:
            self.log.error("获取账号数据超时")
            return False
        if response.status_code == 200:
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                self.log.error("账号数据内容异常！疑似接口失效", False)
                return False
        else:
            self.log.error(f"响应码异常：{response.status_code}，获取账号数据失败")
            return False

    @staticmethod
    def deal_user(data):
        data = data["user"]
        collection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 采集时间
        avatar_larger = data["avatar_larger"]["url_list"][0]  # 头像链接
        cover = c[0]["url_list"][0] if (
            c := data.get("cover_url")) else ""  # 背景图片链接
        favoriting_count = data["favoriting_count"]  # 喜欢作品数量
        follower_count = data["follower_count"]  # 粉丝数量
        following_count = data["following_count"]  # 关注数量
        max_follower_count = data["max_follower_count"]  # 粉丝数量最大值
        signature = data["signature"]  # 简介
        total_favorited = data["total_favorited"]  # 获赞数量
        nickname = data["nickname"]  # 账号昵称
        sec_uid = data["sec_uid"]
        unique_id = data["unique_id"]  # 抖音号
        short_id = data["short_id"]
        user_age = data["user_age"]  # 年龄
        aweme_count = data["aweme_count"]  # 作品数量
        room_data = data.get("room_data")  # 直播数据
        custom_verify = data["custom_verify"] or "无"  # 标签认证
        uid = data["uid"]
        enterprise = data["enterprise_verify_reason"] or "无"  # 企业认证
        return [
            collection_time,
            nickname,
            signature,
            unique_id,
            str(user_age),
            custom_verify,
            enterprise,
            sec_uid,
            uid,
            short_id,
            avatar_larger,
            cover,
            str(aweme_count),
            str(total_favorited),
            str(favoriting_count),
            str(follower_count),
            str(following_count),
            str(max_follower_count), ]

    def save_user(self, file, data):
        self.data = file
        self.log.info("账号数据: " + ", ".join(data), False)
        self.data.save(data, key=1)
        self.log.info("账号数据获取结束")
