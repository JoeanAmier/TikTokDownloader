import random
import re
import time
from urllib.parse import urlparse

import requests

from Recorder import Logger


def sleep():
    time.sleep(random.randrange(10, 55, 5) * 0.1)


class UserData:
    def __init__(self, log: Logger):
        self.log = log
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37"}
        self.sec_uid = None
        self.max_cursor = 0
        self.list = None
        self.name = None
        self.video_data = []
        self.image_data = []
        self.finish = False
        self.share = re.compile(
            r".*?(https://v\.douyin\.com/[A-Za-z0-9]+?/).*?")
        self._url = None
        self._api = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if self.share.match(value):
            self._url = value
            self.log.info(f"当前分享链接: {value}")
        else:
            self.log.warning(f"无效的分享链接: {value}")

    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, value):
        if value in ("post", "like"):
            self._api = f"https://www.iesdouyin.com/web/api/v2/aweme/{value}/"
        else:
            self.log.warning(f"批量下载类型错误！必须设置为“post”或者“like”，错误值: {value}")

    def get_sec_uid(self):
        response = requests.get(self.url, headers=self.headers, timeout=10)
        sleep()
        if response.status_code == 200:
            params = urlparse(response.url)
            self.sec_uid = params.path.split("/")[-1]
            self.log.info(f"sec_uid: {self.sec_uid}")
        else:
            self.log.error(f"响应码异常：{response.status_code}，获取sec_uid失败！")

    def get_user_data(self):
        params = {
            "sec_uid": self.sec_uid,
            "max_cursor": self.max_cursor,
            "count": "20"}
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

    def run(self):
        if not self.api or not self.url:
            self.log.warning("分享链接或下载类型设置无效！")
            return False
        self.log.info("正在尝试获取账号数据！")
        self.get_sec_uid()
        if not self.sec_uid:
            self.log.error("获取 sec_uid 失败！")
            return False
        while not self.finish:
            self.get_user_data()
            self.deal_data()
        self.log.info(f"{self.name} 视频资源列表: {self.video_data}")
        self.log.info(f"{self.name} 图集资源列表: {self.image_data}")
        return True

    def run_alone(self, text: str):
        url = self.clean_url(text)
        if not url:
            self.log.warning("无效的分享链接！")
            return False
        self.url = url
        self.get_sec_uid()
        return self.sec_uid or False

    def clean_url(self, url: str):
        url = self.share.findall(url)
        return url[0] if len(url) == 1 else ""


if __name__ == '__main__':
    demo = UserData(Logger())
    demo.url = ""
    demo.api = "post"
    demo.run()
    print(demo.name)
    print(demo.video_data)
    print(demo.image_data)
