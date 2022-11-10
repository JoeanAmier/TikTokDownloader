import random
import re
import time
from urllib.parse import urlparse

import requests

from Recorder import Logger


def sleep():
    time.sleep(random.randrange(10, 55, 5) * 0.1)


def reset(function):
    def inner(self, *args, **kwargs):
        self.id_ = None
        return function(self, *args, **kwargs)

    return inner


class UserData:
    def __init__(self, log: Logger):
        self.log = log
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37"}
        self.id_ = None  # sec_uid or item_ids
        self.max_cursor = 0
        self.list = None  # 未处理的数据
        self.name = None  # 账号昵称
        self.video_data = []  # 视频ID数据
        self.image_data = []  # 图集ID数据
        self.finish = False  # 是否获取完毕
        self.share = re.compile(
            r".*?(https://v\.douyin\.com/[A-Za-z0-9]+?/).*?")  # 分享短链
        self.account_link = re.compile(
            r"^https://www\.douyin\.com/user/([a-zA-z0-9-_]+)\??.*?$")  # 账号链接
        self.works_link = re.compile(
            r"^https://www\.douyin\.com/(?:video|note)/([0-9]{19})$")  # 作品链接
        self._url = None  # 账号链接
        self._api = None  # 批量下载类型

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
            self.id_ = s[0]
            self.log.info(f"当前账号链接: {value}", False)
        else:
            self.log.warning(f"无效的账号链接: {value}")

    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, value):
        if value in ("post", "like"):
            self._api = f"https://www.iesdouyin.com/web/api/v2/aweme/{value}/"
        else:
            self.log.warning(f"批量下载类型错误！必须设置为“post”或者“like”，错误值: {value}")

    def get_id(self, value="sec_uid", url=None):
        if self.id_:
            self.log.info(f"{self.url} {value}: {self.id_}", False)
            return True
        url = url or self.url
        response = requests.get(url, headers=self.headers, timeout=10)
        sleep()
        if response.status_code == 200:
            params = urlparse(response.url)
            self.id_ = params.path.split("/")[-1]
            self.log.info(f"{url} {value}: {self.id_}", False)
        else:
            self.log.error(
                f"{url} 响应码异常：{response.status_code}，获取 {value} 失败！")

    def get_user_data(self):
        params = {
            "sec_uid": self.id_,
            "max_cursor": self.max_cursor,
            "count": "35"}
        response = requests.get(
            self.api,
            params=params,
            headers=self.headers,
            timeout=10)
        sleep()
        if response.status_code == 200:
            data = response.json()
            self.max_cursor = data['max_cursor']
            self.list = data["aweme_list"]
        else:
            self.log.error(f"响应码异常：{response.status_code}，获取JSON数据失败！")

    def deal_data(self):
        if len(self.list) == 0:
            self.log.info("该账号的资源信息已获取完毕！")
            self.finish = True
        else:
            self.name = self.list[0]["author"]["nickname"]
            for item in self.list:
                if len(item["video"]["play_addr"]["url_list"]) < 4:
                    self.image_data.append(item["aweme_id"])
                else:
                    self.video_data.append(item["aweme_id"])

    def summary(self):
        self.log.info(f"账号 {self.name} 的视频总数: {len(self.video_data)}")
        for i in self.video_data:
            self.log.info(f"视频: {i}", False)
        self.log.info(f"账号 {self.name} 的图集总数: {len(self.image_data)}")
        for i in self.image_data:
            self.log.info(f"图集: {i}", False)

    def run(self):
        if not self.api or not self.url:
            self.log.warning("账号链接或批量下载类型设置无效！")
            return False
        self.log.info("正在获取账号数据！")
        self.get_id()
        if not self.id_:
            self.log.error("获取账号 sec_uid 失败！")
            return False
        while not self.finish:
            self.get_user_data()
            self.deal_data()
        self.summary()
        self.log.info("获取账号数据成功！")
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
            return True
        elif len(s := self.share.findall(url)) == 1:
            return s[0]
        return False
