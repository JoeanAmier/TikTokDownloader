from json import dump
from json import load
from json.decoder import JSONDecodeError
from pathlib import Path
from time import localtime
from time import strftime

from requests import exceptions
from requests import get

from src.Parameter import MsToken
from src.Parameter import TtWid
from src.Recorder import BaseLogger
from src.Recorder import LoggerManager
from src.StringCleaner import Cleaner

__all__ = ["Settings", "Parameter"]


class Settings:
    def __init__(self):
        self.file = Path("./settings.json")  # 配置文件
        self.__default = {
            "accounts": [
                ["账号标识，可以设置为空字符串",
                 "账号主页链接",
                 "账号主页类型",
                 "作品最早发布日期",
                 "作品最晚发布日期"],
            ],
            "mix": [
                ["合集标识，可以设置为空字符串", "合集链接或者作品链接"],
            ],
            "root": "./",
            "folder": "Download",
            "name": "create_time nickname desc",
            "time": "%Y-%m-%d %H.%M.%S",
            "split": "-",
            "music": False,
            "save": "",
            "cookie": None,
            "dynamic": False,
            "original": False,
            "proxies": "",
            "log": False,
            "download": True,
            "max_size": 0,
            "chunk": 512 * 1024,  # 每次从服务器接收的数据块大小
            "retry": 10,  # 重试最大次数
            "pages": 0,
            "thread": False,
        }  # 默认配置

    def create(self):
        """创建默认配置文件"""
        with self.file.open("w", encoding="UTF-8") as f:
            dump(self.__default, f, indent=4)
        print("创建默认配置文件成功！")

    def read(self):
        """读取配置文件，如果没有配置文件，则生成配置文件"""
        try:
            if self.file.exists():
                with self.file.open("r", encoding="UTF-8") as f:
                    return load(f)
            else:
                print("配置文件读取失败，文件不存在！")
                self.create()
                return False  # 生成的默认配置文件必须要设置 cookie 才可以正常运行
        except JSONDecodeError:
            return {}  # 读取配置文件发生错误时返回空配置

    def update(self, settings: dict):
        """更新配置文件"""
        with self.file.open("w", encoding="UTF-8") as f:
            dump(settings, f, indent=4, ensure_ascii=False)
        print("保存配置成功！")


class Parameter:
    name_keys = (
        "id",
        "desc",
        "create_time",
        "nickname",
        "uid",
        "mark",
    )
    clean = Cleaner()

    def __init__(
            self,
            user_agent: str,
            ua_code: tuple,
            log: LoggerManager | BaseLogger,
            xb,
            colour,
            cookie: dict,
            root: str,
            folder: str,
            name: str,
            date_: str,
            split: str,
            music: bool,
            dynamic: bool,
            original: bool,
            proxies: str,
            download: bool,
            max_size: int,
            chunk: int,
            max_retry: int,
            blacklist,
            thread_,
            timeout=10,
    ):
        self.headers = {
            "User-Agent": user_agent,
        }
        self.ua_code = ua_code
        self.log = log
        self.xb = xb
        self.colour = colour
        self.cookie = self.check_cookie(cookie)
        self.root = self.check_root(root)
        self.folder = self.check_folder(folder)
        self.name = self.check_name(name)
        self.date = self.check_date(date_)
        self.split = self.check_split(split)
        self.music = music
        self.dynamic = dynamic
        self.original = original
        self.proxies = self.check_proxies(proxies)
        self.download = download
        self.max_size = self.check_max_size(max_size)
        self.chunk = self.check_chunk(chunk)
        self.max_retry = self.check_max_retry(max_retry)
        self.blacklist = blacklist
        self.id_set = self.blacklist.get_set()
        self.thread = thread_
        self.timeout = self.check_timeout(timeout)

    def check_cookie(self, cookie: dict | str) -> dict:
        if isinstance(cookie, dict):
            return cookie
        elif isinstance(cookie, str):
            self.headers["Cookie"] = cookie
            self.log.warning("Cookie 参数格式应为字典格式")
        else:
            self.log.warning("Cookie 参数格式错误")
        return {}

    @staticmethod
    def add_cookie(cookie: dict) -> None:
        for i in (MsToken.get_ms_token(), TtWid.get_tt_wid(),):
            if isinstance(i, dict):
                cookie |= i

    def check_root(self, root: str) -> Path:
        if (r := Path(root)).is_dir():
            self.log.info(f"root 参数已设置为 {root}", False)
            return r
        self.log.warning(f"root 参数 {root} 不是有效的文件夹路径，程序将使用默认值：./")
        return Path("./")

    def check_folder(self, folder: str) -> str:
        if folder := Cleaner.clean_name(folder):
            self.log.info(f"folder 参数已设置为 {folder}", False)
            return folder
        self.log.warning(f"folder 参数 {folder} 不是有效的文件夹名称，程序将使用默认值：Download")
        return "Download"

    def check_name(self, name: str) -> list[str]:
        name_keys = name.strip().split(" ")
        if all(i in self.name_keys for i in name_keys):
            self.log.info(f"name 参数已设置为 {name}", False)
            return name_keys
        else:
            self.log.warning(f"name 参数 {name} 设置错误，程序将使用默认值：创建时间 账号昵称 作品描述")
            return ["create_time", "nickname", "desc"]

    def check_date(self, date_: str) -> str:
        try:
            _ = strftime(date_, localtime())
            self.log.info(f"time 参数已设置为 {date_}", False)
            return date_
        except ValueError:
            self.log.warning(f"time 参数 {date_} 设置错误，程序将使用默认值：年-月-日 时.分.秒")
            return "%Y-%m-%d %H.%M.%S"

    def check_split(self, split: str) -> str:
        for i in split:
            if i in self.clean.rule.keys():
                self.log.warning(f"split 参数 {split} 包含非法字符，程序将使用默认值：-")
                return "-"
        self.log.info(f"split 参数已设置为 {split}", False)
        return split

    def check_proxies(self, proxies: str) -> dict:
        if isinstance(proxies, str):
            proxies_dict = {
                "http": proxies,
                "https": proxies,
                "ftp": proxies,
            }
            try:
                response = get(
                    "https://www.baidu.com/", proxies=proxies_dict, timeout=10)
                if response.status_code == 200:
                    self.log.info(f"代理 {proxies} 测试成功")
                    return proxies_dict
            except exceptions.ReadTimeout:
                self.log.warning(f"代理 {proxies} 测试超时")
            except (
                    exceptions.ProxyError,
                    exceptions.SSLError,
                    exceptions.ChunkedEncodingError,
                    exceptions.ConnectionError,
            ):
                self.log.warning(f"代理 {proxies} 测试失败")
        return {
            "http": None,
            "https": None,
            "ftp": None,
        }

    def check_max_size(self, max_size: int) -> int:
        max_size = max(max_size, 0)
        self.log.info(f"max_size 参数已设置为 {max_size}", False)
        return max_size

    def check_chunk(self, chunk: int) -> int:
        if isinstance(chunk, int) and chunk > 0:
            self.log.info(f"chunk 参数已设置为 {chunk}", False)
            return chunk
        self.log.warning(f"chunk 参数 {chunk} 设置错误，程序将使用默认值：{512 * 1024}", False)
        return 512 * 1024

    def check_max_retry(self, max_retry: int) -> int:
        if isinstance(max_retry, int) and max_retry >= 0:
            self.log.info(f"max_retry 参数已设置为 {max_retry}", False)
            return max_retry
        self.log.warning(f"max_retry 参数 {max_retry} 设置错误，程序将使用默认值：0", False)
        return 0

    def check_timeout(self, timeout: int | float) -> int | float:
        if isinstance(timeout, (int, float)) and timeout > 0:
            self.log.info(f"timeout 参数已设置为 {timeout}", False)
            return timeout
        self.log.warning(f"timeout 参数 {timeout} 设置错误，程序将使用默认值：10")
        return 10
