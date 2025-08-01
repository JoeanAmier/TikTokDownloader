from asyncio import Semaphore
from asyncio import gather
from datetime import datetime
from pathlib import Path
from shutil import move
from time import time
from types import SimpleNamespace
from typing import TYPE_CHECKING
from typing import Union
from typing import Callable
from aiofiles import open
from httpx import HTTPStatusError
from httpx import RequestError
from httpx import StreamError
from rich.progress import (
    SpinnerColumn,
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

from ..custom import DESCRIPTION_LENGTH
from ..custom import MAX_FILENAME_LENGTH
from ..custom import MAX_WORKERS
from ..custom import (
    PROGRESS,
)
from ..tools import CacheError
from ..tools import Retry
from ..tools import DownloaderError
from ..tools import beautify_string
from ..tools import format_size
from ..tools import FakeProgress
from ..translation import _

if TYPE_CHECKING:
    from ..config import Parameter
    from httpx import AsyncClient

__all__ = ["Downloader"]


class Downloader:
    semaphore = Semaphore(MAX_WORKERS)
    CONTENT_TYPE_MAP = {
        "image/png": "png",
        "image/jpeg": "jpeg",
        "image/webp": "webp",
        "video/mp4": "mp4",
        "video/quicktime": "mov",
        "audio/mp4": "m4a",
        "audio/mpeg": "mp3",
    }

    def __init__(
        self,
        params: "Parameter",
        server_mode: bool = False,
    ):
        self.cleaner = params.CLEANER
        self.client: "AsyncClient" = params.client
        self.client_tiktok: "AsyncClient" = params.client_tiktok
        self.headers = params.headers_download
        self.headers_tiktok = params.headers_download_tiktok
        self.log = params.logger
        self.xb = params.xb
        self.console = params.console
        self.root = params.root
        self.folder_name = params.folder_name
        self.name_format = params.name_format
        self.split = params.split
        self.folder_mode = params.folder_mode
        self.music = params.music
        self.dynamic_cover = params.dynamic_cover
        self.static_cover = params.static_cover
        # self.cookie = params.cookie
        # self.cookie_tiktok = params.cookie_tiktok
        self.proxy = params.proxy
        self.proxy_tiktok = params.proxy_tiktok
        self.download = params.download
        self.max_size = params.max_size
        self.chunk = params.chunk
        self.max_retry = params.max_retry
        self.recorder = params.recorder
        self.timeout = params.timeout
        self.ffmpeg = params.ffmpeg
        self.cache = params.cache
        self.truncate = params.truncate
        self.general_progress_object: Callable = self.init_general_progress(
            server_mode,
        )

    def init_general_progress(
        self,
        server_mode: bool = False,
    ) -> Callable:
        if server_mode:
            return self.__fake_progress_object
        return self.__general_progress_object

    @staticmethod
    def __fake_progress_object(
        *args,
        **kwargs,
    ):
        return FakeProgress()

    def __general_progress_object(self):
        """文件下载进度条"""
        return Progress(
            TextColumn(
                "[progress.description]{task.description}",
                style=PROGRESS,
                justify="left",
            ),
            SpinnerColumn(),
            BarColumn(bar_width=20),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(binary_units=True),
            "•",
            TimeRemainingColumn(),
            console=self.console,
            transient=True,
            expand=True,
        )

    def __live_progress_object(self):
        """直播下载进度条"""
        return Progress(
            TextColumn(
                "[progress.description]{task.description}",
                style=PROGRESS,
                justify="left",
            ),
            SpinnerColumn(),
            BarColumn(bar_width=20),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeElapsedColumn(),
            console=self.console,
            transient=True,
            expand=True,
        )

    async def run(
        self,
        data: Union[list[dict], list[tuple]],
        type_: str,
        tiktok=False,
        **kwargs,
    ) -> None:
        if not self.download or not data:
            return
        self.log.info(_("开始下载作品文件"))
        match type_:
            case "batch":
                await self.run_batch(data, tiktok, **kwargs)
            case "detail":
                await self.run_general(data, tiktok, **kwargs)
            case "music":
                await self.run_music(data, **kwargs)
            case "live":
                await self.run_live(data, tiktok, **kwargs)
            case _:
                raise ValueError

    async def run_batch(
        self,
        data: list[dict],
        tiktok: bool,
        mode: str = "",
        mark: str = "",
        user_id: str = "",
        user_name: str = "",
        mix_id: str = "",
        mix_title: str = "",
        collect_id: str = "",
        collect_name: str = "",
    ):
        root = self.storage_folder(
            mode,
            *self.data_classification(
                mode,
                mark,
                user_id,
                user_name,
                mix_id,
                mix_title,
                collect_id,
                collect_name,
            ),
        )
        await self.batch_processing(
            data,
            root,
            tiktok=tiktok,
        )

    async def run_general(self, data: list[dict], tiktok: bool, **kwargs):
        root = self.storage_folder(mode="detail")
        await self.batch_processing(
            data,
            root,
            tiktok=tiktok,
        )

    async def run_music(
        self,
        data: list[dict],
        **kwargs,
    ):
        root = self.root.joinpath("Music")
        tasks = []
        for i in data:
            name = self.generate_music_name(i)
            temp_root, actual_root = self.deal_folder_path(
                root,
                name,
                False,
            )
            self.download_music(
                tasks,
                name,
                i["id"],
                i,
                temp_root,
                actual_root,
                "download",
                True,
                type_=_("音乐"),
            )
        await self.downloader_chart(
            tasks, SimpleNamespace(), self.general_progress_object(), **kwargs
        )

    async def run_live(
        self,
        data: list[tuple],
        tiktok=False,
        **kwargs,
    ):
        if not data or not self.download:
            return
        download_command = []
        self.generate_live_commands(
            data,
            download_command,
        )
        self.console.info(
            _("程序将会调用 ffmpeg 下载直播，关闭 DouK-Downloader 不会中断下载！"),
        )
        self.__download_live(download_command, tiktok)

    def generate_live_commands(
        self,
        data: list[tuple],
        commands: list,
        suffix: str = "mp4",
    ):
        root = self.root.joinpath("Live")
        root.mkdir(exist_ok=True)
        for i, f, m in data:
            name = self.cleaner.filter_name(
                f"{i['title']}{self.split}{i['nickname']}{self.split}{datetime.now():%Y-%m-%d %H.%M.%S}.{suffix}",
                f"{int(time())}{self.split}{datetime.now():%Y-%m-%d %H.%M.%S}.{suffix}",
            )
            path = root.joinpath(name)
            commands.append(
                (
                    m,
                    str(path.resolve()),
                )
            )

    def __download_live(
        self,
        commands: list,
        tiktok: bool,
    ):
        self.ffmpeg.download(
            commands,
            self.proxy_tiktok if tiktok else self.proxy,
            self.headers["User-Agent"],
        )

    async def batch_processing(self, data: list[dict], root: Path, **kwargs):
        count = SimpleNamespace(
            downloaded_image=set(),
            skipped_image=set(),
            downloaded_video=set(),
            skipped_video=set(),
            downloaded_live=set(),
            skipped_live=set(),
        )
        tasks = []
        for item in data:
            item["desc"] = beautify_string(item["desc"], DESCRIPTION_LENGTH)
            name = self.generate_detail_name(item)
            temp_root, actual_root = self.deal_folder_path(
                root,
                name,
                self.folder_mode,
            )
            params = {
                "tasks": tasks,
                "name": name,
                "id_": item["id"],
                "item": item,
                "temp_root": temp_root,
                "actual_root": actual_root,
            }
            if (t := item["type"]) == _("图集"):
                await self.download_image(
                    **params,
                    type_=_("图集"),
                    skipped=count.skipped_image,
                )
            elif t == _("视频"):
                await self.download_video(
                    **params,
                    type_=_("视频"),
                    skipped=count.skipped_video,
                )
            elif t == _("实况"):
                await self.download_image(
                    suffix="mp4",
                    type_=_("实况"),
                    **params,
                    skipped=count.skipped_live,
                )
            else:
                raise DownloaderError
            self.download_music(
                **params,
                type=_("音乐"),
            )
            self.download_cover(**params)
        await self.downloader_chart(
            tasks, count, self.general_progress_object(), **kwargs
        )
        self.statistics_count(count)

    async def downloader_chart(
        self,
        tasks: list[tuple],
        count: SimpleNamespace,
        progress: Progress,
        semaphore: Semaphore = None,
        **kwargs,
    ):
        with progress:
            tasks = [
                self.request_file(
                    *task,
                    count=count,
                    **kwargs,
                    progress=progress,
                    semaphore=semaphore,
                )
                for task in tasks
            ]
            await gather(*tasks)

    def deal_folder_path(
        self,
        root: Path,
        name: str,
        folder_mode=False,
    ) -> tuple[Path, Path]:
        """生成文件的临时路径和目标路径"""
        root = self.create_detail_folder(root, name, folder_mode)
        root.mkdir(exist_ok=True)
        cache = self.cache.joinpath(name)
        actual = root.joinpath(name)
        return cache, actual

    async def is_downloaded(self, id_: str) -> bool:
        return await self.recorder.has_id(id_)

    @staticmethod
    def is_exists(path: Path) -> bool:
        return path.exists()

    async def is_skip(self, id_: str, path: Path) -> bool:
        return await self.is_downloaded(id_) or self.is_exists(path)

    async def download_image(
        self,
        tasks: list,
        name: str,
        id_: str,
        item: SimpleNamespace,
        skipped: set,
        temp_root: Path,
        actual_root: Path,
        suffix: str = "jpeg",
        type_: str = _("图集"),
    ) -> None:
        if not item["downloads"]:
            self.log.error(
                _("【{type}】{name} 提取文件下载地址失败，跳过下载").format(
                    type=type_, name=name
                )
            )
            return
        for index, img in enumerate(
            item["downloads"],
            start=1,
        ):
            if await self.is_downloaded(id_):
                skipped.add(id_)
                self.log.info(
                    _("【{type}】{name} 存在下载记录，跳过下载").format(
                        type=type_, name=name
                    )
                )
                break
            elif self.is_exists(p := actual_root.with_name(f"{name}_{index}.{suffix}")):
                self.log.info(
                    _("【{type}】{name}_{index} 文件已存在，跳过下载").format(
                        type=type_, name=name, index=index
                    )
                )
                self.log.info(f"文件路径: {p.resolve()}", False)
                skipped.add(id_)
                continue
            tasks.append(
                (
                    img,
                    temp_root.with_name(f"{name}_{index}.{suffix}"),
                    p,
                    f"【{type_}】{name}_{index}",
                    id_,
                    suffix,
                )
            )

    async def download_video(
        self,
        tasks: list,
        name: str,
        id_: str,
        item: SimpleNamespace,
        skipped: set,
        temp_root: Path,
        actual_root: Path,
        suffix: str = "mp4",
        type_: str = _("视频"),
    ) -> None:
        if not item["downloads"]:
            self.log.error(
                _("【{type}】{name} 提取文件下载地址失败，跳过下载").format(
                    type=type_, name=name
                )
            )
            return
        if await self.is_skip(
            id_,
            p := actual_root.with_name(
                f"{name}.{suffix}",
            ),
        ):
            self.log.info(
                _("【{type}】{name} 存在下载记录或文件已存在，跳过下载").format(
                    type=type_, name=name
                )
            )
            self.log.info(f"文件路径: {p.resolve()}", False)
            skipped.add(id_)
            return
        tasks.append(
            (
                item["downloads"],
                temp_root.with_name(f"{name}.{suffix}"),
                p,
                f"【{type_}】{name}",
                id_,
                suffix,
            )
        )

    def download_music(
        self,
        tasks: list,
        name: str,
        id_: str,
        item: dict,
        temp_root: Path,
        actual_root: Path,
        key: str = "music_url",
        switch: bool = False,
        suffix: str = "mp3",
        type_: str = _("音乐"),
        **kwargs,
    ) -> None:
        if self.check_deal_music(
            url := item[key],
            p := actual_root.with_name(f"{name}.{suffix}"),
            switch,
        ):
            tasks.append(
                (
                    url,
                    temp_root.with_name(f"{name}.{suffix}"),
                    p,
                    _("【{type}】{name}").format(
                        type=type_,
                        name=name,
                    ),
                    id_,
                    suffix,
                )
            )

    def download_cover(
        self,
        tasks: list,
        name: str,
        id_: str,
        item: SimpleNamespace,
        temp_root: Path,
        actual_root: Path,
        static_suffix: str = "jpeg",
        dynamic_suffix: str = "webp",
        **kwargs,
    ) -> None:
        if all(
            (
                self.static_cover,
                url := item["static_cover"],
                not self.is_exists(
                    p := actual_root.with_name(f"{name}.{static_suffix}")
                ),
            )
        ):
            tasks.append(
                (
                    url,
                    temp_root.with_name(f"{name}.{static_suffix}"),
                    p,
                    f"【封面】{name}",
                    id_,
                    static_suffix,
                )
            )
        if all(
            (
                self.dynamic_cover,
                url := item["dynamic_cover"],
                not self.is_exists(
                    p := actual_root.with_name(f"{name}.{dynamic_suffix}")
                ),
            )
        ):
            tasks.append(
                (
                    url,
                    temp_root.with_name(f"{name}.{dynamic_suffix}"),
                    p,
                    f"【动图】{name}",
                    id_,
                    dynamic_suffix,
                )
            )

    def check_deal_music(
        self,
        url: str,
        path: Path,
        switch=False,
    ) -> bool:
        """未传入 switch 参数则判断音乐下载开关设置"""
        return all((switch or self.music, url, not self.is_exists(path)))

    @Retry.retry
    async def request_file(
        self,
        url: str,
        temp: Path,
        actual: Path,
        show: str,
        id_: str,
        suffix: str,
        count: SimpleNamespace,
        progress: Progress,
        headers: dict = None,
        tiktok=False,
        unknown_size=False,
        semaphore: Semaphore = None,
    ) -> bool | None:
        async with semaphore or self.semaphore:
            client = self.client_tiktok if tiktok else self.client
            headers = self.__adapter_headers(
                headers,
                tiktok,
            )
            self.__record_request_messages(
                show,
                url,
                headers,
            )
            try:
                # length, suffix = await self.__head_file(client, url, headers, suffix, )
                position = self.__update_headers_range(
                    headers,
                    temp,
                )
                async with client.stream(
                    "GET",
                    url,
                    headers=headers,
                ) as response:
                    if response.status_code == 416:
                        raise CacheError(_("文件缓存异常，尝试重新下载"))
                    response.raise_for_status()
                    length, suffix = self._extract_content(
                        response.headers,
                        suffix,
                    )
                    length += position
                    self._record_response(
                        response,
                        show,
                        length,
                    )
                    match self._download_initial_check(
                        length,
                        unknown_size,
                        show,
                    ):
                        case 1:
                            return await self.download_file(
                                temp,
                                actual.with_suffix(
                                    f".{suffix}",
                                ),
                                show,
                                id_,
                                response,
                                length,
                                position,
                                count,
                                progress,
                            )
                        case 0:
                            return True
                        case -1:
                            return False
                        case _:
                            raise DownloaderError
            except RequestError as e:
                self.log.warning(_("网络异常: {error_repr}").format(error_repr=repr(e)))
                return False
            except HTTPStatusError as e:
                self.log.warning(
                    _("响应码异常: {error_repr}").format(error_repr=repr(e))
                )
                self.console.warning(
                    _(
                        "如果 TikTok 平台作品下载功能异常，请检查配置文件中 browser_info_tiktok 的 device_id 参数！"
                    ),
                )
                return False
            except CacheError as e:
                self.delete(temp)
                self.log.error(str(e))
                return False
            except Exception as e:
                self.log.error(
                    _(
                        "下载文件时发生预期之外的错误，请向作者反馈，错误信息: {error}"
                    ).format(error=repr(e)),
                )
                self.log.error(f"URL: {url}", False)
                self.log.error(f"Headers: {headers}", False)
                return False

    async def download_file(
        self,
        cache: Path,
        actual: Path,
        show: str,
        id_: str,
        response,
        content: int,
        position: int,
        count: SimpleNamespace,
        progress: Progress,
    ) -> bool:
        task_id = progress.add_task(
            beautify_string(show, self.truncate),
            total=content or None,
            completed=position,
        )
        try:
            async with open(cache, "ab") as f:
                async for chunk in response.aiter_bytes(self.chunk):
                    await f.write(chunk)
                    progress.update(task_id, advance=len(chunk))
                progress.remove_task(task_id)
        except (
            RequestError,
            StreamError,
        ) as e:
            progress.remove_task(task_id)
            self.log.warning(
                _("{show} 下载中断，错误信息：{error}").format(show=show, error=e)
            )
            # self.delete_file(cache)
            await self.recorder.delete_id(id_)
            return False
        self.save_file(cache, actual)
        self.log.info(_("{show} 文件下载成功").format(show=show))
        self.log.info(f"文件路径 {actual.resolve()}", False)
        await self.recorder.update_id(id_)
        self.add_count(show, id_, count)
        return True

    def __record_request_messages(
        self,
        show: str,
        url: str,
        headers: dict,
    ):
        self.log.info(f"{show} URL: {url}", False)
        # 请求头脱敏处理，不记录 Cookie
        desensitize = {k: v for k, v in headers.items() if k != "Cookie"}
        self.log.info(f"{show} Headers: {desensitize}", False)

    def __adapter_headers(
        self,
        headers: dict,
        tiktok: bool,
        *args,
        **kwargs,
    ) -> dict:
        return (headers or self.headers_tiktok if tiktok else self.headers).copy()

    @staticmethod
    def add_count(show: str, id_: str, count: SimpleNamespace):
        if show.startswith(f"【{_('图集')}】"):
            count.downloaded_image.add(id_)
        elif show.startswith(f"【{_('视频')}】"):
            count.downloaded_video.add(id_)
        elif show.startswith(f"【{_('实况')}】"):
            count.downloaded_live.add(id_)

    @staticmethod
    def data_classification(
        mode: str = "",
        mark: str = "",
        user_id: str = "",
        user_name: str = "",
        mix_id: str = "",
        mix_title: str = "",
        collect_id: str = "",
        collect_name: str = "",
    ) -> tuple[str, str]:
        match mode:
            case "post" | "favorite" | "collection":
                return user_id, mark or user_name
            case "mix":
                return mix_id, mark or mix_title
            case "collects":
                return collect_id, mark or collect_name
            case _:
                raise DownloaderError

    def storage_folder(
        self,
        mode: str = "",
        id_: str = "",
        name: str = "",
    ) -> Path:
        match mode:
            case "post":
                folder_name = _("UID{id_}_{name}_发布作品").format(id_=id_, name=name)
            case "favorite":
                folder_name = _("UID{id_}_{name}_喜欢作品").format(id_=id_, name=name)
            case "mix":
                folder_name = _("MID{id_}_{name}_合集作品").format(id_=id_, name=name)
            case "collection":
                folder_name = _("UID{id_}_{name}_收藏作品").format(id_=id_, name=name)
            case "collects":
                folder_name = _("CID{id_}_{name}_收藏夹作品").format(id_=id_, name=name)
            case "detail":
                folder_name = self.folder_name
            case _:
                raise DownloaderError
        folder = self.root.joinpath(folder_name)
        folder.mkdir(exist_ok=True)
        return folder

    def generate_detail_name(self, data: dict) -> str:
        """生成作品文件名称"""
        return beautify_string(
            self.cleaner.filter_name(
                self.split.join(data[i] for i in self.name_format),
                data["id"],
            ),
            length=MAX_FILENAME_LENGTH,
        )

    def generate_music_name(self, data: dict) -> str:
        """生成音乐文件名称"""
        return beautify_string(
            self.cleaner.filter_name(
                self.split.join(
                    data[i]
                    for i in (
                        "author",
                        "title",
                        "id",
                    )
                ),
                default=str(time())[:10],
            ),
            length=MAX_FILENAME_LENGTH,
        )

    @staticmethod
    def create_detail_folder(
        root: Path,
        name: str,
        folder_mode=False,
    ) -> Path:
        return root.joinpath(name) if folder_mode else root

    @staticmethod
    def delete(
        temp: "Path",
    ):
        if temp.is_file():
            temp.unlink()

    @staticmethod
    def save_file(cache: Path, actual: Path):
        move(cache.resolve(), actual.resolve())

    def delete_file(self, path: Path):
        path.unlink()
        self.log.info(_("{file_name} 文件已删除").format(file_name=path.name))

    def statistics_count(self, count: SimpleNamespace):
        self.log.info(
            _("下载视频作品 {downloaded_video_count} 个").format(
                downloaded_video_count=len(count.downloaded_video)
            ),
        )
        self.log.info(
            _("跳过视频作品 {skipped_count} 个").format(
                skipped_count=len(count.skipped_video)
            )
        )
        self.log.info(
            _("下载图集作品 {downloaded_image_count} 个").format(
                downloaded_image_count=len(count.downloaded_image)
            ),
        )
        self.log.info(
            _("跳过图集作品 {skipped_count} 个").format(
                skipped_count=len(count.skipped_image)
            )
        )
        self.log.info(
            _("下载实况作品 {downloaded_image_count} 个").format(
                downloaded_image_count=len(count.downloaded_live)
            ),
        )
        self.log.info(
            _("跳过实况作品 {skipped_count} 个").format(
                skipped_count=len(count.skipped_live)
            )
        )

    def _record_response(
        self,
        response,
        show: str,
        length: int,
    ):
        self.log.info(f"{show} Response URL: {response.url}", False)
        self.log.info(f"{show} Response Code: {response.status_code}", False)
        self.log.info(f"{show} Response Headers: {response.headers}", False)
        self.log.info(
            f"{show} 文件大小 {format_size(length)}",
            False,
        )

    async def __head_file(
        self,
        client: "AsyncClient",
        url: str,
        headers: dict,
        suffix: str,
    ) -> tuple[int, str]:
        response = await client.head(
            url,
            headers=headers,
        )
        if response.status_code == 405:
            return 0, suffix
        response.raise_for_status()
        return self._extract_content(
            response.headers,
            suffix,
        )

    def _extract_content(
        self,
        headers: dict,
        suffix: str,
    ) -> tuple[int, str]:
        suffix = (
            self.__extract_type(
                headers.get("Content-Type"),
            )
            or suffix
        )
        length = headers.get(
            "Content-Length",
            0,
        )
        return int(length), suffix

    @staticmethod
    def __get_resume_byte_position(file: Path) -> int:
        return file.stat().st_size if file.is_file() else 0

    def __update_headers_range(
        self,
        headers: dict,
        file: Path,
        length: int = 0,
    ) -> int:
        position = self.__get_resume_byte_position(file)
        # if length and position >= length:
        #     self.delete(file)
        #     position = 0
        headers["Range"] = f"bytes={position}-"
        return position

    def __extract_type(self, content: str) -> str:
        if not (s := self.CONTENT_TYPE_MAP.get(content)):
            return self.__unknown_type(content)
        return s

    def __unknown_type(self, content: str) -> str:
        self.log.warning(_("未收录的文件类型：{content}").format(content=content))
        return ""

    def _download_initial_check(
        self,
        length: int,
        unknown_size: bool,
        show: str,
    ) -> int:
        if not length and not unknown_size:  # 响应内容大小判断
            self.log.warning(_("{show} 响应内容为空").format(show=show))
            return -1  # 执行重试
        if all(
            (
                self.max_size,
                length,
                length > self.max_size,
            )
        ):  # 文件下载跳过判断
            self.log.info(_("{show} 文件大小超出限制，跳过下载").format(show=show))
            return 0  # 跳过下载
        return 1  # 继续下载
