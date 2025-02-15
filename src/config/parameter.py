from pathlib import Path
from time import localtime
from time import strftime
from types import SimpleNamespace
from typing import TYPE_CHECKING
from typing import Type

from httpx import HTTPStatusError
from httpx import RequestError
from httpx import TimeoutException
from httpx import get

from ..custom import BLANK_PREVIEW
from ..custom import (
    DATA_HEADERS,
    DOWNLOAD_HEADERS,
    PROJECT_ROOT,
    DOWNLOAD_HEADERS_TIKTOK,
    PARAMS_HEADERS,
    QRCODE_HEADERS,
    PARAMS_HEADERS_TIKTOK,
    DATA_HEADERS_TIKTOK,
    USERAGENT,
    TIMEOUT,
)
from ..encrypt import ABogus
from ..encrypt import MsToken
from ..encrypt import MsTokenTikTok
from ..encrypt import TtWid
from ..encrypt import TtWidTikTok
from ..encrypt import XBogus
from ..extract import Extractor
from ..interface import API
from ..interface import APITikTok
from ..module import FFMPEG
from ..record import BaseLogger
from ..record import LoggerManager
from ..storage import RecordManager
from ..tools import Cleaner
from ..tools import cookie_dict_to_str
from ..tools import create_client
from ..translation import _

if TYPE_CHECKING:
    from ..manager import DownloadRecorder
    from ..tools import ColorfulConsole
    from .settings import Settings
    from ..module import Cookie

__all__ = ["Parameter"]


class Parameter:
    NAME_KEYS = (
        "id",
        "desc",
        "create_time",
        "nickname",
        "uid",
        "mark",
        "type",
    )
    CLEANER = Cleaner()
    HEADERS = {"User-Agent": USERAGENT}
    NO_PROXY = {
        "http://": None,
        "https://": None,
    }

    def __init__(
            self,
            settings: "Settings",
            cookie_object: "Cookie",
            logger: Type[BaseLogger | LoggerManager],
            console: "ColorfulConsole",
            cookie: dict | str,
            cookie_tiktok: dict | str,
            root: str,
            accounts_urls: list[dict],
            accounts_urls_tiktok: list[dict],
            mix_urls: list[dict],
            mix_urls_tiktok: list[dict],
            folder_name: str,
            name_format: str,
            date_format: str,
            split: str,
            music: bool,
            folder_mode: bool,
            truncate: int,
            storage_format: str,
            dynamic_cover: bool,
            original_cover: bool,
            proxy: str | None | dict,
            proxy_tiktok: str | None | dict,
            twc_tiktok: str,
            download: bool,
            max_size: int,
            chunk: int,
            max_retry: int,
            max_pages: int,
            run_command: str,
            owner_url: dict,
            owner_url_tiktok: dict,
            ffmpeg: str,
            recorder: "DownloadRecorder",
            browser_info: dict,
            browser_info_tiktok: dict,
            timeout=10,
            douyin_platform=True,
            tiktok_platform=True,
            **kwargs,
    ):
        self.settings = settings
        self.cookie_object = cookie_object
        self.ROOT = PROJECT_ROOT  # 项目根路径
        self.cache = PROJECT_ROOT.joinpath("cache")  # 缓存路径
        self.headers = DATA_HEADERS
        self.headers_tiktok = DATA_HEADERS_TIKTOK
        self.headers_download = DOWNLOAD_HEADERS
        self.headers_download_tiktok = DOWNLOAD_HEADERS_TIKTOK
        self.headers_params = PARAMS_HEADERS
        self.headers_params_tiktok = PARAMS_HEADERS_TIKTOK
        self.headers_qrcode = QRCODE_HEADERS
        self.logger = logger(PROJECT_ROOT, console)
        self.logger.run()
        self.ab = ABogus()
        self.xb = XBogus()
        self.console = console
        self.douyin_platform = self.__check_bool(douyin_platform, True)
        self.tiktok_platform = self.__check_bool(tiktok_platform, True)
        self.cookie, self.cookie_cache = self.__check_cookie(cookie)
        self.cookie_tiktok, self.cookie_tiktok_cache = self.__check_cookie_tiktok(
            cookie_tiktok,
        )
        self.cookie_state: bool = self.__check_cookie_state()
        self.cookie_tiktok_state: bool = self.__check_cookie_state(True)
        self.root = self.__check_root(root)
        self.folder_name = self.__check_folder_name(folder_name)
        self.name_format = self.__check_name_format(name_format)
        self.date_format = self.__check_date_format(date_format)
        self.split = self.__check_split(split)
        self.music = self.__check_bool(music)
        self.folder_mode = self.__check_bool(folder_mode)
        self.storage_format = self.__check_storage_format(storage_format)
        self.dynamic_cover = self.__check_bool(dynamic_cover)
        self.original_cover = self.__check_bool(original_cover)
        self.timeout = self.__check_timeout(timeout)
        self.proxy: str | None = self.__check_proxy(
            proxy,
            remark=_("抖音"),
            enable=self.douyin_platform,
        )
        self.proxy_tiktok: str | None = self.__check_proxy_tiktok(proxy_tiktok)
        self.download = self.__check_bool(download)
        self.max_size = self.__check_max_size(max_size)
        self.chunk = self.__check_chunk(chunk)
        self.max_retry = self.__check_max_retry(max_retry)
        self.max_pages = self.__check_max_pages(max_pages)
        self.recorder = recorder
        self.accounts_urls: list[SimpleNamespace] = Extractor.generate_data_object(
            accounts_urls
        )
        self.accounts_urls_tiktok: list[SimpleNamespace] = (
            Extractor.generate_data_object(accounts_urls_tiktok)
        )
        self.mix_urls: list[SimpleNamespace] = Extractor.generate_data_object(mix_urls)
        self.mix_urls_tiktok: list[SimpleNamespace] = Extractor.generate_data_object(
            mix_urls_tiktok
        )
        self.owner_url: SimpleNamespace = Extractor.generate_data_object(owner_url)
        self.owner_url_tiktok: SimpleNamespace = Extractor.generate_data_object(
            owner_url_tiktok
        )
        self.run_command = self.__check_run_command(run_command)
        self.preview = BLANK_PREVIEW
        self.ffmpeg = self.__generate_ffmpeg_object(ffmpeg)
        self.client = create_client(
            timeout=self.timeout,
            proxy=self.proxy,
        )
        self.client_tiktok = create_client(
            timeout=self.timeout,
            proxy=self.proxy_tiktok,
        )
        # TODO: 未更新代码
        self.check_rules = {
            "accounts_urls": self.__check_accounts_urls,
            "mix_urls": self.__check_mix_urls,
            "owner_url": self.__check_owner_url,
            "accounts_urls_tiktok": self.__check_accounts_urls,
            "mix_urls_tiktok": self.__check_mix_urls,
            "owner_url_tiktok": self.__check_owner_url,
            "root": self.__check_root,
            "folder_name": self.__check_folder_name,
            "name_format": self.__check_name_format,
            "date_format": self.__check_date_format,
            "split": self.__check_split,
            "folder_mode": self.__check_bool,
            "music": self.__check_bool,
            "storage_format": self.__check_storage_format,
            "dynamic_cover": self.__check_bool,
            "original_cover": self.__check_bool,
            "proxy": self.__check_proxy,
            "proxy_tiktok": self.__check_proxy_tiktok,
            "download": self.__check_bool,
            "max_size": self.__check_max_size,
            "chunk": self.__check_chunk,
            "max_retry": self.__check_max_retry,
            "max_pages": self.__check_max_pages,
            "run_command": self.__check_run_command,
            "ffmpeg": self.__generate_ffmpeg_object,
        }
        self.twc_tiktok = twc_tiktok if isinstance(twc_tiktok, str) else ""
        self.truncate = self.__check_truncate(truncate)
        self.ms_token = ""
        self.ms_token_tiktok = ""
        self.__check_browser_info(browser_info)
        self.__check_browser_info_tiktok(browser_info_tiktok)
        self.__generate_folders()
        self._set_download_headers()

    @staticmethod
    def __check_bool(value: bool, default=False) -> bool:
        return value if isinstance(value, bool) else default

    def __check_cookie_tiktok(
            self,
            cookie: dict | str,
    ) -> [dict, str]:
        # if isinstance(cookie, str):
        #     self.console.print(
        #         "参数 cookie_tiktok 应为字典格式！请修改配置文件后重新运行程序！",
        #         style=ERROR)
        return self.__check_cookie(cookie, name="cookie_tiktok")

    def __check_cookie(self, cookie: dict | str, name="cookie") -> [dict, str]:
        if isinstance(cookie, dict):
            return cookie, ""
        elif isinstance(cookie, str):
            return {}, cookie
        else:
            self.logger.warning(_("{name} 参数格式错误").format(name=name))
        return {}, ""

    def __get_cookie(
            self,
            cookie: dict,
    ) -> dict:
        return self.__check_cookie(cookie)[0]

    def __get_cookie_cache(
            self,
            cookie: str,
    ) -> str:
        return self.__check_cookie(cookie)[1]

    def __get_cookie_tiktok(
            self,
            cookie: dict,
    ) -> dict:
        return self.__check_cookie_tiktok(cookie)[0]

    def __get_cookie_tiktok_cache(
            self,
            cookie: str,
    ) -> str:
        return self.__check_cookie_tiktok(cookie)[1]

    async def __add_cookie(
            self,
            cookie: dict | str,
            tiktok=False,
            token="",
    ) -> None | str:
        if tiktok:
            parameters = (
                # await MsTokenTikTok.get_long_ms_token(
                #     self.logger,
                #     self.headers_params_tiktok,
                #     token,
                #     **self.proxy_tiktok,
                # ),
                {
                    "msToken": self.ms_token_tiktok,
                },
                await TtWidTikTok.get_tt_wid(
                    self.logger,
                    self.headers_params_tiktok,
                    self.twc_tiktok
                    or f"{TtWidTikTok.NAME}={cookie.get(TtWidTikTok.NAME, '')}",
                    proxy=self.proxy_tiktok,
                ),
            )
        else:
            parameters = (
                # await MsToken.get_real_ms_token(
                #     self.logger,
                #     self.headers_params,
                #     token,
                #     **self.proxy,
                # ),
                {
                    "msToken": self.ms_token,
                },
                await TtWid.get_tt_wid(
                    self.logger,
                    self.headers_params,
                    proxy=self.proxy,
                ),
            )
        if isinstance(cookie, dict):
            for i in parameters:
                if isinstance(i, dict):
                    self.logger.info(
                        f"参数: {i}",
                        False,
                    )
                    cookie |= i
        elif isinstance(cookie, str):
            for i in parameters:
                if isinstance(i, dict):
                    self.logger.info(
                        f"参数: {i}",
                        False,
                    )
                    cookie += cookie_dict_to_str(i)
            return cookie

    def __check_root(self, root: str) -> Path:
        if not root:
            return self.ROOT
        if (r := Path(root)).is_dir():
            self.logger.info(f"root 参数已设置为 {root}", False)
            return r
        if r := self.__check_root_again(r):
            self.logger.info(f"root 参数已设置为 {r}", False)
            return r
        self.logger.warning(
            _(
                "root 参数 {root} 不是有效的文件夹路径，程序将使用项目根路径作为储存路径"
            ).format(root=root),
        )
        return self.ROOT

    @staticmethod
    def __check_root_again(root: Path) -> bool | Path:
        if root.resolve().parent.is_dir():
            root.mkdir()
            return root
        return False

    def __check_folder_name(self, folder_name: str) -> str:
        if folder_name := self.CLEANER.filter_name(
                folder_name,
        ):
            self.logger.info(f"folder_name 参数已设置为 {folder_name}", False)
            return folder_name
        self.logger.warning(
            _(
                "folder_name 参数 {folder_name} 不是有效的文件夹名称，程序将使用默认值：Download"
            ).format(folder_name=folder_name),
        )
        return "Download"

    def __check_name_format(self, name_format: str) -> list[str]:
        name_keys = name_format.strip().split(" ")
        if all(i in self.NAME_KEYS for i in name_keys):
            self.logger.info(f"name_format 参数已设置为 {name_format}", False)
            return name_keys
        else:
            self.logger.warning(
                _(
                    "name_format 参数 {name_format} 设置错误，程序将使用默认值：创建时间 作品类型 账号昵称 作品描述"
                ).format(name_format=name_format)
            )
            return ["create_time", "type", "nickname", "desc"]

    def __check_date_format(self, date_format: str) -> str:
        try:
            strftime(date_format, localtime())
            self.logger.info(f"date_format 参数已设置为 {date_format}", False)
            return date_format
        except ValueError:
            self.logger.warning(
                _(
                    "date_format 参数 {date_format} 设置错误，程序将使用默认值：年-月-日 时:分:秒"
                ).format(date_format=date_format),
            )
            return "%Y-%m-%d %H:%M:%S"

    def __check_split(self, split: str) -> str:
        for i in split:
            if i in self.CLEANER.rule.keys():
                self.logger.warning(
                    _("split 参数 {split} 包含非法字符，程序将使用默认值：-").format(
                        split=split
                    )
                )
                return "-"
        self.logger.info(f"split 参数已设置为 {split}", False)
        return split

    def __check_proxy_tiktok(
            self,
            proxy: str | None | dict,
    ) -> str | None:
        return self.__check_proxy(
            proxy,
            "https://www.tiktok.com/explore",
            "TikTok",
            self.tiktok_platform,
        )

    def __check_proxy(
            self,
            proxy: str | None | dict,
            url="https://www.douyin.com/?recommend=1",
            remark=_("抖音"),
            enable=True,
    ) -> str | None:
        if enable and proxy:
            # 暂时兼容旧版配置；未来将会移除
            if isinstance(proxy, dict):
                self.console.warning(
                    _("{remark}代理参数应为字符串格式，未来不再支持字典格式").format(
                        remark=remark
                    )
                )
                if not (proxy := proxy.get("https://")):
                    return
            try:
                response = get(
                    url,
                    headers=self.HEADERS,
                    follow_redirects=True,
                    timeout=TIMEOUT,
                    proxy=proxy,
                )
                response.raise_for_status()
                self.logger.info(
                    _("{remark}代理 {proxy} 测试成功").format(
                        remark=remark, proxy=proxy
                    )
                )
                return proxy
            except TimeoutException:
                self.logger.warning(
                    _("{remark}代理 {proxy} 测试超时").format(
                        remark=remark, proxy=proxy
                    )
                )
            except (
                    RequestError,
                    HTTPStatusError,
            ) as e:
                self.logger.warning(
                    _("{remark}代理 {proxy} 测试失败：{error}").format(
                        remark=remark, proxy=proxy, error=e
                    ),
                )

    def __check_max_size(self, max_size: int) -> int:
        max_size = max(max_size, 0)
        self.logger.info(f"max_size 参数已设置为 {max_size}", False)
        return max_size

    def __check_chunk(self, chunk: int) -> int:
        if isinstance(chunk, int) and chunk > 1024:
            self.logger.info(f"chunk 参数已设置为 {chunk}", False)
            return chunk
        self.logger.warning(
            _("chunk 参数 {chunk} 设置错误，程序将使用默认值：{default_chunk}").format(
                chunk=chunk,
                default_chunk=1024 * 1024 * 2,
            ),
        )
        return 1024 * 1024 * 2

    def __check_max_retry(self, max_retry: int) -> int:
        if isinstance(max_retry, int) and max_retry >= 0:
            self.logger.info(f"max_retry 参数已设置为 {max_retry}", False)
            return max_retry
        self.logger.warning(
            _("max_retry 参数 {max_retry} 设置错误，程序将使用默认值：5").format(
                max_retry=max_retry
            ),
        )
        return 5

    def __check_max_pages(self, max_pages: int) -> int:
        if isinstance(max_pages, int) and max_pages > 0:
            self.logger.info(f"max_pages 参数已设置为 {max_pages}", False)
            return max_pages
        elif max_pages != 0:
            self.logger.warning(
                _(
                    "max_pages 参数 {max_pages} 设置错误，程序将使用默认值：99999"
                ).format(max_pages=max_pages),
            )
        return 99999

    def __check_timeout(self, timeout: int | float) -> int | float:
        if isinstance(timeout, (int, float)) and timeout > 0:
            self.logger.info(f"timeout 参数已设置为 {timeout}", False)
            return timeout
        self.logger.warning(
            _("timeout 参数 {timeout} 设置错误，程序将使用默认值：10").format(
                timeout=timeout
            )
        )
        return 10

    def __check_storage_format(self, storage_format: str) -> str:
        if storage_format in RecordManager.DataLogger.keys():
            self.logger.info(f"storage_format 参数已设置为 {storage_format}", False)
            return storage_format
        if not storage_format:
            self.logger.info(
                "storage_format 参数未设置，程序不会储存任何数据至文件", False
            )
        else:
            self.logger.warning(
                _(
                    "storage_format 参数 {storage_format} 设置错误，程序默认不会储存任何数据至文件"
                ).format(storage_format=storage_format),
            )
        return ""

    @staticmethod
    def __check_run_command(run_command: str) -> list:
        return run_command.split()[::-1] if run_command else []

    async def update_params(self) -> None:
        self.set_uif_id()
        if self.douyin_platform:
            self.console.info(
                _("正在更新抖音参数，请稍等..."),
            )
            await self.__get_token_params()
            API.params["msToken"] = self.ms_token
            await self.__update_cookie(
                self.headers, self.cookie, self.cookie_cache, False
            )
            self.console.info(
                _("抖音参数更新完毕！"),
            )
        if self.tiktok_platform:
            self.console.info(
                "正在更新 TikTok 参数，请稍等...",
            )
            await self.__get_token_params_tiktok()
            APITikTok.params["msToken"] = self.ms_token_tiktok
            await self.__update_cookie(
                self.headers_tiktok,
                self.cookie_tiktok,
                self.cookie_tiktok_cache,
                True,
            )
            self.console.info(
                _("TikTok 参数更新完毕！"),
            )

    async def __update_cookie(
            self,
            headers: dict,
            cookie: dict,
            cache: str,
            tiktok=False,
    ) -> None:
        if cookie:
            await self.__add_cookie(cookie, tiktok, cookie.get("msToken"))
            headers["Cookie"] = cookie_dict_to_str(cookie)
        elif cache:
            headers["Cookie"] = await self.__add_cookie(
                cache,
                tiktok,
            )

    def set_headers_cookie(
            self,
    ) -> None:
        if self.cookie:
            self.headers["Cookie"] = cookie_dict_to_str(self.cookie)
        elif self.cookie_cache:
            self.headers["Cookie"] = self.cookie_cache
        if self.cookie_tiktok:
            self.headers_tiktok["Cookie"] = cookie_dict_to_str(self.cookie_tiktok)
        elif self.cookie_tiktok_cache:
            self.headers_tiktok["Cookie"] = self.cookie_tiktok_cache

    def _set_download_headers(self) -> None:
        self.__update_download_headers()
        self.__update_download_headers_tiktok()

    def __update_download_headers(self) -> None:
        self.headers_download["Cookie"] = "dy_swidth=1536; dy_sheight=864"

    def __update_download_headers_tiktok(self) -> None:
        key = "tt_chain_token"
        if tk := self.cookie_tiktok.get(
                key,
        ):
            self.headers_download_tiktok["Cookie"] = f"{key}={tk}"
        else:
            self.headers_download_tiktok["Cookie"] = self.cookie_tiktok_cache
        # self.headers_download_tiktok["Cookie"] = self.headers_tiktok.get(
        #     "Cookie", "")

    async def set_token_params(self):
        await self.__get_token_params()
        await self.__get_token_params_tiktok()
        API.params["msToken"] = self.ms_token
        APITikTok.params["msToken"] = self.ms_token_tiktok

    async def __get_token_params(self):
        if not self.douyin_platform:
            return
        if not any(
                (
                        self.cookie,
                        self.cookie_cache,
                )
        ):
            self.logger.warning(_("抖音 cookie 参数未设置，相应功能可能无法正常使用"))
            return
        # if not (m := self.cookie.get("msToken")):
        #     self.logger.warning("抖音 cookie 缺少必需的键值对，请尝试重新写入 cookie")
        #     return
        if d := await MsToken.get_real_ms_token(
                self.logger,
                self.headers_params,
                # m,
                proxy=self.proxy,
        ):
            # self.cookie |= d
            self.ms_token = d[MsToken.NAME]
            self.logger.info(
                f"抖音 MsToken 请求值: {self.ms_token}",
                False,
            )
        else:
            self.ms_token = self.cookie.get("msToken", "")
            self.logger.info(
                f"抖音 MsToken 本地值: {self.ms_token}",
                False,
            )

    async def __get_token_params_tiktok(self):
        if not self.tiktok_platform:
            return
        if not any(
                (
                        self.cookie_tiktok,
                        self.cookie_tiktok_cache,
                )
        ):
            self.logger.warning(_("TikTok cookie 参数未设置，相应功能可能无法正常使用"))
            return
        if not (m := self.cookie_tiktok.get("msToken")):
            self.logger.warning(
                _("TikTok cookie 缺少必需的键值对，请尝试重新写入 cookie")
            )
            return
        if d := await MsTokenTikTok.get_long_ms_token(
                self.logger,
                self.headers_params_tiktok,
                m,
                proxy=self.proxy_tiktok,
        ):
            # self.cookie_tiktok |= d
            self.ms_token_tiktok = d[MsTokenTikTok.NAME]
            self.logger.info(
                f"TikTok MsToken 请求值: {self.ms_token}",
                False,
            )
        else:
            self.ms_token = self.cookie_tiktok.get("msToken", "")
            self.logger.info(
                f"TikTok MsToken 本地值: {self.ms_token}",
                False,
            )

    def set_uif_id(
            self,
    ) -> None:
        self.deal_uif_id()
        self.deal_uif_id_tiktok()

    def deal_uif_id(
            self,
    ) -> None:
        API.params["uifid"] = self.cookie.get("UIFID", "")

    def deal_uif_id_tiktok(
            self,
    ) -> None:
        # APITikTok.params["uifid"] = self.cookie_tiktok.get("UIFID", "")
        pass

    @staticmethod
    def __generate_ffmpeg_object(ffmpeg_path: str) -> FFMPEG:
        return FFMPEG(ffmpeg_path)

    def get_settings_data(self) -> dict:
        # TODO: 未更新代码
        return {
            "accounts_urls": [vars(i) for i in self.accounts_urls],
            "accounts_urls_tiktok": [vars(i) for i in self.accounts_urls_tiktok],
            "mix_urls": [vars(i) for i in self.mix_urls],
            "mix_urls_tiktok": [vars(i) for i in self.mix_urls_tiktok],
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
            "cookie_tiktok": self.cookie_tiktok_cache or self.cookie_tiktok,
            "dynamic_cover": self.dynamic_cover,
            "original_cover": self.original_cover,
            "proxy": self.proxy,
            "proxy_tiktok": self.proxy_tiktok,
            "download": self.download,
            "max_size": self.max_size,
            "chunk": self.chunk,
            "max_retry": self.max_retry,
            "max_pages": self.max_pages,
            "run_command": " ".join(self.run_command[::-1]),
            "ffmpeg": self.ffmpeg.path or "",
        }

    async def update_settings_data(
            self,
            data: dict,
    ) -> dict:
        keys = list(self.check_rules.keys())[6:]
        for key, value in data.items():
            if key in keys:
                # print(key, hasattr(self, key))  # 调试使用
                setattr(self, key, self.check_rules[key](value))
        await self.__update_cookie_data(data)
        self.settings.update(data := self.get_settings_data())
        # print(data)  # 调试使用
        return data

    async def __update_cookie_data(self, data: dict) -> None:
        for i in ("cookie", "cookie_tiktok"):
            if c := data.get(i):
                setattr(self, i, self.cookie_object.extract(c, False, key=i))
        await self.update_params()

    def __check_accounts_urls(self, data: list[dict]) -> list[dict]:
        pass

    def __check_mix_urls(self, data: list[dict]) -> list[dict]:
        pass

    def __check_owner_url(self, data: list[dict]) -> list[dict]:
        pass

    async def close_client(self) -> None:
        await self.client.aclose()
        await self.client_tiktok.aclose()

    def __generate_folders(self):
        self.cache.mkdir(exist_ok=True)

    def __check_browser_info(
            self,
            info: dict,
    ):
        self.logger.info(f"抖音浏览器信息: {info}", False)
        for j in (
                self.headers,
                self.headers_download,
                self.headers_params,
                self.headers_qrcode,
        ):
            if v := info.get(
                    "User-Agent",
            ):
                j["User-Agent"] = v
        for i in (
                "pc_libra_divert",
                "browser_platform",
                "browser_name",
                "browser_version",
                "engine_name",
                "engine_version",
                "os_name",
                "os_version",
                # 'webid',
        ):
            if v := info.get(
                    i,
            ):
                API.params[i] = v

    def __check_browser_info_tiktok(
            self,
            info: dict,
    ):
        self.logger.info(f"TikTok 浏览器信息: {info}", False)
        for j in (
                self.headers_tiktok,
                self.headers_download_tiktok,
                self.headers_params_tiktok,
        ):
            if v := info.get(
                    "User-Agent",
            ):
                j["User-Agent"] = v
        for i in (
                "app_language",
                "browser_language",
                "browser_name",
                "browser_platform",
                "browser_version",
                "language",
                "os",
                "priority_region",
                "region",
                "tz_name",
                "webcast_language",
                "device_id",
        ):
            if v := info.get(
                    i,
            ):
                APITikTok.params[i] = v

    def __check_truncate(self, truncate: int) -> int:
        if isinstance(truncate, int) and truncate >= 32:
            self.logger.info(f"truncate 参数已设置为 {truncate}", False)
            return truncate
        self.logger.warning(
            _("truncate 参数 {truncate} 设置错误，程序将使用默认值：50").format(
                truncate=truncate
            ),
        )
        return 50

    def __check_cookie_state(self, tiktok=False) -> bool:
        if tiktok:
            return (self.cookie_object.STATE_KEY in self.cookie_tiktok) or (
                    self.cookie_object.STATE_KEY in self.cookie_tiktok_cache
            )
        return (self.cookie_object.STATE_KEY in self.cookie) or (
                self.cookie_object.STATE_KEY in self.cookie_cache
        )
