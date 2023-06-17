import datetime
import random
import re
import time
from urllib.parse import urlencode
from urllib.parse import urlparse

import requests

from Parameter import XBogus
from Recorder import RunLogger


def sleep():
    """避免频繁请求"""
    time.sleep(random.randrange(10, 40, 5) * 0.1)


def reset(function):
    """重置数据"""

    def inner(self, *args, **kwargs):
        if not isinstance(self.url, bool):
            self.id_ = None
        self.max_cursor = 0
        self.list = None  # 未处理的数据
        self.name = None  # 账号昵称
        self.video_data = []  # 视频ID数据
        self.image_data = []  # 图集ID数据
        self.finish = False  # 是否获取完毕
        return function(self, *args, **kwargs)

    return inner


def retry(max_num=3):
    """发生错误时尝试重新执行"""

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

    def __init__(self, log: RunLogger, session=None):
        self.xb = XBogus()
        self.log = log
        self.session = self.check_session(session)
        self._cookie = False
        self.id_ = None  # sec_uid or item_ids
        self.max_cursor = 0
        self.list = None  # 未处理的数据
        self.name = None  # 账号昵称
        self.video_data = []  # 视频ID数据
        self.image_data = []  # 图集ID数据
        self.finish = False  # 是否获取完毕
        self._earliest = None
        self._latest = None
        self._url = None  # 账号链接
        self._api = None  # 批量下载类型

    @staticmethod
    def check_session(session):
        if not session:
            return requests.session()
        return session

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
        if value in ("post", "favorite"):
            self._api = f"https://www.douyin.com/aweme/v1/web/aweme/{value}/"
        else:
            self.log.warning(f"批量下载类型错误！必须设置为“post”或者“favorite”，错误值: {value}")

    @property
    def cookie(self):
        return self._cookie

    @cookie.setter
    def cookie(self, cookie):
        if isinstance(cookie, str):
            self.headers["Cookie"] = cookie
            self._cookie = True

    @property
    def earliest(self):
        return self._earliest

    @earliest.setter
    def earliest(self, value):
        if not value:
            self._earliest = datetime.date(2010, 1, 1)
            return
        try:
            self._earliest = datetime.datetime.strptime(
                value, "%Y/%m/%d").date()
            self.log.info(f"作品最早发布日期: {value}")
        except ValueError:
            self.log.warning("作品最早发布日期无效！")

    @property
    def latest(self):
        return self._latest

    @latest.setter
    def latest(self, value):
        if not value:
            self._latest = datetime.date.today()
            return
        try:
            self._latest = datetime.datetime.strptime(value, "%Y/%m/%d").date()
            self.log.info(f"作品最晚发布日期: {value}")
        except ValueError:
            self.log.warning("作品最晚发布日期无效！")

    @retry(max_num=5)
    def get_id(self, value="sec_uid", url=None):
        """获取账号ID或者作品ID"""
        if self.id_:
            self.log.info(f"{url} {value}: {self.id_}", False)
            return True
        url = url or self.url
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=10)
        except requests.exceptions.ReadTimeout:
            return False
        sleep()
        if response.status_code == 200:
            params = urlparse(response.url)
            self.id_ = params.path.rstrip("/").split("/")[-1]
            self.log.info(f"{url} {value}: {self.id_}", False)
            return True
        else:
            self.log.error(
                f"{url} 响应码异常：{response.status_code}，获取 {value} 失败！")
            return False

    @retry(max_num=5)
    def get_user_data(self):
        """获取账号作品信息"""
        params = {
            "aid": "6383",
            "sec_user_id": self.id_,
            "count": "35",
            "max_cursor": self.max_cursor,
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10",
        }
        xb = self.xb.get_x_bogus(urlencode(params))
        params["X-Bogus"] = xb
        try:
            response = requests.get(
                self.api,
                params=params,
                headers=self.headers,
                timeout=10)
        except requests.exceptions.ReadTimeout:
            return False
        sleep()
        if response.status_code == 200:
            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                self.list = []
                self.log.error("数据接口返回内容异常！疑似接口失效！", False)
                return False
            try:
                self.max_cursor = data['max_cursor']
                self.list = data["aweme_list"]
                return True
            except KeyError:
                self.list = []
                self.log.error(f"响应内容异常: {data}", False)
                return False
        else:
            self.list = []
            self.log.error(f"响应码异常：{response.status_code}，获取JSON数据失败！")
            return False

    def deal_data(self):
        """对账号作品进行分类"""
        if len(self.list) == 0:
            self.log.info("该账号的资源信息获取结束！")
            self.finish = True
        else:
            self.name = self.list[0]["author"]["nickname"]
            for item in self.list:
                if t := item["aweme_type"] == 68:
                    self.image_data.append(
                        [item["create_time"], item["aweme_id"]])
                elif t == 0:
                    self.video_data.append(
                        [item["create_time"], item["aweme_id"]])
                else:
                    self.log.warning(f"无法判断资源类型, 详细数据: {item}")

    def summary(self):
        """汇总账号作品数量"""
        self.log.info(f"账号 {self.name} 的视频总数: {len(self.video_data)}")
        for i in self.video_data:
            self.log.info(f"视频: {i[1]}", False)
        self.log.info(f"账号 {self.name} 的图集总数: {len(self.image_data)}")
        for i in self.image_data:
            self.log.info(f"图集: {i[1]}", False)

    @reset
    def run(self, index: int):
        if not all((self.api, self.url, self.earliest, self.latest)):
            self.log.warning("账号链接或批量下载类型设置无效！")
            return False
        self.log.info(f"正在获取第 {index} 个账号数据！")
        self.get_id()
        if not self.id_:
            self.log.error("获取账号 sec_uid 失败！")
            return False
        while not self.finish:
            self.get_user_data()
            self.deal_data()
        if not self.name:
            self.log.error("获取账号数据失败，请稍后重试！")
            return False
        self.date_filters()
        self.summary()
        self.log.info(f"获取第 {index} 个账号数据成功！")
        return True

    @reset
    def run_alone(self, text: str):
        url = self.check_url(text)
        if not url:
            self.log.warning("无效的作品链接！")
            return False
        self.get_id("item_ids", url)
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
        earliest_date = self.earliest
        latest_date = self.latest
        filtered = []
        for item in self.video_data:
            date = datetime.datetime.fromtimestamp(item[0]).date()
            if earliest_date <= date <= latest_date:
                filtered.append(item[1])
        self.video_data = filtered
        filtered = []
        for item in self.image_data:
            date = datetime.datetime.fromtimestamp(item[0]).date()
            if earliest_date <= date <= latest_date:
                filtered.append(item[1])
        self.image_data = filtered
