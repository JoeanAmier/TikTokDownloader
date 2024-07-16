from asyncio import Semaphore
from asyncio import gather
from datetime import datetime
from pathlib import Path
from shutil import move
from time import time
from types import SimpleNamespace
from typing import TYPE_CHECKING

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

from src.custom import DESCRIPTION_LENGTH
from src.custom import MAX_WORKERS
from src.custom import (
    PROGRESS,
    INFO,
    WARNING,
)
from src.tools import PrivateRetry
from src.tools import format_size
from src.tools import trim_string

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["Downloader"]


class Downloader:
    semaphore = Semaphore(MAX_WORKERS)

    def __init__(self, params: "Parameter"):
        self.cleaner = params.CLEANER
        self.client = params.client
        self.client_tiktok = params.client_tiktok
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
        self.dynamic = params.dynamic_cover
        self.original = params.original_cover
        # self.cookie = params.cookie
        # self.cookie_tiktok = params.cookie_tiktok
        self.proxy = params.proxy_str
        self.proxy_tiktok = params.proxy_str_tiktok
        self.download = params.download
        self.max_size = params.max_size
        self.chunk = params.chunk
        self.max_retry = params.max_retry
        self.recorder = params.recorder
        self.timeout = params.timeout
        self.ffmpeg = params.ffmpeg
        self.cache = params.cache
        self.truncate = params.truncate

    def __general_progress_object(self):
        """文件下载进度条"""
        return Progress(
            TextColumn(
                "[progress.description]{task.description}",
                style=PROGRESS,
                justify="left"),
            SpinnerColumn(),
            BarColumn(
                bar_width=20),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(
                binary_units=True),
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
                justify="left"),
            SpinnerColumn(),
            BarColumn(
                bar_width=20),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeElapsedColumn(),
            console=self.console,
            transient=True,
            expand=True,
        )

    async def run(self,
                  data: list[dict],
                  type_: str,
                  tiktok=False,
                  **kwargs, ) -> None:
        if not self.download or not data:
            return
        if type_ == "batch":
            self.log.info("Bắt đầu tải xuống các tập tin") #开始下载作品文件
            await self.run_batch(data, tiktok, **kwargs)
        elif type_ == "detail":
            await self.run_general(data, tiktok, )
        else:
            raise ValueError

    async def run_batch(
            self,
            data: list[dict],
            tiktok: bool,
            id_: str,
            name: str,
            mark="",
            addition="xuất bản video", #发布作品
            mid: str = None,
            title: str = None,
    ):
        # assert addition in {"喜欢作品", "收藏作品", "发布作品", "合集作品"}, ValueError
        mix = addition == "Bộ sưu tập videos" #合集作品
        root = self.storage_folder(
            mid if mix else id_,
            title if mix else name,
            not mix,
            mark,
            addition,
            mix)
        await self.batch_processing(data, root, tiktok=tiktok, )

    async def run_general(self, data: list[dict], tiktok: bool):
        root = self.storage_folder()
        await self.batch_processing(data, root, tiktok=tiktok, )

    async def run_live(self, data: list[tuple], tiktok=False, ):
        if not data or not self.download:
            return
        download_tasks = []
        download_command = []
        self.generate_live_tasks(data, download_tasks, download_command)
        if self.ffmpeg.state:
            self.console.print(
                "检测到 ffmpeg，程序将会调用 ffmpeg 下载直播，关闭 TikTokDownloader 不会中断下载！",
                style=INFO,
            )
            self.__download_live(download_command, tiktok)
        else:
            self.console.print(
                "未检测到 ffmpeg，程序将会调用内置下载器下载直播，您需要保持 TikTokDownloader 运行直到直播结束！",
                style=WARNING,
            )
            await self.downloader_chart(
                download_tasks,
                SimpleNamespace(),
                self.__live_progress_object(),
                semaphore=Semaphore(len(download_tasks)),
                unknown_size=True,
                headers=self.headers,
                tiktok=tiktok,
            )

    def generate_live_tasks(
            self, data: list[tuple], tasks: list, commands: list):
        for i, f, m in data:
            name = self.cleaner.filter_name(
                f'{
                i["title"]}{
                self.split}{
                i["nickname"]}{
                self.split}{
                datetime.now():%Y-%m-%d %H.%M.%S}.flv',
                inquire=False,
                default=str(
                    time())[
                        :10])
            temp_root, actual_root = self.deal_folder_path(
                self.storage_folder(folder_name="Live"), name, True)
            tasks.append((
                f,
                temp_root,
                actual_root,
                f'直播 {i["title"]}{self.split}{i["nickname"]}',
                "0" * 19,
            ))
            commands.append((
                m,
                str(actual_root.with_name(f"{actual_root.stem}.mp4").resolve()),
            ))

    def __download_live(self, commands: list, tiktok: bool, ):
        self.ffmpeg.download(
            commands,
            self.proxy_tiktok if tiktok else self.proxy,
            self.timeout,
            self.headers["User-Agent"],
        )

    async def batch_processing(
            self,
            data: list[dict],
            root: Path,
            **kwargs):
        count = SimpleNamespace(
            downloaded_image=set(),
            skipped_image=set(),
            downloaded_video=set(),
            skipped_video=set()
        )
        tasks = []
        for item in data:
            item["desc"] = item["desc"][:DESCRIPTION_LENGTH]
            name = self.generate_detail_name(item)
            temp_root, actual_root = self.deal_folder_path(root, name)
            params = {
                "tasks": tasks,
                "name": name,
                "id_": item["id"],
                "item": item,
                "count": count,
                "temp_root": temp_root,
                "actual_root": actual_root
            }
            if (t := item["type"]) == "图集":
                await self.download_image(**params)
            elif t == "视频":
                await self.download_video(**params)
            self.download_music(**params)
            self.download_cover(**params)
        await self.downloader_chart(
            tasks,
            count,
            self.__general_progress_object(),
            **kwargs)
        self.statistics_count(count)

    async def downloader_chart(
            self,
            tasks: list[tuple],
            count: SimpleNamespace,
            progress: Progress,
            semaphore: Semaphore = None,
            **kwargs):
        with progress:
            tasks = [self.request_file(
                *task,
                count=count,
                **kwargs,
                progress=progress,
                semaphore=semaphore, ) for task in tasks]
            await gather(*tasks)

    def deal_folder_path(self, root: Path, name: str,
                         pass_=False) -> tuple[Path, Path]:
        root = self.create_detail_folder(root, name, pass_)
        root.mkdir(exist_ok=True)
        cache = self.cache.joinpath(name)
        actual = root.joinpath(name)
        return cache, actual

    async def is_downloaded(self, id_: str) -> bool:
        return await self.recorder.has_ids(id_)

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
            count: SimpleNamespace,
            temp_root: Path,
            actual_root: Path) -> None:
        for index, img in enumerate(
                item["downloads"].split(" "), start=1):
            if await self.is_downloaded(id_):
                count.skipped_image.add(id_)
                self.log.info(f"【图集】{name} 存在下载记录，跳过下载")
                count.skipped_image.add(id_)
                break
            elif self.is_exists(p := actual_root.with_name(f"{name}_{index}.jpeg")):
                self.log.info(f"【图集】{name}_{index} 文件已存在，跳过下载")
                self.log.info(f"文件路径: {p.resolve()}", False)
                count.skipped_image.add(id_)
                continue
            tasks.append((
                img,
                temp_root.with_name(
                    f"{name}_{index}.jpeg"),
                p,
                f"【图集】{name}_{index}",
                id_,
            ))

    async def download_video(
            self,
            tasks: list,
            name: str,
            id_: str,
            item: SimpleNamespace,
            count: SimpleNamespace,
            temp_root: Path,
            actual_root: Path) -> None:
        if await self.is_skip(
                id_, p := actual_root.with_name(
                    f"{name}.mp4")):
            self.log.info(f"【video】{name} đã được download hoặc file đã tồn tại, bỏ qua việc tải xuống") # 【视频】存在下载记录或文件已存在，跳过下载
            self.log.info(f"đường dẫn tập tin: {p.resolve()}", False) #文件路径
            count.skipped_video.add(id_)
            return
        tasks.append((
            item["downloads"],
            temp_root.with_name(f"{name}.mp4"),
            p,
            f"【视频】{name}",
            id_,
        ))

    def download_music(
            self,
            tasks: list,
            name: str,
            id_: str,
            item: SimpleNamespace,
            temp_root: Path,
            actual_root: Path,
            **kwargs, ) -> None:
        if self.check_deal_music(
                url := item["music_url"],
                p := actual_root.with_name(f"{name}.mp3"), ):
            tasks.append((
                url,
                temp_root.with_name(f"{name}.mp3"),
                p,
                f"【音乐】{name}",
                id_,
            ))

    def download_cover(
            self,
            tasks: list,
            name: str,
            id_: str,
            item: SimpleNamespace,
            temp_root: Path,
            actual_root: Path,
            **kwargs, ) -> None:
        if all((self.original,
                url := item["origin_cover"],
                not self.is_exists(p := actual_root.with_name(f"{name}.jpeg"))
                )):
            tasks.append((
                url,
                temp_root.with_name(f"{name}.jpeg"),
                p,
                f"【封面】{name}",
                id_,
            ))
        if all((self.dynamic,
                url := item["dynamic_cover"],
                not self.is_exists(p := actual_root.with_name(f"{name}.webp"))
                )):
            tasks.append((
                url,
                temp_root.with_name(f"{name}.webp"),
                p,
                f"【动图】{name}",
                id_,
            ))

    def check_deal_music(self, url: str, path: Path) -> bool:
        return all((self.music, url, not self.is_exists(path)))

    @PrivateRetry.retry
    async def request_file(
            self,
            url: str,
            temp: Path,
            actual: Path,
            show: str,
            id_: str,
            count: SimpleNamespace,
            progress: Progress,
            headers: dict = None,
            tiktok=False,
            unknown_size=False,
            semaphore: Semaphore = None,
    ) -> bool:
        async with semaphore or self.semaphore:
            client = self.client_tiktok if tiktok else self.client
            headers = self.__adapter_headers(headers, tiktok, )
            self.log.info(f"{show} URL: {url}", False, )
            self.log.info(f"{show} Headers: {headers}", False, )
            try:
                async with client.stream(
                        "GET",
                        url,
                        headers=headers, ) as response:
                    self.log.info(
                        f"{show} Response URL: {response.url}", False)
                    self.log.info(
                        f"{show} Response Code: {response.status_code}", False)
                    self.log.info(
                        f"{show} Response Headers: {response.headers}", False)
                    if not (
                            content := int(
                                response.headers.get(
                                    'content-length',
                                    0))) and not unknown_size:  # 响应内容大小判断
                        self.log.warning(f"{show} Nội dung phản hồi rỗng") #响应内容为空
                        return False
                    response.raise_for_status()
                    # if response.status_code >= 400:  # 响应码判断
                    #     self.log.warning(
                    #         f"{response.url} 响应码异常: {response.status_code}")
                    #     return False
                    self.log.info(
                        f"{show} Kích thước tập tin {format_size(content)}", False, ) #文件大小
                    if all(
                            (self.max_size, content, content > self.max_size)):  # 文件下载跳过判断
                        self.log.info(f"{show} Kích thước tập tin vượt quá giới hạn, download bị bỏ qua") #文件大小超出限制，跳过下载
                        return True
                    return await self.download_file(
                        temp,
                        actual,
                        show,
                        id_,
                        response,
                        content,
                        count,
                        progress)
            except RequestError as e:
                self.log.warning(f"网络异常: {e}")
                return False

    async def download_file(
            self,
            cache: Path,
            actual: Path,
            show: str,
            id_: str,
            response,
            content: int,
            count: SimpleNamespace,
            progress: Progress) -> bool:
        task_id = progress.add_task(
            trim_string(show, self.truncate), total=content or None)
        try:
            with cache.open("wb") as f:
                async for chunk in response.aiter_bytes(self.chunk):
                    f.write(chunk)
                    progress.update(task_id, advance=len(chunk))
                progress.remove_task(task_id)
        except (
                RequestError,
                StreamError,
        ) as e:
            self.log.warning(f"{show} download bị gián đoạn, thông báo lỗi:{e}") #下载中断，错误信息：
            self.delete_file(cache)
            await self.recorder.delete_id(id_)
            return False
        self.save_file(cache, actual)
        self.log.info(f"{show} download file thành công") #文件下载成功
        self.log.info(f"Đường dẫn tập tin {actual.resolve()}", False) #文件路径
        await self.recorder.update_id(id_)
        self.add_count(show, id_, count)
        return True

    def __adapter_headers(
            self,
            headers: dict,
            tiktok: bool,
            *args,
            **kwargs, ) -> dict:
        return headers or (self.headers_tiktok if tiktok else self.headers)

    @staticmethod
    def add_count(type_: str, id_: str, count: SimpleNamespace):
        if type_.startswith("【图集】"):
            count.downloaded_image.add(id_)
        elif type_.startswith("【视频】"):
            count.downloaded_video.add(id_)

    def storage_folder(
            self,
            id_: str = None,
            name: str = None,
            batch=False,
            mark: str = None,
            addition: str = None,
            mix=False,
            folder_name: str = None) -> Path:
        if batch and all((id_, name, addition)):
            folder_name = f"UID{id_}_{mark or name}_{addition}"
        elif mix and all((id_, name, addition)):
            folder_name = f"MIX{id_}_{mark or name}_{addition}"
        else:
            folder_name = folder_name or self.folder_name
        folder = self.root.joinpath(folder_name)
        folder.mkdir(exist_ok=True)
        return folder

    def generate_detail_name(self, data: dict) -> str:
        return self.cleaner.filter_name(
            self.split.join(
                data[i] for i in self.name_format), inquire=False, default=str(
                time())[:10])

    def create_detail_folder(
            self,
            root: Path,
            name: str,
            pass_=False) -> Path:
        if pass_:
            return root
        return root.joinpath(name) if self.folder_mode else root

    @staticmethod
    def save_file(cache: Path, actual: Path):
        move(cache.resolve(), actual.resolve())

    def delete_file(self, path: Path):
        path.unlink()
        self.log.info(f"{path.name} đã bị xóa") # 文件已删除

    def statistics_count(self, count: SimpleNamespace):
        self.log.info(f"Bỏ qua video {len(count.skipped_video)} links") # 跳过视频作品
        self.log.info(f"Bỏ qua thư viện {len(count.skipped_image)} links") # 跳过图集作品
        self.log.info(f"Tải xuống video {len(count.downloaded_video)} links") # 下载视频作品
        self.log.info(f"Tải xuống album {len(count.downloaded_image)} links") # 下载图集作品

    def __format_item_name(self, name: str) -> str:
        pass
