from json import dump
from json import load
from json.decoder import JSONDecodeError
from pathlib import Path
from platform import system
from shutil import which
from subprocess import Popen
from time import localtime
from time import strftime
from types import SimpleNamespace

from requests import exceptions
from requests import get

from src.CookieTool import Register
from src.DataExtractor import Extractor
from src.Parameter import MsToken
from src.Parameter import TtWid
from src.StringCleaner import Cleaner
from src.custom import INFO, ERROR

__all__ = ["Settings", "Parameter"]


class Settings:
    encode = "UTF-8-SIG" if system() == "Windows" else "UTF-8"

    def __init__(self, root: Path, console):
        self.file = root.joinpath("./settings.json")  # 配置文件
        self.console = console
        self.__default = {
            "accounts_urls": [
                {"mark": "账号标识，可以设置为空字符串",
                 "url": "账号主页链接",
                 "tab": "账号主页类型",
                 "earliest": "作品最早发布日期",
                 "latest": "作品最晚发布日期"},
            ],
            "mix_urls": [
                {"mark": "合集标识，可以设置为空字符串",
                 "url": "合集链接或者作品链接"},
            ],
            "owner_url": {"mark": "账号标识，可以设置为空字符串",
                          "url": "账号主页链接", },
            "root": "",
            "folder_name": "Download",
            "name_format": "create_time type nickname desc",
            "date_format": "%Y-%m-%d %H:%M:%S",
            "split": "-",
            "folder_mode": False,
            "music": False,
            "storage_format": "",
            "cookie": "",
            "dynamic_cover": False,
            "original_cover": False,
            "proxies": "",
            "download": True,
            "max_size": 0,
            "chunk": 1024 * 1024,  # 每次从服务器接收的数据块大小
            "max_retry": 5,  # 重试最大次数
            "max_pages": 0,
            "default_mode": 0,
            "ffmpeg": "",
        }  # 默认配置

    def __create(self) -> dict:
        """创建默认配置文件"""
        with self.file.open("w", encoding=self.encode) as f:
            dump(self.__default, f, indent=4, ensure_ascii=False)
        self.console.print(
            "创建默认配置文件 settings.json 成功！\n请参考项目文档的快速入门部分，设置 Cookie 后重新运行程序！\n建议根据实际使用需求"
            "修改配置文件 settings.json！\n")
        return self.__default

    def read(self) -> dict:
        """读取配置文件，如果没有配置文件，则生成配置文件"""
        try:
            if self.file.exists():
                with self.file.open("r", encoding=self.encode) as f:
                    return self.__check(load(f))
            return self.__create()  # 生成的默认配置文件必须要设置 cookie 才可以正常运行
        except JSONDecodeError:
            self.console.print(
                "配置文件 settings.json 格式错误，请检查 JSON 格式！",
                style=ERROR)
            return self.__default  # 读取配置文件发生错误时返回空配置

    def __check(self, data: dict) -> dict:
        if set(self.__default.keys()).issubset(set(data.keys())):
            return data
        if self.console.input(
                f"[{ERROR}]配置文件 settings.json 缺少必要的参数，是否需要生成默认配置文件(YES/NO): [/{ERROR}]").upper() == "YES":
            self.__create()
        self.console.print("本次运行将会使用各项参数默认值，程序功能可能无法正常使用！")
        return self.__default

    def update(self, settings: dict | SimpleNamespace):
        """更新配置文件"""
        with self.file.open("w", encoding=self.encode) as f:
            dump(
                settings if isinstance(
                    settings,
                    dict) else vars(settings),
                f,
                indent=4,
                ensure_ascii=False)
        self.console.print("保存配置成功！", style=INFO)


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
            settings,
            cookie_object,
            main_path: Path,
            user_agent: str,
            ua_code: tuple,
            logger,
            xb,
            console,
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
            blacklist,
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
        self.music = music
        self.folder_mode = folder_mode
        self.storage_format = self.check_storage_format(storage_format)
        self.dynamic_cover = dynamic_cover
        self.original_cover = original_cover
        self.proxies = self.check_proxies(proxies)
        self.download = download
        self.max_size = self.check_max_size(max_size)
        self.chunk = self.check_chunk(chunk)
        self.max_retry = self.check_max_retry(max_retry)
        self.max_pages = self.check_max_pages(max_pages)
        self.blacklist = blacklist
        self.timeout = self.check_timeout(timeout)
        self.accounts_urls = Extractor.generate_data_object(accounts_urls)
        self.mix_urls = Extractor.generate_data_object(mix_urls)
        self.owner_url = Extractor.generate_data_object(owner_url)
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
    def _check_bool(value: bool) -> bool:
        return value if isinstance(value, bool) else False

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
        if storage_format in {"xlsx", "csv", "sql"}:
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

    def update_cookie(self):
        # self.console.print("Update Cookie")
        if self.cookie:
            self.add_cookie(self.cookie)
            self.headers["Cookie"] = Register.generate_cookie(self.cookie)
        elif self.cookie_cache:
            self.headers["Cookie"] = self.add_cookie(self.cookie_cache)

    @staticmethod
    def _generate_ffmpeg_object(ffmpeg_path: str):
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

    def update_settings_data(self, data: dict, ):
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


class FFMPEG:
    def __init__(self, path: str):
        self.path = self.__check_ffmpeg_path(Path(path))
        self.state = bool(self.path)
        self.command, self.shell = self._check_system_type()

    @staticmethod
    def _check_system_type():
        if (s := system()) == "Darwin":  # macOS
            return ['open', '-a', 'Terminal'], False
        elif s == "Windows":  # Windows
            return ['start', 'cmd', '/k'], True
        elif s == "Linux":  # Linux
            return ['x-terminal-emulator'], False

    def __check_ffmpeg_path(self, path: Path):
        # return None  # 调试使用
        return self.__check_system_ffmpeg() or self.__check_system_ffmpeg(path)

    def download(self, data: list[tuple], proxies, timeout, user_agent):
        for u, p in data:
            command = self.__generate_command(
                u, p, proxies, timeout, user_agent)
            Popen(command, shell=self.shell)

    def __generate_command(
            self,
            url,
            file,
            proxies,
            timeout,
            user_agent) -> str:
        command = self.command.copy()
        command.extend([
            self.path,
            "-hide_banner",
            "-log_level", "error",
            "-protocol_whitelist", "rtmp,crypto,file,http,https,tcp,tls,udp,rtp",
            "-fflags", "+discardcorrupt",
            "-timeout", f"{timeout * 1000 * 1000}",
            "-user_agent", f'"{user_agent}"',
            "-i", f'"{url}"',
            "-bufsize", "5120k",
            "-map", "0",
            "-c:v", "copy",
            "-c:a", "copy",
            "-sn", "-dn",
            "-reconnect_delay_max", "15",
            "-reconnect_streamed", "-reconnect_at_eof",
            "-max_muxing_queue_size", "64",
            "-correct_ts_overflow", "1",
        ])
        if proxies:
            for insert_index, item in enumerate(
                    ("-http_proxy", proxies), start=len(self.command) + 2):
                command.insert(insert_index, item)
        command.append(f'"{file}"')
        # print(" ".join(command))  # 调试使用
        return " ".join(command)

    @staticmethod
    def __check_system_ffmpeg(path: Path = None):
        return which(path or "ffmpeg")
