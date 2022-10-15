import re

import requests

from main import sleep


class UserData:
    def __init__(self):
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
        self._url = None
        self._api = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if re.match(r'https://v\.douyin\.com/[A-Za-z0-9]+/$', value):
            self._url = value

    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, value):
        if value in ("post", "like"):
            self._api = f"https://www.iesdouyin.com/web/api/v2/aweme/{value}/"

    def get_sec_uid(self):
        response = requests.get(self.url, headers=self.headers, timeout=10)
        sleep()
        if len(
                sec_uid := re.match(
                    r'https://www\.douyin\.com/user/(.*?)\?previous_page=(?:web|app)_code_link$',
                    response.url).groups()) == 1:
            self.sec_uid = sec_uid[0]

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

    def deal_data(self):
        if len(self.list) == 0:
            self.finish = True
            return False
        self.name = self.list[0]["author"]["nickname"]
        for item in self.list:
            if len(item["video"]["play_addr"]["url_list"]) < 4:
                self.image_data.extend([item["desc"], item["aweme_id"]])
            else:
                self.video_data.extend([item["desc"], item["aweme_id"]])

    def run(self):
        if not self.api or not self.url:
            return False
        self.get_sec_uid()
        if not self.sec_uid:
            return False
        while not self.finish:
            self.get_user_data()
            if not self.list:
                return False
            self.deal_data()


if __name__ == '__main__':
    demo = UserData()
    demo.url = "https://v.douyin.com/MYnH9Jm/"  # 发布页测试一
    # demo.url = "https://v.douyin.com/MhgkDKs/"  # 发布页测试二
    # demo.url = "https://v.douyin.com/MhqA5A1/"  # 喜欢页测试
    demo.api = "post"
    demo.run()
    print(demo.name)
    print(demo.video_data)
    print(demo.image_data)
