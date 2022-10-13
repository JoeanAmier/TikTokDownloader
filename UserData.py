import re

import requests


class UserData:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37"}
        self.api = "https://www.iesdouyin.com/web/api/v2/aweme/post/"
        self.sec_uid = None
        self.max_cursor = 0
        self.json = None
        self.name = None
        self.data = None
        self.finish = False
        self._url = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if re.match(r'https://v\.douyin\.com/[A-Za-z0-9]+/$', value):
            self._url = value

    def get_sec_uid(self):
        response = requests.get(self.url, headers=self.headers, timeout=10)
        if len(
                sec_uid := re.match(
                    r'https://www\.douyin\.com/user/(.*?)\?previous_page=web_code_link$',
                    response.url).groups()) == 1:
            self.sec_uid = sec_uid[0]

    def get_user_data(self):
        params = {
            "sec_uid": self.sec_uid,
            "max_cursor": self.max_cursor,
            "count": "35"}
        response = requests.get(
            self.api,
            params=params,
            headers=self.headers,
            timeout=10)
        if response.status_code == 200:
            data = response.json()
            self.max_cursor = data['max_cursor']
            self.json = data["aweme_list"]

    def deal_data(self):
        if len(self.json) == 0:
            return False

    def run(self):
        if not self.url:
            return False
        self.get_sec_uid()
        if not self.sec_uid:
            return False
        while not self.finish:
            self.get_user_data()
            if not self.json:
                return False
            self.deal_data()


if __name__ == '__main__':
    demo = UserData()
    demo.url = "https://v.douyin.com/MYnH9Jm/"
    demo.run()
