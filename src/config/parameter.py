from pathlib import Path
from shutil import move
from time import localtime, strftime
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, Type

from httpx import HTTPStatusError, RequestError, TimeoutException, get

from ..custom import (
    BLANK_PREVIEW,
    DATA_HEADERS,
    DATA_HEADERS_TIKTOK,
    DOWNLOAD_HEADERS,
    DOWNLOAD_HEADERS_TIKTOK,
    PARAMS_HEADERS,
    PARAMS_HEADERS_TIKTOK,
    PROJECT_ROOT,
    QRCODE_HEADERS,
    TIMEOUT,
    USERAGENT,
)
from ..encrypt import ABogus, MsToken, MsTokenTikTok, TtWid, TtWidTikTok, XBogus
from ..extract import Extractor
from ..interface import API, APITikTok
from ..module import FFMPEG
from ..record import BaseLogger, LoggerManager
from ..storage import RecordManager
from ..tools import Cleaner, DownloaderError, cookie_dict_to_str, create_client
from ..translation import _

if TYPE_CHECKING:
    from ..manager import DownloadRecorder
    from ..module import Cookie
    from ..tools import ColorfulConsole
    from .settings import Settings

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
        static_cover: bool,
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
        live_qualities: str,
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
        self.cache = PROJECT_ROOT.joinpath("Cache")  # 缓存路径
        self.logger = logger(PROJECT_ROOT, console)
        self.logger.run()
        self.ab = ABogus()
        self.xb = XBogus()
        self.console = console
        self.recorder = recorder
        self.preview = BLANK_PREVIEW
        self.ms_token = ""
        self.ms_token_tiktok = ""

        self.headers = DATA_HEADERS
        self.headers_tiktok = DATA_HEADERS_TIKTOK
        self.headers_download = DOWNLOAD_HEADERS
        self.headers_download_tiktok = DOWNLOAD_HEADERS_TIKTOK
        self.headers_params = PARAMS_HEADERS
        self.headers_params_tiktok = PARAMS_HEADERS_TIKTOK
        self.headers_qrcode = QRCODE_HEADERS

        self.accounts_urls: list[SimpleNamespace] = self.check_urls_params(
            accounts_urls
        )
        self.accounts_urls_tiktok: list[SimpleNamespace] = self.check_urls_params(
            accounts_urls_tiktok
        )
        self.mix_urls: list[SimpleNamespace] = self.check_urls_params(mix_urls)
        self.mix_urls_tiktok: list[SimpleNamespace] = self.check_urls_params(
            mix_urls_tiktok
        )
        self.owner_url: SimpleNamespace = self.check_url_params(owner_url)
        self.owner_url_tiktok: SimpleNamespace | None = None

        self.cookie_dict, self.cookie_str = self.__check_cookie(cookie)
        self.cookie_dict_tiktok, self.cookie_str_tiktok = self.__check_cookie_tiktok(
            cookie_tiktok,
        )
        self.cookie_state: bool = self.__check_cookie_state()
        self.cookie_tiktok_state: bool = self.__check_cookie_state(True)
        self.set_uif_id()
        # self.set_download_headers()

        self.root = self.__check_root(root)
        self.folder_name = self.__check_folder_name(folder_name)
        self.name_format = self.__check_name_format(name_format)
        self.date_format = self.__check_date_format(date_format)
        self.split = self.__check_split(split)
        self.folder_mode = self.check_bool_false(folder_mode)
        self.music = self.check_bool_false(music)
        self.truncate = self.__check_truncate(truncate)
        self.storage_format = self.__check_storage_format(storage_format)
        self.dynamic_cover = self.check_bool_false(dynamic_cover)
        self.static_cover = self.check_bool_false(static_cover)
        self.twc_tiktok = self.check_str(twc_tiktok)
        self.download = self.check_bool_true(download)
        self.max_size = self.__check_max_size(max_size)
        self.chunk = self.__check_chunk(chunk)
        self.timeout = self.__check_timeout(timeout)
        self.max_retry = self.__check_max_retry(max_retry)
        self.max_pages = self.__check_max_pages(max_pages)
        self.run_command = self.__check_run_command(run_command)
        self.ffmpeg = self.__generate_ffmpeg_object(ffmpeg)
        self.live_qualities = self.__check_live_qualities(live_qualities)
        self.douyin_platform = self.check_bool_true(
            douyin_platform,
        )
        self.tiktok_platform = self.check_bool_true(
            tiktok_platform,
        )

        self.browser_info = self.merge_browser_info(
            browser_info,
            {},
        )
        self.browser_info_tiktok = self.merge_browser_info(
            browser_info_tiktok,
            {},
        )
        self.__set_browser_info(self.browser_info)
        self.__set_browser_info_tiktok(self.browser_info_tiktok)

        self.proxy: str | None = self.__check_proxy(
            proxy,
            remark=_("抖音"),
            enable=self.douyin_platform,
        )
        self.proxy_tiktok: str | None = self.__check_proxy_tiktok(proxy_tiktok)
        self.client = create_client(
            timeout=self.timeout,
            proxy=self.proxy,
        )
        self.client_tiktok = create_client(
            timeout=self.timeout,
            proxy=self.proxy_tiktok,
        )

        self.__generate_folders()

        # self.__URLS_PARAMS = {
        #     "accounts_urls": None,
        #     "accounts_urls_tiktok": None,
        #     "mix_urls": None,
        #     "mix_urls_tiktok": None,
        #     "owner_url": None,
        #     "owner_url_tiktok": None,
        # }
        self.__CHECK = {
            "root": self.__check_root,
            "folder_name": self.__check_folder_name,
            "name_format": self.__check_name_format,
            "date_format": self.__check_date_format,
            "split": self.__check_split,
            "folder_mode": self.check_bool_false,
            "music": self.check_bool_false,
            "truncate": self.__check_truncate,
            "storage_format": self.__check_storage_format,
            "dynamic_cover": self.check_bool_false,
            "static_cover": self.check_bool_false,
            "twc_tiktok": self.check_str,
            "download": self.check_bool_true,
            "max_size": self.__check_max_size,
            "chunk": self.__check_chunk,
            "timeout": self.__check_timeout,
            "max_retry": self.__check_max_retry,
            "max_pages": self.__check_max_pages,
            "run_command": self.__check_run_command,
            "ffmpeg": self.__generate_ffmpeg_object,
            "live_qualities": self.__check_live_qualities,
            "douyin_platform": self.check_bool_true,
            "tiktok_platform": self.check_bool_true,
        }
        # self.__BROWSER_INFO = {
        #     "browser_info": None,
        #     "browser_info_tiktok": None,
        # }

    @staticmethod
    def check_bool_false(
        value: bool,
    ) -> bool:
        return value if isinstance(value, bool) else False

    @staticmethod
    def check_bool_true(
        value: bool,
    ) -> bool:
        return value if isinstance(value, bool) else True

    def __check_cookie_tiktok(
        self,
        cookie: dict | str,
    ) -> tuple[dict, str]:
        # if isinstance(cookie, str):
        #     self.console.print(
        #         "参数 cookie_tiktok 应为字典格式！请修改配置文件后重新运行程序！",
        #         style=ERROR)
        return self.__check_cookie(cookie, name="cookie_tiktok")

    def __check_cookie(self, cookie: dict | str, name="cookie") -> tuple[dict, str]:
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

    def __add_cookie(
        self,
        parameters: tuple[dict, ...],
        cookie: dict | str,
    ) -> None | str:
        if isinstance(cookie, dict):
            for i in parameters:
                if i:
                    self.logger.info(
                        f"参数: {i}",
                        False,
                    )
                    cookie |= i
            return None
        elif isinstance(cookie, str):
            for i in parameters:
                if i:
                    self.logger.info(
                        f"参数: {i}",
                        False,
                    )
                    cookie += f"; {cookie_dict_to_str(i)}"
            return cookie
        raise DownloaderError

    async def __get_tt_wid_params(self) -> dict:
        if tt_wid := await TtWid.get_tt_wid(
            self.logger,
            self.headers_params,
            proxy=self.proxy,
        ):
            self.logger.info(f"抖音 {TtWid.NAME} 请求值: {tt_wid[TtWid.NAME]}", False)
            return tt_wid
        return {}

    async def __get_tt_wid_params_tiktok(self) -> dict:
        if tt_wid := await TtWidTikTok.get_tt_wid(
            self.logger,
            self.headers_params_tiktok,
            self.twc_tiktok
            or f"{TtWidTikTok.NAME}={
                self.cookie_dict_tiktok.get(TtWidTikTok.NAME, '')
                or self.get_cookie_value(
                    self.cookie_str_tiktok,
                    TtWidTikTok.NAME,
                )
            }",
            proxy=self.proxy_tiktok,
        ):
            self.logger.info(
                f"TikTok {TtWidTikTok.NAME} 请求值: {tt_wid[TtWidTikTok.NAME]}", False
            )
            return tt_wid
        return {}

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
                    return None
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
                return None
            except (
                RequestError,
                HTTPStatusError,
            ) as e:
                self.logger.warning(
                    _("{remark}代理 {proxy} 测试失败：{error}").format(
                        remark=remark, proxy=proxy, error=e
                    ),
                )
                return None
        return None

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
        if self.douyin_platform:
            if any(
                (
                    self.cookie_dict,
                    self.cookie_str,
                )
            ):
                self.console.info(
                    _("正在更新抖音参数，请稍等..."),
                )
                ms_token = await self.__get_token_params()
                tt_wid = await self.__get_tt_wid_params()
                API.params["msToken"] = ms_token.get(MsToken.NAME, "")
                await self.__update_cookie(
                    (
                        ms_token,
                        tt_wid,
                    ),
                    (
                        self.headers,
                        self.headers_download,
                    ),
                    self.cookie_dict,
                    self.cookie_str,
                )
                self.console.info(
                    _("抖音参数更新完毕！"),
                )
            else:
                self.logger.warning(
                    _("配置文件 cookie 参数未设置，抖音平台功能可能无法正常使用")
                )
        if self.tiktok_platform:
            if any(
                (
                    self.cookie_dict_tiktok,
                    self.cookie_str_tiktok,
                )
            ):
                self.console.info(
                    _("正在更新 TikTok 参数，请稍等..."),
                )
                ms_token = await self.__get_token_params_tiktok()
                tt_wid = await self.__get_tt_wid_params_tiktok()
                APITikTok.params["msToken"] = ms_token.get(MsTokenTikTok.NAME, "")
                await self.__update_cookie(
                    (
                        ms_token,
                        tt_wid,
                    ),
                    (
                        self.headers_tiktok,
                        self.headers_download_tiktok,
                    ),
                    self.cookie_dict_tiktok,
                    self.cookie_str_tiktok,
                )
                self.console.info(
                    _("TikTok 参数更新完毕！"),
                )
            else:
                self.logger.warning(
                    _(
                        "配置文件 cookie_tiktok 参数未设置，TikTok 平台功能可能无法正常使用"
                    )
                )

    async def update_params_offline(self) -> None:
        if self.douyin_platform:
            if any(
                (
                    self.cookie_dict,
                    self.cookie_str,
                )
            ):
                ms_token = self.cookie_dict.get(MsToken.NAME) or self.get_cookie_value(
                    self.cookie_str,
                    MsToken.NAME,
                )
                API.params["msToken"] = ms_token
                await self.__update_cookie(
                    ({MsToken.NAME: ms_token},),
                    (
                        self.headers,
                        self.headers_download,
                    ),
                    self.cookie_dict,
                    self.cookie_str,
                )
            else:
                self.logger.warning(
                    _("配置文件 cookie 参数未设置，抖音平台功能可能无法正常使用")
                )
        if self.tiktok_platform:
            if any(
                (
                    self.cookie_dict_tiktok,
                    self.cookie_str_tiktok,
                )
            ):
                ms_token = await self.__get_token_params_tiktok()
                APITikTok.params["msToken"] = ms_token.get(MsTokenTikTok.NAME, "")
                await self.__update_cookie(
                    (ms_token,),
                    (
                        self.headers_tiktok,
                        self.headers_download_tiktok,
                    ),
                    self.cookie_dict_tiktok,
                    self.cookie_str_tiktok,
                )
            else:
                self.logger.warning(
                    _(
                        "配置文件 cookie_tiktok 参数未设置，TikTok 平台功能可能无法正常使用"
                    )
                )

    async def __update_cookie(
        self,
        parameters: tuple[dict, ...],
        headers: tuple[dict, ...],
        cookie_dict: dict,
        cookie_str: str,
    ) -> None:
        cookie = self.__add_cookie(
            parameters,
            cookie_dict or cookie_str,
        )
        if not isinstance(cookie, str):
            cookie = cookie_dict_to_str(cookie_dict)
        for i in headers:
            i["Cookie"] = cookie

    def set_headers_cookie(
        self,
    ) -> None:
        if self.cookie_dict:
            cookie = cookie_dict_to_str(self.cookie_dict)
            self.headers["Cookie"] = cookie
            self.headers_download["Cookie"] = cookie
        elif self.cookie_str:
            self.headers["Cookie"] = self.cookie_str
            self.headers_download["Cookie"] = self.cookie_str
        if self.cookie_dict_tiktok:
            cookie = cookie_dict_to_str(self.cookie_dict_tiktok)
            self.headers_tiktok["Cookie"] = cookie
            self.headers_download_tiktok["Cookie"] = cookie
        elif self.cookie_str_tiktok:
            self.headers_tiktok["Cookie"] = self.cookie_str_tiktok
            self.headers_download_tiktok["Cookie"] = self.cookie_str_tiktok

    def set_download_headers(self) -> None:
        self.__update_download_headers()
        self.__update_download_headers_tiktok()

    def __update_download_headers(self) -> None:
        self.headers_download["Cookie"] = "dy_swidth=1536; dy_sheight=864"

    def __update_download_headers_tiktok(self) -> None:
        key = "tt_chain_token"
        if tk := self.cookie_dict_tiktok.get(
            key,
        ):
            self.headers_download_tiktok["Cookie"] = f"{key}={tk}"
        else:
            self.headers_download_tiktok["Cookie"] = self.cookie_str_tiktok
        # self.headers_download_tiktok["Cookie"] = self.headers_tiktok.get(
        #     "Cookie", "")

    async def __get_token_params(self) -> dict:
        # if not (
        #     m := (
        #         self.cookie_dict.get(MsToken.NAME)
        #         or self.get_cookie_value(
        #             self.cookie_str,
        #             MsToken.NAME,
        #         )
        #     )
        # ):
        #     self.logger.warning(
        #         _("抖音 cookie 缺少 {name} 键值对，请尝试重新写入 cookie").format(
        #             name=MsToken.NAME
        #         )
        #     )
        #     return {}
        if d := await MsToken.get_real_ms_token(
            self.logger,
            self.headers_params,
            # m,
            proxy=self.proxy,
        ):
            self.logger.info(
                f"抖音 MsToken 请求值: {d[MsToken.NAME]}",
                False,
            )
            return d
        else:
            ms_token = self.cookie_dict.get(MsToken.NAME) or self.get_cookie_value(
                self.cookie_str,
                MsToken.NAME,
            )
            self.logger.info(
                f"抖音 MsToken 本地值: {ms_token}",
                False,
            )
            return {MsToken.NAME: ms_token}

    async def __get_token_params_tiktok(self) -> dict:
        if not (
            m := (
                self.cookie_dict_tiktok.get(MsTokenTikTok.NAME)
                or self.get_cookie_value(
                    self.cookie_str_tiktok,
                    MsTokenTikTok.NAME,
                )
            )
        ):
            self.logger.warning(
                _("TikTok cookie 缺少 {name} 键值对，请尝试重新写入 cookie").format(
                    name=MsTokenTikTok.NAME
                )
            )
            return {}
        # if d := await MsTokenTikTok.get_long_ms_token(
        #     self.logger,
        #     self.headers_params_tiktok,
        #     m,
        #     proxy=self.proxy_tiktok,
        # ):
        #     self.logger.info(
        #         f"TikTok MsToken 请求值: {d[MsTokenTikTok.NAME]}",
        #         False,
        #     )
        #     return d
        # else:
        #     self.logger.info(
        #         f"TikTok MsToken 本地值: {m}",
        #         False,
        #     )
        #     return {MsTokenTikTok.NAME: m}
        return {MsTokenTikTok.NAME: m}

    def set_uif_id(
        self,
    ) -> None:
        if self.cookie_dict:
            API.params["uifid"] = self.cookie_dict.get("UIFID", "")
        elif self.cookie_str:
            API.params["uifid"] = self.get_cookie_value(
                self.cookie_str,
                "UIFID",
            )

    @staticmethod
    def __generate_ffmpeg_object(ffmpeg_path: str) -> FFMPEG:
        return FFMPEG(ffmpeg_path)

    def get_settings_data(self) -> dict:
        return {
            "accounts_urls": [vars(i) for i in self.accounts_urls],
            "accounts_urls_tiktok": [vars(i) for i in self.accounts_urls_tiktok],
            "mix_urls": [vars(i) for i in self.mix_urls],
            "mix_urls_tiktok": [vars(i) for i in self.mix_urls_tiktok],
            "owner_url": vars(self.owner_url),
            "owner_url_tiktok": self.owner_url_tiktok,
            "root": str(self.root.resolve()),
            "folder_name": self.folder_name,
            "name_format": " ".join(self.name_format),
            "date_format": self.date_format,
            "split": self.split,
            "folder_mode": self.folder_mode,
            "music": self.music,
            "truncate": self.truncate,
            "storage_format": self.storage_format,
            "cookie": self.cookie_str or self.cookie_dict,
            "cookie_tiktok": self.cookie_str_tiktok or self.cookie_dict_tiktok,
            "dynamic_cover": self.dynamic_cover,
            "static_cover": self.static_cover,
            "proxy": self.proxy,
            "proxy_tiktok": self.proxy_tiktok,
            "twc_tiktok": self.twc_tiktok,
            "download": self.download,
            "max_size": self.max_size,
            "chunk": self.chunk,
            "max_retry": self.max_retry,
            "max_pages": self.max_pages,
            "run_command": " ".join(self.run_command[::-1]),
            "ffmpeg": self.ffmpeg.path or "",
        }

    async def set_settings_data(
        self,
        data: dict,
    ) -> None:
        self.set_urls_params(
            data.pop("accounts_urls"),
            data.pop("mix_urls"),
            data.pop("owner_url"),
            data.pop("accounts_urls_tiktok"),
            data.pop("mix_urls_tiktok"),
            data.pop("owner_url_tiktok"),
        )
        self.set_cookie(
            data.pop(
                "cookie",
            ),
            data.pop(
                "cookie_tiktok",
            ),
        )
        self.set_browser_info(
            data.pop(
                "browser_info",
            ),
            data.pop(
                "browser_info_tiktok",
            ),
        )
        await self.set_proxy(
            data.pop(
                "proxy",
            ),
            data.pop(
                "proxy_tiktok",
            ),
        )
        self.set_general_params(data)

    async def __update_cookie_data(self, data: dict) -> None:
        for i, j in zip(("cookie", "cookie_tiktok"), (_("抖音"), "TikTok")):
            if c := data.get(i):
                setattr(
                    self, i, self.cookie_object.extract(c, False, key=i, platform=j)
                )
        await self.update_params()

    @staticmethod
    def check_urls_params(data: list[dict]) -> list[SimpleNamespace]:
        items = []
        for item in data:
            if not item.get("url") or not item.get("enable", True):
                continue
            if not isinstance(item.get("mark"), str):
                item["mark"] = ""
            items.append(item)
        return Extractor.generate_data_object(items)

    @staticmethod
    def check_url_params(data: dict) -> SimpleNamespace:
        if not data.get("url"):
            return SimpleNamespace(
                mark="",
                url="",
            )
        if not isinstance(data.get("mark"), str):
            data["mark"] = ""
        return Extractor.generate_data_object(data)

    def set_urls_params(
        self,
        accounts_urls: list[dict],
        mix_urls: list[dict],
        owner_url: dict,
        accounts_urls_tiktok: list[dict],
        mix_urls_tiktok: list[dict],
        owner_url_tiktok: dict,
    ):
        if accounts_urls:
            self.accounts_urls = self.check_urls_params(accounts_urls)
        if accounts_urls_tiktok:
            self.accounts_urls_tiktok = self.check_urls_params(accounts_urls_tiktok)
        if mix_urls:
            self.mix_urls = self.check_urls_params(mix_urls)
        if mix_urls_tiktok:
            self.mix_urls_tiktok = self.check_urls_params(mix_urls_tiktok)
        if owner_url:
            self.owner_url = self.check_url_params(owner_url)
        # if owner_url_tiktok:
        #     self.owner_url_tiktok = self.check_url_params(owner_url_tiktok)

    def set_cookie(
        self, cookie: str | dict[str, str], cookie_tiktok: str | dict[str, str]
    ):
        if cookie:
            self.cookie_dict, self.cookie_str = self.__check_cookie(cookie)
            self.cookie_state: bool = self.__check_cookie_state()
            self.set_uif_id()
        if cookie_tiktok:
            self.cookie_dict_tiktok, self.cookie_str_tiktok = (
                self.__check_cookie_tiktok(
                    cookie_tiktok,
                )
            )
            self.cookie_tiktok_state: bool = self.__check_cookie_state(True)
            self.__update_download_headers_tiktok()

    def set_general_params(self, data: dict[str, Any]) -> None:
        for i, j in data.items():
            if j is not None:
                self.__CHECK[i](j)

    async def set_proxy(self, proxy: str | None, proxy_tiktok: str | None):
        if isinstance(proxy, str):
            self.proxy: str | None = self.__check_proxy(
                proxy,
                remark=_("抖音"),
                enable=self.douyin_platform,
            )
        if isinstance(proxy_tiktok, str):
            self.proxy_tiktok: str | None = self.__check_proxy_tiktok(proxy_tiktok)
        await self.close_client()
        self.client = create_client(
            timeout=self.timeout,
            proxy=self.proxy,
        )
        self.client_tiktok = create_client(
            timeout=self.timeout,
            proxy=self.proxy_tiktok,
        )

    @staticmethod
    def merge_browser_info(
        browser_info: dict,
        new_info: dict,
    ) -> dict:
        return browser_info | new_info

    def set_browser_info(self, browser_info: dict, browser_info_tiktok: dict):
        self.browser_info = self.merge_browser_info(
            self.browser_info,
            browser_info or {},
        )
        self.browser_info_tiktok = self.merge_browser_info(
            self.browser_info_tiktok,
            browser_info_tiktok or {},
        )
        self.__set_browser_info(self.browser_info)
        self.__set_browser_info_tiktok(self.browser_info_tiktok)

    @staticmethod
    def check_str(value: str) -> str:
        return value if isinstance(value, str) else ""

    async def close_client(self) -> None:
        await self.client.aclose()
        await self.client_tiktok.aclose()

    def __generate_folders(self):
        self.compatible()
        self.cache.mkdir(exist_ok=True)

    def __set_browser_info(
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

    def __set_browser_info_tiktok(
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

    def __check_live_qualities(self, live_qualities: str) -> str:
        if isinstance(live_qualities, str):
            self.logger.info(f"live_qualities 参数已设置为 {live_qualities}", False)
            return live_qualities
        self.logger.warning(
            _("live_qualities 参数 {live_qualities} 设置错误").format(
                live_qualities=live_qualities
            ),
        )
        return ""

    def __check_cookie_state(self, tiktok=False) -> bool:
        if tiktok:
            return (self.cookie_object.STATE_KEY in self.cookie_dict_tiktok) or (
                self.cookie_object.STATE_KEY in self.cookie_str_tiktok
            )
        return (self.cookie_object.STATE_KEY in self.cookie_dict) or (
            self.cookie_object.STATE_KEY in self.cookie_str
        )

    @staticmethod
    def get_cookie_value(cookie_str: str, key: str, return_key=False) -> str:
        """
        解析cookie字符串并返回指定键的值或键值对

        :param cookie_str: cookie字符串（格式如 "name=John; age=30;"）
        :param key: 需要获取的键名
        :param return_key: 是否返回键值对格式，默认为False
        :return: 键值对字符串或值（若不存在返回None）
        """
        cookies = {}
        for pair in cookie_str.split(";"):
            pair = pair.strip()
            if not pair:
                continue
            # 分割键值（最多分割一次，应对含等号的值）
            key_value = pair.split("=", 1)
            if len(key_value) != 2:
                continue  # 跳过无效格式
            k, v = key_value[0].strip(), key_value[1].strip()
            cookies[k] = v

        value = cookies.get(key)
        if value is None:
            return ""

        return f"{key}={value}" if return_key else value

    def compatible(self):
        if (
            old := self.ROOT.parent.joinpath("Cache")
        ).exists() and not self.cache.exists():
            move(old, self.cache)
