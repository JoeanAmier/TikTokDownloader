import os
import time
from datetime import datetime
from urllib.parse import urlencode

import requests

from src.DataAcquirer import check_cookie
from src.DataAcquirer import retry
from src.DataAcquirer import sleep
from src.Parameter import MsToken
from src.Parameter import TtWid
from src.Parameter import XBogus
from src.Recorder import LoggerManager
from src.StringCleaner import Cleaner


def reset(function):
    """重置数据"""

    def inner(self, *args, **kwargs):
        self.type_ = {"video": "", "images": ""}  # 文件保存目录
        self.video_data = []
        self.image_data = []
        self.video = 0  # 视频下载数量
        self.image = 0  # 图集下载数量
        self.mix_data = []
        self.image_id = None  # 临时记录图集ID，用于下载计数
        return function(self, *args, **kwargs)

    return inner


class Download:
    UA = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    }  # 下载请求头
    video_id_api = "https://aweme.snssdk.com/aweme/v1/play/"  # 官方视频下载接口
    item_ids_api = "https://www.douyin.com/aweme/v1/web/aweme/detail/"  # 官方信息接口
    clean = Cleaner()  # 过滤错误字符
    length = 128  # 文件名称长度限制
    chunk = 1048576  # 单次下载文件大小，单位字节
    xb = XBogus()

    def __init__(self, log: LoggerManager, save):
        self.headers = self.UA | {
            'referer': 'https://www.douyin.com/',
        }  # 请求头
        self.log = log  # 日志记录模块
        self.data = save  # 详细数据记录模块
        self._cookie = False
        self._nickname = None  # 账号昵称
        self._root = None
        self._name = None
        self.time = None  # 创建时间格式，从DataAcquirer.py传入
        self._split = None
        self._folder = None
        self._music = False  # 是否下载音乐
        self._dynamic = False  # 是否下载动态封面图
        self._original = False  # 是否下载静态封面图
        self.favorite = False  # 喜欢页下载模式
        self.type_ = {"video": "", "images": ""}  # 文件保存目录
        self.video_data = []  # 视频详细信息
        self.image_data = []  # 图集详细信息
        self.mix_data = []  # 合集详细信息
        self.video = 0  # 视频下载数量
        self.image = 0  # 图集下载数量
        self.image_id = None  # 临时记录图集ID，用于下载计数
        self.proxies = None  # 代理，从DataAcquirer.py传入
        self.download = None  # 是否启用下载文件功能

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
                self.log.info(f"命名格式设置成功: {value}", False)
            except KeyError:
                self.log.warning(f"命名格式错误: {value}，将使用默认命名格式(创建时间 作者 描述)")
                self._name = [2, 3, 1]
        else:
            self.log.warning("错误的命名格式，将使用默认命名格式(创建时间 作者 描述)")
            self._name = [2, 3, 1]

    def get_name(self, data: list) -> str:
        """生成文件名称"""
        return self.clean.filter(self.split.join(data[i] for i in self.name))

    @property
    def split(self):
        return self._split

    @split.setter
    def split(self, value):
        if value:
            for s in value:
                if s in self.clean.rule.keys():
                    self.log.warning(f"无效的文件命名分隔符: {value}，默认使用“-”作为分隔符")
                    self._split = "-"
                    return
            self._split = value
            self.log.info(f"命名分隔符设置成功: {value}", False)
        else:
            self.log.warning("错误的文件命名分隔符，默认使用“-”作为分隔符")
            self._split = "-"

    @property
    def folder(self):
        return self._folder

    @folder.setter
    def folder(self, value):
        if value:
            for s in value:
                if s in self.clean.rule.keys():
                    self.log.warning(
                        f"无效的下载文件夹名称: {value}，默认使用“Download”作为下载文件夹名称")
                    self._folder = "Download"
                    return
            self._folder = value
            self.log.info(f"下载文件夹名称设置成功: {value}", False)
        else:
            self.log.warning("错误的下载文件夹名称，默认使用“Download”作为下载文件夹名称")
            self._folder = "Download"

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        if os.path.exists(value) and os.path.isdir(value):
            self._root = value
            self.log.info(f"文件保存路径设置成功: {value}", False)
        else:
            self.log.warning(f"文件保存路径错误: {value}，将使用当前路径作为保存路径")
            self._root = "./"

    @property
    def music(self):
        return self._music

    @music.setter
    def music(self, value):
        if isinstance(value, bool):
            self._music = value
            self.log.info(f"是否下载视频/图集的音乐: {value}", False)
        else:
            self.log.warning(f"音乐下载设置错误: {value}，默认不下载视频/图集的音乐")
            self._music = False

    @property
    def dynamic(self):
        return self._dynamic

    @dynamic.setter
    def dynamic(self, value):
        if isinstance(value, bool):
            self._dynamic = value
            self.log.info(f"是否下载视频动态封面图: {value}", False)
        else:
            self.log.warning(f"动态封面图下载设置错误: {value}，默认不下载视频动态封面图")
            self._dynamic = False

    @property
    def original(self):
        return self._original

    @original.setter
    def original(self, value):
        if isinstance(value, bool):
            self._original = value
            self.log.info(f"是否下载视频封面图: {value}", False)
        else:
            self.log.warning(f"封面图下载设置错误: {value}，默认不下载视频封面图")
            self._original = False

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, value):
        if name := self.clean.filter(value):
            self._nickname = name
            self.log.info(f"账号昵称: {value}, 去除错误字符后: {name}", False)
        else:
            self._nickname = f"账号_{str(time.time())[:10]}"
            self.log.error(f"无效的账号昵称，原始昵称: {value}, 去除错误字符后: {name}")
            self.log.warning(f"本次运行将默认使用当前时间戳作为帐号昵称: {self._nickname}")

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

    def create_folder(self, folder, live=False):
        """创建作品保存文件夹"""
        if self.favorite:
            folder = f"{folder}_favorite"
        root = os.path.join(self.root, folder)
        if not os.path.exists(root):
            os.mkdir(root)
        if live:
            return
        self.type_["video"] = os.path.join(root, "video")
        if not os.path.exists(self.type_["video"]):
            os.mkdir(self.type_["video"])
        self.type_["images"] = os.path.join(root, "images")
        if not os.path.exists(self.type_["images"]):
            os.mkdir(self.type_["images"])

    @retry(max_num=5)
    def get_data(self, item: str) -> dict | bool:
        """获取作品详细数据"""
        params = {
            "aweme_id": item,
            "aid": "6383",
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10"
        }
        xb = self.xb.get_x_bogus(urlencode(params))
        params["X-Bogus"] = xb
        try:
            response = requests.get(
                self.item_ids_api,
                params=params,
                proxies=self.proxies,
                headers=self.headers, timeout=10)
            sleep()
            if response.status_code == 200 and response.text:
                try:
                    return response.json()["aweme_detail"]
                except (KeyError, IndexError):
                    self.log.error(f"作品详细数据内容异常: {response.json()}", False)
                    return False
        except requests.exceptions.ReadTimeout:
            self.log.error(f"请求超时，资源 {item} 获取详细数据失败")
            return False

    def get_info(self, data: list[str | dict]):
        """
        提取作品详细信息
        视频格式: 采集时间, 作品ID, 描述, 创建时间, 作者, 视频ID, [音乐名称, 音乐链接], 动态封面图, 静态封面图, 点赞数量, 评论数量, 收藏数量, 分享数量
        图集格式: 采集时间, 作品ID, 描述, 创建时间, 作者, [图集链接], [音乐名称, 音乐链接], 点赞数量, 评论数量, 收藏数量, 分享数量
        """

        def get_music():
            nonlocal item
            if music_data := item.get("music", False):
                name = f'{music_data["author"]}-{music_data["title"]}'
                url = u[0] if (u := music_data["play_url"]
                ["url_list"]) else None  # 部分作品的数据没有音乐下载地址
                return name, url
            return None, None

        def get_statistics():
            nonlocal item
            result = []
            for i in (
                    "digg_count",
                    "comment_count",
                    "collect_count",
                    "share_count"):
                result.append(str(item["statistics"][i]))
            return result

        for item in data:
            if isinstance(item, str):
                item = self.get_data(item)
            collection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            id_ = item["aweme_id"]
            desc = self.clean.filter(item["desc"]) or id_
            create_time = time.strftime(
                self.time,
                time.localtime(
                    item["create_time"]))
            music_name, music_url = get_music()
            statistics = get_statistics()
            if images := item["images"]:
                images = [i['url_list'][0] for i in images]
                self.log.info(
                    "图集: " +
                    ", ".join(
                        [collection_time,
                         id_,
                         desc,
                         create_time.replace(
                             ".",
                             ":"),
                         self.nickname] +
                        statistics),
                    False)
                self.data.save(["图集",
                                collection_time,
                                id_,
                                desc[:self.length],
                                create_time.replace(".",
                                                    ":"),
                                self.nickname,
                                "#"] + statistics)
                self.image_data.append(
                    [id_, desc, create_time, self.nickname, images, [music_name, music_url]])
            else:
                video_id = item["video"]["play_addr"]["uri"]
                # 动态封面图链接
                dynamic_cover = item["video"]["dynamic_cover"]["url_list"][-1]
                # 静态封面图链接
                origin_cover = item["video"]["cover"]["url_list"][-1]
                self.log.info(
                    "视频: " +
                    ", ".join(
                        [collection_time,
                         id_,
                         desc,
                         create_time.replace(
                             ".",
                             ":"),
                         self.nickname,
                         video_id] + statistics),
                    False)
                self.data.save(["视频",
                                collection_time,
                                id_,
                                desc[:self.length],
                                create_time.replace(".",
                                                    ":"),
                                self.nickname,
                                video_id] + statistics)
                self.video_data.append([id_, desc, create_time, self.nickname, video_id, [
                    music_name, music_url], dynamic_cover, origin_cover])

    def download_images(self):
        root = self.type_["images"]
        for item in self.image_data:
            for index, image in enumerate(item[4]):
                with requests.get(
                        image,
                        stream=True,
                        proxies=self.proxies,
                        headers=self.UA) as response:
                    name = self.get_name(item)
                    self.save_file(
                        response,
                        root,
                        f"{name}_{index + 1}",
                        "jpeg",
                        item[0])
                self.image_id = item[0]
                sleep()
            self.download_music(root, item)

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
                    proxies=self.proxies,
                    headers=self.UA) as response:
                name = self.get_name(item)
                self.save_file(response, root, name, "mp4")
            sleep()
            self.download_music(root, item)
            self.download_cover(root, name, item)

    def download_music(self, root: str, item: list):
        """下载音乐"""
        if self.music and (u := item[5][1]):
            with requests.get(
                    u,
                    stream=True,
                    proxies=self.proxies,
                    headers=self.UA) as response:
                self.save_file(
                    response,
                    root,
                    self.clean.filter(f"{f'{item[0]}-{item[5][0]}'}"),
                    "mp3",
                )
            sleep()

    def download_cover(self, root: str, name: str, item: list):
        """下载静态/动态封面图"""
        if not self.dynamic and not self.original:
            return
        if self.dynamic and (u := item[6]):
            with requests.get(
                    u,
                    stream=True,
                    proxies=self.proxies,
                    headers=self.UA) as response:
                self.save_file(
                    response,
                    root,
                    name,
                    "webp")
            sleep()
        if self.original and (u := item[7]):
            with requests.get(
                    u,
                    stream=True,
                    proxies=self.proxies,
                    headers=self.UA) as response:
                self.save_file(
                    response,
                    root,
                    name,
                    "jpeg")
            sleep()

    @retry(max_num=3)
    def save_file(self, data, root: str, name: str, type_: str, id_=""):
        """保存文件"""

        def delete_file(error_file):
            """清除下载失败的文件"""
            os.remove(error_file)
            self.log.info(f"文件: {error_file} 已删除")

        if not self.download:
            return True
        file = os.path.join(root, f"{name[:self.length].strip()}.{type_}")
        if os.path.exists(file):
            self.log.info(f"{name[:self.length].strip()}.{type_} 已存在，跳过下载")
            self.log.info(
                f"文件保存路径: {file}", False)
            return True
        try:
            with open(file, "wb") as f:
                for chunk in data.iter_content(chunk_size=self.chunk):
                    f.write(chunk)
        except requests.exceptions.ChunkedEncodingError:
            self.log.warning(f"文件: {file} 由于网络异常下载中断")
            delete_file(file)
            return False
        if type_ == "mp4":
            self.video += 1
        elif type_ == "jpeg" and id_ and id_ != self.image_id:
            self.image += 1
        self.log.info(f"{name[:self.length].strip()}.{type_} 下载成功")
        self.log.info(
            f"文件保存路径: {file}",
            False)
        return True

    def summary(self, index: int):
        """汇总下载数量"""
        self.log.info(f"第 {index} 个账号的视频下载数量: {self.video}")
        self.log.info(f"第 {index} 个账号的图集下载数量: {self.image}")
        self.video = 0
        self.image = 0

    @reset
    @check_cookie
    def run(self, index: int, video: list[str], image: list[str]):
        """批量下载"""
        self.create_folder(self.nickname)
        self.log.info(f"开始获取第 {index} 个账号的作品数据")
        self.get_info(video)
        self.get_info(image)
        self.log.info(f"获取第 {index} 个账号的作品数据成功")
        if not self.download:
            return
        self.log.info(f"开始下载第 {index} 个账号的视频/图集")
        self.download_video()
        self.download_images()
        self.log.info(f"第 {index} 个账号的视频/图集下载结束")
        self.summary(index)

    @reset
    @check_cookie
    def run_alone(self, id_: str, download=True):
        """单独下载"""
        if not self.folder:
            self.log.warning("未设置下载文件夹名称")
            return False
        self.create_folder(self.folder)
        data = self.get_data(id_)
        if not data:
            self.log.warning("获取作品详细信息失败")
            return False
        self.nickname = self.clean.filter(data["author"]["nickname"])
        self.get_info([data])
        if data["images"]:
            if not download:
                return self.image_data
            self.download_images()
            return self.image_data[0][4][0]
        else:
            if not download:
                return self.video_data
            self.download_video()
            return self.video_data[0][7]

    def download_live(self, link: str, name: str):
        """下载直播，不需要Cookie信息"""
        self.create_folder("Live", True)
        with requests.get(
                link,
                stream=True,
                proxies=self.proxies, headers=self.UA) as response:
            self.log.info("开始下载直播视频")
            self.save_file(response, f"{self.root}/Live", name, "flv")

    @reset
    @check_cookie
    def run_mix(self, items: list[dict]):
        self.create_folder(self.nickname)
        self.get_info(items)
        self.log.info(f"{self.nickname} 开始下载")
        self.download_video()
        self.download_images()
        self.log.info(f"{self.nickname} 下载结束")
