from contextlib import suppress
from typing import TYPE_CHECKING
from asyncio import Event, create_task, gather, sleep, Queue, QueueEmpty
from .main_terminal import TikTok
from ..translation import _
from pyperclip import copy, paste

if TYPE_CHECKING:
    from ..config import Parameter
    from ..manager import Database

__all__ = ["ClipboardMonitor", "PostMonitor"]


class ClipboardMonitor(TikTok):
    def __init__(
        self,
        parameter: "Parameter",
        database: "Database",
        server_mode: bool = True,
    ):
        super().__init__(
            parameter,
            database,
            server_mode,
        )
        self.event_clipboard = Event()
        self.clipboard_cache = ""
        self.queue_dy = Queue()
        self.queue_tk = Queue()

    async def run(self, run_command: list):
        await self.start_listener()

    async def start_listener(
        self,
        delay: int | float = 1,
    ):
        self.console.info(
            _(
                "程序会自动检测并提取剪贴板中的抖音和 TikTok 作品链接，并自动下载作品文件；如需关闭，请按下 Ctrl+C，或将剪贴板内容设置为“close”以停止监听！"
            ),
        )
        copy("")
        self.event_clipboard.clear()
        await gather(
            self.check_clipboard(
                delay=delay,
            ),
            self.deal_tasks(
                delay=delay,
            ),
            self.deal_tasks_tiktok(
                delay=delay,
            ),
        )

    async def stop_listener(self):
        self.console.debug("停止监听剪贴板！")
        self.event_clipboard.set()

    async def check_clipboard(
        self,
        delay: int | float = 1,
    ):
        self.console.debug("开始监听剪贴板！")
        while not self.event_clipboard.is_set():
            if (c := paste()).lower() == "close":
                await self.stop_listener()
            elif c != self.clipboard_cache:
                self.clipboard_cache = c
                create_task(self.check_link(c))
            await sleep(delay)

    async def check_link(
        self,
        text: str,
    ):
        links = text.split()
        for i in links:
            if "douyin" in i:
                self.console.debug(f"处理抖音链接: {i}")
                await self.queue_dy.put(i)
            elif "tiktok" in i:
                self.console.debug(f"处理 TikTok 链接: {i}")
                await self.queue_tk.put(i)

    async def deal_tasks(
        self,
        delay: int | float = 1,
    ):
        await self._deal_tasks(
            self.parameter.douyin_platform,
            self.queue_dy,
            self.links,
            False,
            delay,
        )

    async def deal_tasks_tiktok(
        self,
        delay: int | float = 1,
    ):
        await self._deal_tasks(
            self.parameter.tiktok_platform,
            self.queue_tk,
            self.links_tiktok,
            True,
            delay,
        )

    async def _deal_tasks(
        self,
        enable: bool,
        queue: Queue,
        link_object,
        tiktok: bool,
        delay: int | float = 1,
    ):
        if not enable:
            return
        root, params, logger = self.record.run(self.parameter, blank=True)
        async with logger(root, console=self.console, **params) as record:
            while not self.event_clipboard.is_set() or queue.qsize() > 0:
                with suppress(QueueEmpty):
                    url = queue.get_nowait()
                    id_ = await link_object.run(url)
                    if not any(id_):
                        self.logger.warning(_("{url} 提取作品 ID 失败").format(url=url))
                    else:
                        await self._handle_detail(
                            id_,
                            tiktok,
                            record,
                        )
                await sleep(delay)


class PostMonitor(TikTok):
    def __init__(
        self,
        parameter: "Parameter",
        database: "Database",
        server_mode: bool = True,
    ):
        super().__init__(
            parameter,
            database,
            server_mode,
        )
