import os
import time

import requests

from DataAcquirer import sleep
from String_Cleaner import StringCleaner


class Download:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37"}
        self.video_id_api = "https://aweme.snssdk.com/aweme/v1/play/"
        self.item_ids_api = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/"
        self.root = {"video": "", "images": ""}
        self.clean = StringCleaner()
        self.rename = [2, 3, 1]
        self.music = False
        self.video_data = []
        self.image_data = []

    def set_rename(self, name):
        dict_ = {
            "id": 0,
            "desc": 1,
            "create_time": 2,
            "author": 3,
        }
        rename = name.split("-")
        self.rename = [dict_[i] for i in rename]

    def get_rename(self, data: list) -> str:
        return self.clean.filter("-".join(data[i] for i in self.rename))

    def create_folder(self, author, root="./"):
        if not author:
            return
        root = os.path.join(root, author)
        if not os.path.exists(root):
            os.mkdir(root)
        self.root["video"] = os.path.join(root, "video")
        if not os.path.exists(self.root["video"]):
            os.mkdir(self.root["video"])
        self.root["images"] = os.path.join(root, "images")
        if not os.path.exists(self.root["images"]):
            os.mkdir(self.root["images"])

    def get_data(self, item):
        params = {
            "item_ids": item,
        }
        response = requests.get(
            self.item_ids_api,
            params=params,
            headers=self.headers, timeout=10)
        sleep()
        return response.json()["item_list"][0]

    def get_video(self, data):
        for item in data:
            item = self.get_data(item)
            id_ = item["aweme_id"]
            desc = item["desc"] or id_
            create_time = time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(
                    item["create_time"]))
            author = item["author"]["nickname"]
            video_id = item["video"]["play_addr"]["uri"]
            music_title = item["music"]["title"]
            music = item["music"]["play_url"]["url_list"][0]
            self.video_data.append(
                [id_, desc, create_time, author, video_id, [music_title, music]])

    def get_image(self, data):
        for item in data:
            item = self.get_data(item)
            id_ = item["aweme_id"]
            desc = item["desc"] or id_
            create_time = time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(
                    item["create_time"]))
            author = item["author"]["nickname"]
            images = item["images"]
            images = [i['url_list'][3] for i in images]
            music_title = item["music"]["title"]
            music = item["music"]["play_url"]["url_list"][0]
            self.image_data.append(
                [id_, desc, create_time, author, images, [music_title, music]])

    def download_images(self):
        root = self.root["images"]
        for item in self.image_data:
            for index, image in enumerate(item[4]):
                with requests.get(
                        image,
                        stream=True,
                        headers=self.headers) as response:
                    sleep()
                    name = self.get_rename(item)
                    self.save_file(response, root, f"{name}_{index}", "webp")
            if self.music:
                with requests.get(
                        item[5][1],
                        stream=True,
                        headers=self.headers) as response:
                    sleep()
                    self.save_file(
                        response, root, self.clean.filter(
                            item[5][0]), "mp3")

    def download_video(self):
        root = self.root["video"]
        for item in self.video_data:
            params = {
                "video_id": item[4],
                "ratio": "1080p",
            }
            with requests.get(
                    self.video_id_api,
                    params=params,
                    stream=True,
                    headers=self.headers) as response:
                sleep()
                name = self.get_rename(item)
                self.save_file(response, root, name, "mp4")
            if self.music:
                with requests.get(
                        item[5][1],
                        stream=True,
                        headers=self.headers) as response:
                    sleep()
                    self.save_file(
                        response, root, self.clean.filter(
                            item[5][0]), "mp3")

    @staticmethod
    def save_file(data, root: str, name: str, file: str):
        with open(os.path.join(root, f"{name}.{file}"), "wb") as f:
            for chunk in data.iter_content(chunk_size=1048576):
                f.write(chunk)

    def run(self, author: str, video: list[str], image: list[str]):
        self.create_folder(author)
        if self.root:
            self.get_video(video)
            self.get_image(image)
            self.download_video()
            self.download_images()
        else:
            print("Invalid user name!")

    def run_alone(self, id_: str, author="Download"):
        self.create_folder(author)
        data = self.get_data(id_)
        if data["images"]:
            self.get_image([id_])
            self.download_images()
        else:
            self.get_video([id_])
            self.download_video()


if __name__ == "__main__":
    video_data = [
        '7151969548021845285',
        '7150201232915778847',
        '7147640146253368612',
        '7147564509018787079',
        '7147289039563951390']
    image_data = ['7153520963852799262', '7150543698709777694']
    demo = Download()
    demo.music = True
    demo.run("Demo", video_data, image_data)
    # print(demo.video_data)
    # print(demo.image_data)
    # demo.run_alone('7153520963852799262')
