import requests


class Downloader:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37"}
        self.video_id_api = "https://aweme.snssdk.com/aweme/v1/play/"
        self.item_ids_api = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/"

    def download_video_id(self, data):
        for item in data:
            params = {
                "video_id": item,
                "ratio": "1080p",
            }
            response = requests.get(
                self.video_id_api,
                params=params,
                headers=self.headers)

    def download_item_ids(self, data):
        for item in data:
            params = {
                "video_id": item,
                "ratio": "1080p",
            }
            response = requests.get(
                self.item_ids_api,
                params=params,
                headers=self.headers)

    def download_image(self, url):
        pass
