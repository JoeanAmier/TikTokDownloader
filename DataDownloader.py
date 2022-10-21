import os
import time
from string import whitespace

import requests

from DataAcquirer import sleep
from StringCleaner import Cleaner


class Download:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37"}
        self.video_id_api = "https://aweme.snssdk.com/aweme/v1/play/"
        self.item_ids_api = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/"
        self.type_ = {"video": "", "images": ""}
        self.clean = Cleaner()
        self._root = None
        self._name = None
        self._time = None
        self._split = None
        self._folder = None
        self.music = False
        self.video_data = []
        self.image_data = []
        self.illegal = "".join(self.clean.replace.keys()) + whitespace

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        if value:
            try:
                _ = time.strftime(value, time.localtime())
                self._time = value
            except ValueError:
                print("时间格式错误，将使用默认时间格式（2022-11-11 11:11:11）")
                self._time = "%Y-%m-%d"
        else:
            print("时间格式错误，将使用默认时间格式（2022-11-11 11:11:11）")
            self._time = "%Y-%m-%d"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value:
            dict_ = {
                "id": 0,
                "desc": 1,
                "create_time": 2,
                "author": 3,
            }
            name = value.strip().split(" ")
            try:
                self._name = [dict_[i] for i in name]
            except KeyError:
                print("命名格式错误，将使用默认命名格式（创建时间 作者 描述）")
                self._name = [2, 3, 1]
        else:
            print("命名格式错误，将使用默认命名格式（创建时间 作者 描述）")
            self._name = [2, 3, 1]

    def get_name(self, data: list) -> str:
        return self.clean.filter(self.split.join(data[i] for i in self.name))

    @property
    def split(self):
        return self._split

    @split.setter
    def split(self, value):
        if value:
            for s in value:
                if s in self.illegal:
                    print("无效的文件命名分隔符！默认使用“-”作为分隔符！")
                    self._split = "-"
                    return
            self._split = value
        else:
            print("无效的文件命名分隔符！默认使用“-”作为分隔符！")
            self._split = "-"

    @property
    def folder(self):
        return self._folder

    @folder.setter
    def folder(self, value):
        if value:
            for s in value:
                if s in self.illegal:
                    print("无效的下载文件夹名称！默认使用“Download”作为下载文件夹名称！")
                    self._folder = "Download"
                    return
            self._folder = value
        else:
            print("无效的下载文件夹名称！默认使用“Download”作为下载文件夹名称！")
            self._folder = "Download"

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        if os.path.exists(value) and os.path.isdir(value):
            self._root = value
        else:
            print("文件保存路径错误！将使用当前路径作为保存路径！")
            self._root = "./"

    def create_folder(self, author):
        if not author:
            return False
        root = os.path.join(self.root, self.clean.filter(author))
        if not os.path.exists(root):
            os.mkdir(root)
        self.type_["video"] = os.path.join(root, "video")
        if not os.path.exists(self.type_["video"]):
            os.mkdir(self.type_["video"])
        self.type_["images"] = os.path.join(root, "images")
        if not os.path.exists(self.type_["images"]):
            os.mkdir(self.type_["images"])
        return True

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
                self.time,
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
                self.time,
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
        root = self.type_["images"]
        for item in self.image_data:
            for index, image in enumerate(item[4]):
                with requests.get(
                        image,
                        stream=True,
                        headers=self.headers) as response:
                    sleep()
                    name = self.get_name(item)
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
        root = self.type_["video"]
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
                name = self.get_name(item)
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
        if self.create_folder(author):
            self.get_video(video)
            self.get_image(image)
            self.download_video()
            self.download_images()
        else:
            print("Invalid user name!")

    def run_alone(self, id_: str):
        self.create_folder(self.folder)
        data = self.get_data(id_)
        if data["images"]:
            self.get_image([id_])
            self.download_images()
        else:
            self.get_video([id_])
            self.download_video()


if __name__ == "__main__":
    video_data = []
    image_data = []
    demo = Download()
    demo.music = True
    demo.root = ""
    demo.name = ""
    demo.time = ""
    demo.split = ""
    demo.run("Demo", video_data, image_data)
