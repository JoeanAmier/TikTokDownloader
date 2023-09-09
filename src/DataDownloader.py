import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from itertools import cycle
from pathlib import Path
from shutil import move
from threading import Thread

import requests
from emoji import replace_emoji

from src.Customizer import MAX_WORKERS
from src.Customizer import wait
from src.DataAcquirer import check_cookie
from src.DataAcquirer import retry
from src.DataAcquirer import update_cookie
from src.Recorder import BaseLogger
from src.Recorder import LoggerManager
from src.StringCleaner import Cleaner


def reset(function):
    """重置数据"""

    def inner(self, *args, **kwargs):
        self.video_data = []
        self.image_data = []
        self.api_data = []
        self.video = 0  # 视频下载数量
        self.image = 0  # 图集下载数量
        self.mix_data = []
        self.image_id = None  # 临时记录图集ID，用于下载计数
        return function(self, *args, **kwargs)

    return inner


class Downloader:
    """未来将会弃用"""
    PC_UA = {
        "User-Agent": ""
    }  # 下载请求头
    Phone_UA = {
        'User-Agent': 'com.ss.android.ugc.trill/494+Mozilla/5.0+(Linux;+Android+12;+2112123G+Build/SKQ1.211006.001;+wv)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Version/4.0+Chrome/107.0.5304.105+Mobile+Safari/537.36'
    }  # 移动端请求头
    # video_id_api = "https://aweme.snssdk.com/aweme/v1/play/"  # 官方视频下载接口，已弃用
    item_api = "https://www.douyin.com/aweme/v1/web/aweme/detail/"  # 作品数据接口
    item_tiktok_api = "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/"  # 作品数据接口
    clean = Cleaner()  # 过滤错误字符
    length = 64  # 作品描述长度限制
    temp = Path("./cache/temp")

    def __init__(
            self,
            log: LoggerManager | BaseLogger,
            save,
            xb,
            colour,
            blacklist,
            thread_: bool, ):
        self.colour = colour
        self.headers = {}  # 请求头，通用
        self.log = log  # 日志记录模块，通用
        self.data = save  # 详细数据记录模块，调用前赋值
        self._cookie = {}  # 从DataAcquirer.py传入，通用
        self._nickname = None  # 账号昵称，调用前赋值
        self._root = None  # 根目录，通用
        self._name = None  # 文件命名格式，通用
        self.time = None  # 创建时间格式，从DataAcquirer.py传入，通用
        self._split = None  # 分隔符，通用
        self._folder = None  # 单独下载作品保存文件夹名称，通用
        self._music = False  # 是否下载音乐，通用
        self._dynamic = False  # 是否下载动态封面图，通用
        self._original = False  # 是否下载静态封面图，通用
        self.favorite = False  # 喜欢页下载模式，调用前赋值
        self.type_ = {"video": Path, "images": Path}  # 文件保存目录，运行时赋值
        self.video_data = []  # 视频详细信息
        self.image_data = []  # 图集详细信息
        self.api_data = []
        self.mix_data = []  # 合集详细信息
        self.uid = None  # 账号UID，从DataAcquirer.py传入，提取数据时赋值
        self.mark = None  # 账号标识，从DataAcquirer.py传入，调用前赋值
        self.video = 0  # 视频下载数量
        self.image = 0  # 图集下载数量
        self.image_id = None  # 临时记录图集ID，用于下载计数
        self.proxies = None  # 代理，从DataAcquirer.py传入，通用
        self.download = None  # 是否启用下载文件功能，通用
        self._max_size = 0
        self.retry = 10  # 重试最大次数，通用
        self.tiktok = False  # TikTok 平台
        self.xb = xb
        self.__pool = ThreadPoolExecutor if thread_ else FakeThreadPool
        self.__thread = None
        self._chunk = None  # 每次从服务器接收的数据块大小
        self.__code = None
        self._blacklist = blacklist
        self._id_set = self._blacklist.get_set()

    def initialization(self, user_agent: str, code: tuple):
        self.PC_UA["User-Agent"], self.__code = user_agent, code

    @property
    def max_size(self):
        return self._max_size

    @max_size.setter
    def max_size(self, value: int):
        if isinstance(value, int):
            self._max_size = max(value, 0)

    @property
    def chunk(self):
        return self._chunk

    @chunk.setter
    def chunk(self, chunk: int):
        self._chunk = chunk if isinstance(
            chunk, int) and chunk > 0 else 512 * 1024
        self.log.info(f"每次从服务器接收的数据块大小已设置为 {self._chunk}", False)

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
                "nickname": 4,
                "uid": 3,
                "mark": 5,
            }
            name = value.strip().split(" ")
            try:
                self._name = [dict_[i] for i in name]
                self.log.info(f"命名格式设置成功: {value}", False)
            except KeyError:
                self.log.warning(f"命名格式错误: {value}，将使用默认命名格式(创建时间 账号昵称 描述)")
                self._name = [2, 4, 1]
        else:
            self.log.warning("错误的命名格式，将使用默认命名格式(创建时间 账号昵称 描述)")
            self._name = [2, 4, 1]

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
        if (r := Path(value)).is_dir():
            self._root = r
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
            self.log.error(f"无效的账号昵称，原始昵称: {value}")
            self.log.warning(f"本次运行将默认使用当前时间戳作为账号昵称: {self._nickname}")

    @property
    def cookie(self):
        return self._cookie

    @cookie.setter
    def cookie(self, cookie: dict):
        if isinstance(cookie, dict):
            self.headers |= self.PC_UA
            self._cookie = cookie
            self.headers["Cookie"] = (
                "; ".join([f"{i}={j}" for i, j in self._cookie.items()]))

    # def deal_url_params(self, params: dict, platform="PC"):
    #     xb = self.xb.get_x_bogus(params, self.PC_UA["User-Agent"], platform)
    #     params["X-Bogus"] = xb

    def deal_url_params(self, params: dict, version=23):
        xb = self.xb.get_x_bogus(params, self.__code, version)
        params["X-Bogus"] = xb

    def create_folder(self, folder: str, live=False, collection=False):
        """创建作品保存文件夹"""
        if self.favorite and not collection:
            folder = f"{folder}_喜欢作品"
        root = self.root.joinpath(folder)
        if not root.is_dir():
            root.mkdir()
        if live:
            return
        self.type_["video"] = root.joinpath("video")
        if not self.type_["video"].is_dir():
            self.type_["video"].mkdir()
        self.type_["images"] = root.joinpath("images")
        if not self.type_["images"].is_dir():
            self.type_["images"].mkdir()

    @retry(finish=False)
    def get_data(self, item: str) -> dict | bool:
        """获取作品详细数据"""
        if self.tiktok:
            params = {
                "aweme_id": item,
            }
            api = self.item_tiktok_api
            headers = self.Phone_UA
        else:
            params = {
                "aweme_id": item,
                "aid": "6383",
                "cookie_enabled": "true",
                "platform": "PC",
                "downlink": "10"
            }
            api = self.item_api
            self.deal_url_params(params)
            headers = self.headers
        try:
            response = requests.get(
                api,
                params=params,
                proxies=self.proxies,
                headers=headers, timeout=10)
            wait()
            if response.content == b"":
                self.log.warning("作品详细数据响应内容为空")
                return False
            try:
                return response.json()["aweme_list"][0] if self.tiktok else response.json()[
                    "aweme_detail"]
            except KeyError:
                self.log.error(f"作品详细数据内容异常: {response.json()}", False)
                return False
        except (
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ChunkedEncodingError,
                requests.exceptions.SSLError,
        ):
            self.log.error(f"请求超时，资源 {item} 获取详细数据失败")
            return False

    def get_author_data(self, data):
        data = data["author"]
        uid = self.uid or data["uid"]
        sec_uid = data["sec_uid"]
        short_id = data.get("short_id") or ""
        unique_id = data.get("unique_id") or ""
        signature = data.get("signature") or ""
        nickname = data.get("nickname") or "已注销账号"
        return uid, sec_uid, nickname, unique_id, short_id, signature

    @staticmethod
    def clear_spaces(string: str):
        """将连续的空格转换为单个空格"""
        return " ".join(string.split())

    @staticmethod
    def get_music(item, id_):
        if music_data := item.get("music", False):
            name = music_data.get("title") or id_
            url = m[-1] if (m := music_data["play_url"]
            ["url_list"]) else ""  # 部分作品的数据没有音乐下载地址
            return name, url
        return "", ""

    @staticmethod
    def get_statistics(item):
        return [
            str(item["statistics"][i])
            for i in (
                "digg_count",
                "comment_count",
                "collect_count",
                "share_count",
            )
        ]

    @staticmethod
    def get_cover(item):
        # 动态封面图链接
        dynamic_cover = u["url_list"][-1] if (
                                                 u := item["video"].get("dynamic_cover")) and u["url_list"] else ""
        # 静态封面图链接
        origin_cover = u["url_list"][-1] if (
                                                u := item["video"].get("origin_cover")) and u["url_list"] else ""
        return dynamic_cover, origin_cover

    @staticmethod
    def get_tags(item):
        if not (t := item.get("video_tag")):
            return ["", "", ""]
        tags = [i["tag_name"] for i in t]
        return tags or ["", "", ""]

    @staticmethod
    def get_description(item) -> str:
        try:
            desc = item["share_info"]["share_link_desc"]
            return desc.split(
                ":/ ", 1)[1].rstrip("  %s 复制此链接，打开Dou音搜索，直接观看视频！")
        except (KeyError, IndexError):
            return ""

    def get_info(self, data: list[str | dict], api=False):
        """
        提取作品详细信息
        视频格式: 作品ID, 作品描述, 发布时间, UID, 作者昵称, 账号标识, 下载链接, [音乐名称, 音乐链接], 静态封面图, 动态封面图
        图集格式: 作品ID, 作品描述, 发布时间, UID, 作者昵称, 账号标识, 下载链接, [音乐名称, 音乐链接]
        """
        for item in data:
            if isinstance(item, str):
                item = self.get_data(item)
            collection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            id_ = item["aweme_id"]
            uid, sec_uid, nickname, unique_id, short_id, signature = self.get_author_data(
                item)
            desc = self.clear_spaces(
                self.clean.filter(
                    self.get_description(item))[
                :self.length]) or id_
            create_time = time.strftime(
                self.time,
                time.localtime(
                    item["create_time"]))
            music_name, music_url = self.get_music(item, id_)
            statistics = self.get_statistics(item)
            tags = self.get_tags(item)
            if images := item.get("images"):
                type_ = "图集"
                images = [i['url_list'][-1] for i in images]
                download_link = " ".join(images)
                dynamic_cover = ""
                origin_cover = ""
                self.image_data.append([id_,
                                        desc,
                                        create_time,
                                        uid,
                                        self.clean.filter(nickname) if self.favorite else self.nickname,
                                        self.mark,
                                        images,
                                        [music_name,
                                         music_url]])
            elif images := item.get("image_post_info"):
                type_ = "图集"
                images = [i["display_image"]["url_list"][-1]
                          for i in images["images"]]
                download_link = " ".join(images)
                dynamic_cover = ""
                origin_cover = ""
                self.image_data.append([id_,
                                        desc,
                                        create_time,
                                        uid,
                                        self.clean.filter(nickname) if self.favorite else self.nickname,
                                        self.mark,
                                        images,
                                        [music_name,
                                         music_url]])
            else:
                type_ = "视频"
                download_link = item["video"]["play_addr"]["url_list"][-1]
                dynamic_cover, origin_cover = self.get_cover(item)
                self.video_data.append([id_,
                                        desc,
                                        create_time,
                                        uid,
                                        self.clean.filter(nickname) if self.favorite else self.nickname,
                                        self.mark,
                                        download_link,
                                        [music_name,
                                         music_url],
                                        origin_cover,
                                        dynamic_cover])
            self.log.info(
                f"{type_}: " +
                ", ".join(
                    [
                        id_,
                        desc,
                        create_time.replace(
                            ".",
                            ":"),
                        uid,
                        self.clean.filter(nickname) if self.favorite else self.nickname,
                        music_name]),
                False)
            works_data = [
                             type_,
                             collection_time,
                             uid,
                             sec_uid,
                             unique_id,
                             short_id,
                             id_,
                             desc,
                             create_time.replace(
                                 ".",
                                 ":"),
                             self.clean.filter(nickname) if self.favorite else self.nickname,
                             signature,
                             download_link,
                             music_name,
                             music_url,
                             origin_cover,
                             dynamic_cover,
                             *tags,
                         ] + statistics
            self.data.save(works_data)
            if api:
                self.api_data.append(works_data)

    def check_blacklist(self, id_) -> bool:
        if not id_:
            return True
        if id_ in self._id_set:
            self.log.info(f"作品 {id_} 存在下载记录，跳过下载")
            return False
        return True

    def update_blacklist(self, id_):
        if self._blacklist.switch:
            self._id_set.add(id_)
            self._blacklist.update_id(id_)

    @retry(finish=False)
    def request_file(
            self,
            url: str,
            root,
            name: str,
            type_: str,
            image_id="",
            file_id=None,
            unknown_size=False):
        """发送请求获取文件内容"""
        if not self.download:
            return True
        file = f"{name.strip()}.{type_}"
        full_path = root.joinpath(file)
        if full_path.exists():
            self.log.info(f"{file} 已存在，跳过下载")
            self.log.info(
                f"文件保存路径: {full_path}", False)
            return True
        try:
            with requests.get(
                    url,
                    stream=True,
                    proxies=self.proxies,
                    headers=self.Phone_UA if self.tiktok else self.headers) as response:
                if not (
                        content := int(
                            response.headers.get(
                                'content-length',
                                0))) and not unknown_size:
                    self.log.warning(f"{url} 返回内容为空")
                    return False
                if response.status_code != 200:
                    self.log.warning(
                        f"{response.url} 响应码异常: {response.status_code}")
                    return False
                elif all((self.max_size, content, content > self.max_size)):
                    self.log.info(f"{file} 文件大小超出限制，跳过下载")
                    return True
                return bool(
                    self.save_file(
                        response,
                        file,
                        content,
                        full_path,
                        type_,
                        file_id or f"直播 {file} ",
                        image_id, ))
        except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as e:
            self.log.warning(f"网络异常: {e}")
            return False

    def download_images(self):
        root = self.type_["images"]
        for item in self.image_data:
            if not self.check_blacklist(item[0]):
                continue
            for index, image in enumerate(item[6]):
                name = replace_emoji(self.get_name(item))
                self.__thread.submit(
                    self.request_file,
                    image,
                    root,
                    f"{name}_{index + 1}",
                    type_="jpeg",
                    image_id=item[0],
                    file_id=f"图集 {item[0]}_{index + 1} ")
                self.image_id = item[0]
            self.update_blacklist(item[0])
            self.download_music(root, item)

    def download_video(self):
        root = self.type_["video"]
        for item in self.video_data:
            if not self.check_blacklist(item[0]):
                continue
            name = replace_emoji(self.get_name(item))
            self.__thread.submit(
                self.request_file,
                item[6],
                root,
                name,
                type_="mp4",
                file_id=f"视频 {item[0]} "
            )
            self.update_blacklist(item[0])
            self.download_music(root, item)
            self.download_cover(root, name, item)

    def download_music(self, root, item: list):
        """下载音乐"""
        if self.music and (u := item[7][1]):
            self.__thread.submit(self.request_file, u, root, self.clean.filter(
                f"{f'{item[0]}-{item[7][0]}'}"), type_="mp3", file_id=f"原声 {item[0]} ")

    def download_cover(self, root, name: str, item: list):
        """下载静态/动态封面图"""
        if not self.dynamic and not self.original:
            return
        if self.dynamic and (u := item[9]):
            self.__thread.submit(
                self.request_file,
                u,
                root,
                name,
                type_="webp",
                file_id=f"动图 {item[0]} ")
        if self.original and (u := item[8]):
            self.__thread.submit(
                self.request_file,
                u,
                root,
                name,
                type_="jpeg",
                file_id=f"封面 {item[0]} ")

    def save_file(
            self,
            data,
            file,
            size: int,
            full_path,
            type_: str,
            file_id: str,
            id_=""):
        """保存文件"""

        def delete_file(name, error_file):
            """清除下载失败的文件"""
            error_file.unlink()
            self.log.info(f"文件: {name} 已删除")

        def stop_bar():
            if self.__pool != FakeThreadPool:
                return
            if not size:
                progress_bar.update(0, True)
            print()

        temp_path = self.temp.joinpath(file)
        try:
            # self.log.info(f"{file} 开始下载")
            progress_bar = ProgressBar(
                size, text=file_id,
                colorize=self.colour.colorize,
                solo=self.__pool == FakeThreadPool) if size > 0 else LoopingBar(
                text=file_id,
                colorize=self.colour.colorize,
                solo=self.__pool == FakeThreadPool)
            with temp_path.open("wb") as f:
                for chunk in data.iter_content(chunk_size=self.chunk):
                    f.write(chunk)
                    progress_bar.update(len(chunk))
                stop_bar()
        except requests.exceptions.ChunkedEncodingError:
            self.log.warning(f"文件: {file} 由于网络异常下载中断")
            delete_file(file, temp_path)
            stop_bar()
            return False
        if type_ == "mp4":
            self.video += 1
        elif type_ == "jpeg" and id_ and id_ != self.image_id:
            self.image += 1
        self.remove_file(temp_path, full_path)
        # self.log.info(f"{file} 下载成功")
        return True

    def remove_file(self, temp, path):
        move(temp.resolve(), path)
        self.log.info(
            f"文件保存路径: {path}",
            False)

    def summary(self, tip: str):
        """汇总下载数量"""
        self.log.info(f"{tip}账号的视频下载数量: {self.video}")
        self.log.info(f"{tip}账号的图集下载数量: {self.image}")
        self.video = 0
        self.image = 0

    @reset
    @check_cookie
    def run(
            self,
            tip: str,
            video: list[str],
            image: list[str],
            api=False,
            collection=""):
        """批量下载"""
        self.create_folder(f"{self.uid}_{self.mark}", collection=True)
        self.log.info(f"开始获取{tip}账号的{collection}作品数据")
        self.get_info(video, api)
        self.get_info(image, api)
        self.log.info(f"获取{tip}账号的{collection}作品数据成功")
        if not self.download:
            return
        with self.__pool(max_workers=MAX_WORKERS) as self.__thread:
            self.log.info(f"开始下载{tip}账号的{collection}视频/图集")
            self.download_video()
            self.download_images()
            self.log.info(f"{tip}账号的{collection}视频/图集下载结束")
        self.summary(tip)

    @reset
    @check_cookie
    def run_alone(self, id_: str, download=True, api=False):
        """单独下载"""
        if download and not self.folder:
            self.log.warning("未设置下载文件夹名称")
            return False
        elif download:
            self.create_folder(self.folder)
        data = self.get_data(id_)
        if not data:
            self.log.warning("获取作品详细信息失败")
            return False
        self.nickname = self.clean.filter(data["author"]["nickname"])
        self.mark = self.nickname
        self.get_info([data], api)
        if api:
            return self.api_data
        with self.__pool(max_workers=MAX_WORKERS) as self.__thread:
            if data.get("images") or data.get("image_post_info"):
                if not download:
                    return self.image_data
                self.download_images()
                return self.image_data[0][6][0]
            else:
                if not download:
                    return self.video_data
                self.download_video()
                return self.video_data[0][8]

    def download_live(self, link: str, name: str):
        """下载直播，不需要Cookie信息"""
        self.create_folder("Live", True)
        _ = self.headers.pop("Cookie", None)
        self.request_file(link, self.root.joinpath(
            "Live"), name, "flv", unknown_size=True)

    @reset
    @check_cookie
    def run_mix(self, folder: str, items: list[dict], api=False):
        """下载合集作品"""
        self.create_folder(folder)
        self.get_info(items, api)
        if not self.download:
            return
        with self.__pool(max_workers=MAX_WORKERS) as self.__thread:
            self.log.info(f"{self.nickname} 的合集开始下载")
            self.download_video()
            self.download_images()
            self.log.info(f"{self.nickname} 的合集下载结束")


class NewDownloader:
    Phone_headers = None
    temp = Path("./cache/temp")

    def __init__(self, params):
        self.cookie = params.cookie
        self.PC_headers, self.black_headers = self.init_headers(params.headers)
        self.ua_code = params.ua_code
        self.log = params.log
        self.xb = params.xb
        self.colour = params.colour
        self.root = params.root
        self.folder = params.folder
        self.name = params.name
        self.split = params.split
        self.music = params.music
        self.dynamic = params.dynamic
        self.original = params.original
        self.proxies = params.proxies
        self.download = params.download
        self.max_size = params.max_size
        self.chunk = params.chunk
        self.max_retry = params.max_retry
        self.blacklist = params.blacklist
        self.id_set = params.id_set
        self.__thread = ThreadPoolExecutor if params.thread else FakeThreadPool
        self.__pool = None

    @staticmethod
    def init_headers(headers: dict) -> tuple:
        return headers.copy(), {"User-Agent": headers["User-Agent"]}

    @update_cookie
    def run(self, data: list[dict]) -> None:
        pass

    def download_image(self) -> None:
        pass

    def download_video(self) -> None:
        pass

    def download_music(self) -> None:
        pass

    def download_cover(self) -> None:
        pass

    def download_live(self) -> None:
        pass

    def request_file(self) -> bool:
        pass

    def download_file(self, urls: list) -> bool:
        pass

    def create_folder(self, name: str):
        pass

    def delete_file(self, path: Path):
        path.unlink()
        self.log.info(f"文件 {path} 已删除")


class FakeThreadPool:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def submit(function, *args, **kwargs):
        function(*args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class NoneBar:
    def __init__(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    @staticmethod
    def bytes_to_mb(bytes_value):
        return bytes_value / (1024 * 1024)

    @staticmethod
    def direct(text, *args, **kwargs):
        return text


class ProgressBar(NoneBar):
    def __init__(
            self,
            total,
            text="文件",
            colorize=None,
            length=10,
            fill='█',
            solo=True,
            *args,
            **kwargs):
        super().__init__(*args, **kwargs)
        self.params = {"end": "", "flush": True} if solo else {}
        self.colorize = colorize or self.direct
        self.text = text
        self.total = total
        self.length = length
        self.fill = fill
        self.downloaded_size = 0
        self.start_time = time.time()
        self.update(0)

    def update(self, chunk_size):
        self.downloaded_size = min(
            self.downloaded_size + chunk_size, self.total)
        percent = 100 * (self.downloaded_size / float(self.total))
        filled_length = int(self.length * self.downloaded_size // self.total)
        bar = self.fill * filled_length + '-' * (self.length - filled_length)
        elapsed_time = time.time() - self.start_time
        print(
            self.colorize(
                f'\r{self.text}下载进度: |{bar}| {percent:.1f}%  耗时: {elapsed_time:.1f}s  文件: {self.bytes_to_mb(self.downloaded_size):.1f}MB/{self.bytes_to_mb(self.total):.1f}MB',
                95),
            **self.params)


class LoopingBar(NoneBar):
    def __init__(self,
                 text="文件",
                 colorize=None,
                 animation=(
                         '⣾',
                         '⣷',
                         '⣯',
                         '⣟',
                         '⡿',
                         '⢿',
                         '⣻',
                         '⣽'),
                 solo=True,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.params = {"end": "", "flush": True} if solo else {}
        self.colorize = colorize or self.direct
        self.text = text
        self.spin_chars = cycle(animation)
        self.download_size = 0
        self.start_time = time.time()
        self.update(0)

    def update(self, size: int, finished=False):
        elapsed_time = time.time() - self.start_time
        spin_char = next(self.spin_chars)
        self.download_size += size
        print(
            self.colorize(
                f"\r{self.text}{'下载完成' if finished else '正在下载'}: {'✔️' if finished else spin_char}  耗时: {elapsed_time:.1f}s  文件: {self.bytes_to_mb(self.download_size):.1f}MB",
                95),
            **self.params)


class LoadingAnimation:
    def __init__(
            self,
            text="文件正在下载",
            colorize=None,
            animation=(
                    '⣾',
                    '⣷',
                    '⣯',
                    '⣟',
                    '⡿',
                    '⢿',
                    '⣻',
                    '⣽'),
            frequency=0.25):
        self.colorize = colorize or NoneBar.direct
        self.text = text
        self.animation_chars = cycle(animation)
        self.frequency = frequency
        self.running = True

    def run(self):
        while self.running:
            print(
                self.colorize(
                    f"\r{self.text}: {next(self.animation_chars)}",
                    95),
                end="",
                flush=True)
            time.sleep(self.frequency)
        print("\r", end="", flush=True)

    def stop(self):
        self.running = False
        print()


if __name__ == "__main__":
    demo = LoadingAnimation()
    thread = Thread(target=demo.run)
    thread.start()
    wait()
    demo.stop()
    print("运行结束！")
    a = FakeThreadPool
    print(a == FakeThreadPool)
