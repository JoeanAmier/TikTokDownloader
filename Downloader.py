import json
import re

import requests

from String_Cleaner import StringCleaner


class Download:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.34'}
        self.android_headers = {'user-agent': 'Android'}

    def get_share_url(self, url):
        response = requests.get(
            url,
            headers=self.headers,
            allow_redirects=False)
        if 'location' in response.headers.keys():
            return response.headers['location']

    def get_data(self, url, vid):
        response = requests.get(url, headers=self.headers).text
        json_str = json.loads(response)
        download_url = json_str['item_list'][0]['video']['play_addr']['url_list'][0].replace(
            "playwm", "play")
        name = StringCleaner().filter(json_str["item_list"][0]["desc"]) or vid
        with open(f'{name}.mp4', 'wb') as f:
            f.write(
                requests.get(
                    url=download_url,
                    headers=self.android_headers).content)
        print('视频下载完成！')

    def run(self):
        share = input("请输入抖音短视频分享链接：")
        url = re.findall(r'https://v.douyin.com/.*?/', share)[0]
        if location := self.get_share_url(url):
            vid = re.findall(r'/share/video/(\d*?)/', location)[0]
            url = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={vid}'
            self.get_data(url, vid)
        else:
            print("解析失败！")


if __name__ == '__main__':
    Download().run()
