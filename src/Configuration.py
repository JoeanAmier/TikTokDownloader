from json import dump
from json import load
from json.decoder import JSONDecodeError
from pathlib import Path
from time import localtime
from time import strftime
from types import SimpleNamespace

from requests import exceptions
from requests import get

from src.Customizer import WARNING, INFO, ERROR, GENERAL
from src.Parameter import MsToken
from src.Parameter import TtWid
from src.Recorder import BaseLogger
from src.Recorder import LoggerManager
from src.StringCleaner import Cleaner

__all__ = ["Settings", "Parameter"]


class Settings:
    def __init__(self, root: Path, console):
        self.file = root.joinpath("./settings.json")  # 配置文件
        self.console = console
        self.__default = {
            "Accounts_Urls": [
                {"Mark": "账号标识，可以设置为空字符串",
                 "Url": "账号主页链接",
                 "Tab": "账号主页类型",
                 "Earliest": "作品最早发布日期",
                 "Latest": "作品最晚发布日期"},
            ],
            "Mix_Urls": [
                {"Mark": "合集标识，可以设置为空字符串",
                 "Url": "合集链接或者作品链接"},
            ],
            "Root": "",
            "Folder_Name": "Download",
            "Name_Format": "create_time nickname desc",
            "Date_Format": "%Y-%m-%d %H.%M.%S",
            "Split": "-",
            "Folder_Mode": False,
            "Music": False,
            "Storage_Format": "",
            "Cookie": None,
            "Dynamic_Cover": False,
            "Original_Cover": False,
            "Proxies": "",
            "Log": False,
            "Download": True,
            "Max_Size": 0,
            "Chunk": 512 * 1024,  # 每次从服务器接收的数据块大小
            "Max_Retry": 10,  # 重试最大次数
            "Max_Pages": 0,
            "Thread": False,
        }  # 默认配置

    def create(self):
        """创建默认配置文件"""
        with self.file.open("w", encoding="UTF-8") as f:
            dump(self.__default, f, indent=4, ensure_ascii=False)
        self.console.print(
            "创建默认配置文件 settings.json 成功！\n请参考项目文档的快速入门部分，设置 Cookie 后重新运行程序！",
            style=GENERAL)

    def read(self):
        """读取配置文件，如果没有配置文件，则生成配置文件"""
        try:
            if self.file.exists():
                with self.file.open("r", encoding="UTF-8") as f:
                    return self.check(
                        load(f).keys(), load(
                            f, object_hook=lambda d: SimpleNamespace(
                                **d)))
            else:
                self.console.print(
                    "配置文件 settings.json 读取失败，文件不存在！",
                    style=WARNING)
                self.create()
                return False  # 生成的默认配置文件必须要设置 cookie 才可以正常运行
        except JSONDecodeError:
            self.console.print(
                "配置文件 settings.json 格式错误，请检查 JSON 格式！",
                style=ERROR)
            return False  # 读取配置文件发生错误时返回空配置

    def check(self, keys, result: SimpleNamespace):
        if set(self.__default.keys()).issubset(set(keys)):
            return result
        if self.console.input(
                f"[{ERROR}]配置文件 settings.json 缺少必要的参数，是否需要生成默认配置文件(YES/NO): [/{ERROR}]").upper() == "YES":
            self.create()
        return None

    def update(self, settings: dict):
        """更新配置文件"""
        with self.file.open("w", encoding="UTF-8") as f:
            dump(settings, f, indent=4, ensure_ascii=False)
        self.console.print("保存配置成功！", style=INFO)


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
            main_path: Path,
            user_agent: str,
            ua_code: tuple,
            log: LoggerManager | BaseLogger,
            xb,
            cookie: dict | str,
            root: str,
            folder_name: str,
            name_format: str,
            date_format: str,
            split: str,
            music: bool,
            folder_mode: bool,
            dynamic: bool,
            original: bool,
            proxies: str,
            download: bool,
            max_size: int,
            chunk: int,
            max_retry: int,
            max_pages: int,
            blacklist,
            thread_: bool,
            timeout=10,
    ):
        self.main_path = main_path  # 项目根路径
        self.headers = {
            "User-Agent": user_agent,
        }
        self.ua_code = ua_code
        self.log = log
        self.xb = xb
        self.cookie = self.check_cookie(cookie)
        self.root = self.check_root(root)
        self.folder_name = self.check_folder_name(folder_name)
        self.name_format = self.check_name_format(name_format)
        self.date_format = self.check_date_format(date_format)
        self.split = self.check_split(split)
        self.music = music
        self.folder_mode = folder_mode
        self.dynamic = dynamic
        self.original = original
        self.proxies = self.check_proxies(proxies)
        self.download = download
        self.max_size = self.check_max_size(max_size)
        self.chunk = self.check_chunk(chunk)
        self.max_retry = self.check_max_retry(max_retry)
        self.max_pages = self.check_max_pages(max_pages)
        self.blacklist = blacklist
        self.thread = thread_
        self.timeout = self.check_timeout(timeout)

    def check_cookie(self, cookie: dict | str) -> dict:
        if isinstance(cookie, dict):
            return cookie
        elif isinstance(cookie, str):
            self.headers["Cookie"] = cookie
            # self.log.warning("Cookie 参数格式应为字典格式")
        else:
            self.log.warning("Cookie 参数格式错误")
        return {}

    @staticmethod
    def add_cookie(cookie: dict) -> None:
        for i in (MsToken.get_ms_token(), TtWid.get_tt_wid(),):
            if isinstance(i, dict):
                cookie |= i

    def check_root(self, root: str) -> Path:
        if root and (r := Path(root)).is_dir():
            self.log.info(f"Root 参数已设置为 {root}", False)
            return r
        self.log.warning(f"Root 参数 {root} 不是有效的文件夹路径，程序将使用项目根路径作为储存路径")
        return self.main_path

    def check_folder_name(self, folder_name: str) -> str:
        if folder_name := Cleaner.clean_name(folder_name):
            self.log.info(f"Folder_Name 参数已设置为 {folder_name}", False)
            return folder_name
        self.log.warning(
            f"Folder_Name 参数 {folder_name} 不是有效的文件夹名称，程序将使用默认值：Download")
        return "Download"

    def check_name_format(self, name_format: str) -> list[str]:
        name_keys = name_format.strip().split(" ")
        if all(i in self.name_keys for i in name_keys):
            self.log.info(f"Name_Format 参数已设置为 {name_format}", False)
            return name_keys
        else:
            self.log.warning(
                f"Name_Format 参数 {name_format} 设置错误，程序将使用默认值：创建时间 账号昵称 作品描述")
            return ["create_time", "nickname", "desc"]

    def check_date_format(self, date_format: str) -> str:
        try:
            _ = strftime(date_format, localtime())
            self.log.info(f"Date_Format 参数已设置为 {date_format}", False)
            return date_format
        except ValueError:
            self.log.warning(
                f"Date_Format 参数 {date_format} 设置错误，程序将使用默认值：年-月-日 时.分.秒")
            return "%Y-%m-%d %H.%M.%S"

    def check_split(self, split: str) -> str:
        for i in split:
            if i in self.clean.rule.keys():
                self.log.warning(f"Split 参数 {split} 包含非法字符，程序将使用默认值：-")
                return "-"
        self.log.info(f"Split 参数已设置为 {split}", False)
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
        self.log.info(f"Max_Size 参数已设置为 {max_size}", False)
        return max_size

    def check_chunk(self, chunk: int) -> int:
        if isinstance(chunk, int) and chunk > 0:
            self.log.info(f"Chunk 参数已设置为 {chunk}", False)
            return chunk
        self.log.warning(f"Chunk 参数 {chunk} 设置错误，程序将使用默认值：{512 * 1024}", False)
        return 512 * 1024

    def check_max_retry(self, max_retry: int) -> int:
        if isinstance(max_retry, int) and max_retry >= 0:
            self.log.info(f"Max_Retry 参数已设置为 {max_retry}", False)
            return max_retry
        self.log.warning(f"Max_Retry 参数 {max_retry} 设置错误，程序将使用默认值：0", False)
        return 0

    def check_max_pages(self, max_pages: int) -> int:
        if isinstance(max_pages, int) and max_pages > 0:
            self.log.info(f"Max_Pages 参数已设置为 {max_pages}", False)
            return max_pages
        elif max_pages != 0:
            self.log.warning(
                f"Max_Pages 参数 {max_pages} 设置错误，程序将使用默认值：99999", False)
        return 99999

    def check_timeout(self, timeout: int | float) -> int | float:
        if isinstance(timeout, (int, float)) and timeout > 0:
            self.log.info(f"Timeout 参数已设置为 {timeout}", False)
            return timeout
        self.log.warning(f"Timeout 参数 {timeout} 设置错误，程序将使用默认值：10")
        return 10
