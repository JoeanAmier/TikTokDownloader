from pathlib import Path
from time import localtime
from time import strftime
from types import SimpleNamespace
from typing import TYPE_CHECKING

from requests import exceptions
from requests import get

from src.encrypt import MsToken
from src.encrypt import TtWid
from src.extract import Extractor
from src.module import Cleaner
from src.module import ColorfulConsole
from src.module import Cookie
from src.module import FFMPEG
from src.module import Register
from src.storage import RecordManager
from .settings import Settings

if TYPE_CHECKING:
    from src.manager import DownloadRecorder

__all__ = ["Parameter"]


class Parameter:
    name_keys = (
        "id",
        "desc",
        "create_time",
        "nickname",
        "uid",
        "mark",
        "type",
    )
    cleaner = Cleaner()

    def __init__(
            self,
            settings: Settings,
            cookie_object: Cookie,
            main_path: Path,
            user_agent: str,
            ua_code: tuple,
            logger,
            xb,
            console: ColorfulConsole,
            cookie: dict | str,
            root: str,
            accounts_urls: dict,
            mix_urls: dict,
            folder_name: str,
            name_format: str,
            date_format: str,
            split: str,
            music: bool,
            folder_mode: bool,
            storage_format: str,
            dynamic_cover: bool,
            original_cover: bool,
            proxies: str,
            download: bool,
            max_size: int,
            chunk: int,
            max_retry: int,
            max_pages: int,
            default_mode: int,
            owner_url: dict,
            ffmpeg: str,
            blacklist: "DownloadRecorder",
            timeout=10,
            **kwargs,
    ):
        self.settings = settings
        self.cookie_object = cookie_object
        self.main_path = main_path  # 项目根路径
        self.temp = main_path.joinpath("./cache/temp")  # 缓存路径
        self.headers = {
            "User-Agent": user_agent,
        }
        self.ua_code = ua_code
        self.logger = logger(main_path, console)
        self.logger.run()
        self.xb = xb
        self.console = console
        self.cookie_cache = None
        self.cookie = self.check_cookie(cookie)
        self.root = self.check_root(root)
        self.folder_name = self.check_folder_name(folder_name)
        self.name_format = self.check_name_format(name_format)
        self.date_format = self.check_date_format(date_format)
        self.split = self.check_split(split)
        self.music = self._check_bool(music)
        self.folder_mode = self._check_bool(folder_mode)
        self.storage_format = self.check_storage_format(storage_format)
        self.dynamic_cover = self._check_bool(dynamic_cover)
        self.original_cover = self._check_bool(original_cover)
        self.proxies = self.check_proxies(proxies)
        self.download = self._check_bool(download)
        self.max_size = self.check_max_size(max_size)
        self.chunk = self.check_chunk(chunk)
        self.max_retry = self.check_max_retry(max_retry)
        self.max_pages = self.check_max_pages(max_pages)
        self.blacklist = blacklist
        self.timeout = self.check_timeout(timeout)
        self.accounts_urls: SimpleNamespace = Extractor.generate_data_object(
            accounts_urls)
        self.mix_urls: SimpleNamespace = Extractor.generate_data_object(
            mix_urls)
        self.owner_url: SimpleNamespace = Extractor.generate_data_object(
            owner_url)
        self.default_mode = self.check_default_mode(default_mode)
        self.preview = "static/images/blank.png"
        self.ffmpeg = self._generate_ffmpeg_object(ffmpeg)
        self.check_rules = {
            "accounts_urls": None,
            "mix_urls": None,
            "owner_url": None,
            "root": self.check_root,
            "folder_name": self.check_folder_name,
            "name_format": self.check_name_format,
            "date_format": self.check_date_format,
            "split": self.check_split,
            "folder_mode": self._check_bool,
            "music": self._check_bool,
            "storage_format": self.check_storage_format,
            "dynamic_cover": self._check_bool,
            "original_cover": self._check_bool,
            "proxies": self.check_proxies,
            "download": self._check_bool,
            "max_size": self.check_max_size,
            "chunk": self.check_chunk,
            "max_retry": self.check_max_retry,
            "max_pages": self.check_max_pages,
            "default_mode": self.check_default_mode,
            "ffmpeg": self._generate_ffmpeg_object,
        }

    @staticmethod
    def _check_bool(value: bool, default=False) -> bool:
        return value if isinstance(value, bool) else default

    def check_cookie(self, cookie: dict | str) -> dict:
        if isinstance(cookie, dict):
            return cookie
        elif isinstance(cookie, str):
            self.cookie_cache = cookie
        else:
            self.logger.warning("Cookie 参数格式错误")
        return {}

    @staticmethod
    def add_cookie(cookie: dict | str) -> None | str:
        parameters = (MsToken.get_real_ms_token(), TtWid.get_tt_wid(),)
        if isinstance(cookie, dict):
            for i in parameters:
                if isinstance(i, dict):
                    cookie |= i
        elif isinstance(cookie, str):
            for i in parameters:
                if isinstance(i, dict):
                    cookie += Register.generate_cookie(i)
            return cookie

    def check_root(self, root: str) -> Path:
        if not root:
            return self.main_path
        if (r := Path(root)).is_dir():
            self.logger.info(f"root 参数已设置为 {root}", False)
            return r
        if r := self.check_root_again(r):
            self.logger.info(f"root 参数已设置为 {r}", False)
            return r
        self.logger.warning(f"root 参数 {root} 不是有效的文件夹路径，程序将使用项目根路径作为储存路径")
        return self.main_path

    @staticmethod
    def check_root_again(root: Path) -> bool | Path:
        if root.resolve().parent.is_dir():
            root.mkdir()
            return root
        return False

    def check_folder_name(self, folder_name: str) -> str:
        if folder_name := self.cleaner.filter_name(folder_name, False):
            self.logger.info(f"folder_name 参数已设置为 {folder_name}", False)
            return folder_name
        self.logger.warning(
            f"folder_name 参数 {folder_name} 不是有效的文件夹名称，程序将使用默认值：Download")
        return "Download"

    def check_name_format(self, name_format: str) -> list[str]:
        name_keys = name_format.strip().split(" ")
        if all(i in self.name_keys for i in name_keys):
            self.logger.info(f"name_format 参数已设置为 {name_format}", False)
            return name_keys
        else:
            self.logger.warning(
                f"name_format 参数 {name_format} 设置错误，程序将使用默认值：创建时间 作品类型 账号昵称 作品描述")
            return ["create_time", "type", "nickname", "desc"]

    def check_date_format(self, date_format: str) -> str:
        try:
            _ = strftime(date_format, localtime())
            self.logger.info(f"date_format 参数已设置为 {date_format}", False)
            return date_format
        except ValueError:
            self.logger.warning(
                f"date_format 参数 {date_format} 设置错误，程序将使用默认值：年-月-日 时:分:秒")
            return "%Y-%m-%d %H:%M:%S"

    def check_split(self, split: str) -> str:
        for i in split:
            if i in self.cleaner.rule.keys():
                self.logger.warning(f"split 参数 {split} 包含非法字符，程序将使用默认值：-")
                return "-"
        self.logger.info(f"split 参数已设置为 {split}", False)
        return split

    def check_proxies(self, proxies: str) -> dict:
        if isinstance(proxies, str) and proxies:
            proxies_dict = {
                "http": proxies,
                "https": proxies,
                "ftp": proxies,
            }
            try:
                response = get(
                    "https://www.baidu.com/", proxies=proxies_dict, timeout=10)
                if response.status_code == 200:
                    self.logger.info(f"代理 {proxies} 测试成功")
                    return proxies_dict
            except exceptions.ReadTimeout:
                self.logger.warning(f"代理 {proxies} 测试超时")
            except (
                    exceptions.ProxyError,
                    exceptions.SSLError,
                    exceptions.ChunkedEncodingError,
                    exceptions.ConnectionError,
            ):
                self.logger.warning(f"代理 {proxies} 测试失败")
        return {
            "http": None,
            "https": None,
            "ftp": None,
        }

    def check_max_size(self, max_size: int) -> int:
        max_size = max(max_size, 0)
        self.logger.info(f"max_size 参数已设置为 {max_size}", False)
        return max_size

    def check_chunk(self, chunk: int) -> int:
        if isinstance(chunk, int) and chunk > 1024:
            self.logger.info(f"chunk 参数已设置为 {chunk}", False)
            return chunk
        self.logger.warning(
            f"chunk 参数 {chunk} 设置错误，程序将使用默认值：{
            1024 * 1024}", False)
        return 1024 * 1024

    def check_max_retry(self, max_retry: int) -> int:
        if isinstance(max_retry, int) and max_retry >= 0:
            self.logger.info(f"max_retry 参数已设置为 {max_retry}", False)
            return max_retry
        self.logger.warning(f"max_retry 参数 {max_retry} 设置错误，程序将使用默认值：5", False)
        return 5

    def check_max_pages(self, max_pages: int) -> int:
        if isinstance(max_pages, int) and max_pages > 0:
            self.logger.info(f"max_pages 参数已设置为 {max_pages}", False)
            return max_pages
        elif max_pages != 0:
            self.logger.warning(
                f"max_pages 参数 {max_pages} 设置错误，程序将使用默认值：99999", False)
        return 99999

    def check_timeout(self, timeout: int | float) -> int | float:
        if isinstance(timeout, (int, float)) and timeout > 0:
            self.logger.info(f"timeout 参数已设置为 {timeout}", False)
            return timeout
        self.logger.warning(f"timeout 参数 {timeout} 设置错误，程序将使用默认值：10")
        return 10

    def check_storage_format(self, storage_format: str) -> str:
        if storage_format in RecordManager.DataLogger.keys():
            self.logger.info(f"storage_format 参数已设置为 {storage_format}", False)
            return storage_format
        if not storage_format:
            self.logger.info("storage_format 参数未设置，程序不会储存任何数据至文件", False)
        else:
            self.logger.warning(
                f"storage_format 参数 {storage_format} 设置错误，程序默认不会储存任何数据至文件")
        return ""

    def check_default_mode(self, default_mode: int) -> str:
        if default_mode in range(3, 7):
            return str(default_mode)
        if default_mode:
            self.logger.warning(f"default_mode 参数 {default_mode} 设置错误")
        return "0"

    def update_cookie(self) -> None:
        # self.console.print("Update Cookie")
        if self.cookie:
            self.add_cookie(self.cookie)
            self.headers["Cookie"] = Register.generate_cookie(self.cookie)
        elif self.cookie_cache:
            self.headers["Cookie"] = self.add_cookie(self.cookie_cache)

    @staticmethod
    def _generate_ffmpeg_object(ffmpeg_path: str) -> FFMPEG:
        return FFMPEG(ffmpeg_path)

    def get_settings_data(self) -> dict:
        return {
            "accounts_urls": [vars(i) for i in self.accounts_urls],
            "mix_urls": [vars(i) for i in self.mix_urls],
            "owner_url": vars(self.owner_url),
            "root": str(self.root.resolve()),
            "folder_name": self.folder_name,
            "name_format": " ".join(self.name_format),
            "date_format": self.date_format,
            "split": self.split,
            "folder_mode": self.folder_mode,
            "music": self.music,
            "storage_format": self.storage_format,
            "cookie": self.cookie_cache or self.cookie,
            "dynamic_cover": self.dynamic_cover,
            "original_cover": self.original_cover,
            "proxies": self.proxies["https"] or "",
            "download": self.download,
            "max_size": self.max_size,
            "chunk": self.chunk,
            "max_retry": self.max_retry,
            "max_pages": self.max_pages,
            "default_mode": int(self.default_mode),
            "ffmpeg": self.ffmpeg.path or "",
        }

    def update_settings_data(self, data: dict, ) -> dict:
        for key, value in data.items():
            if key in list(self.check_rules.keys())[3:]:
                # print(key, hasattr(self, key))  # 调试使用
                setattr(self, key, self.check_rules[key](value))
        if c := data.get("cookie"):
            setattr(
                self,
                "cookie",
                self.cookie_object.extract(
                    c,
                    return_=True))
            self.update_cookie()
        self.settings.update(data := self.get_settings_data())
        # print(data)  # 调试使用
        return data
