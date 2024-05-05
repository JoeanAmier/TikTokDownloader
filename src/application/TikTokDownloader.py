from asyncio import TimeoutError
from asyncio import run
from asyncio import sleep as asleep
from contextlib import suppress
from shutil import rmtree
from threading import Event
from threading import Thread
# from typing import Type
# from webbrowser import open
from time import sleep

# from typing import Type
# from webbrowser import open
from aiohttp import ClientError
# from flask import Flask
from flask import abort
from flask import request

from src.config import Parameter
from src.config import Settings
from src.custom import COOKIE_UPDATE_INTERVAL
from src.custom import (
    MASTER,
    WARNING,
    INFO,
    ERROR
)
from src.custom import (
    PROJECT_ROOT,
    VERSION_MAJOR,
    VERSION_MINOR,
    VERSION_BETA,
    RELEASES,
    REPOSITORY,
    LICENCE,
    DOCUMENTATION_URL,
    DISCLAIMER_TEXT,
    PROJECT_NAME,
)
# from src.custom import SERVER_HOST
# from src.custom import SERVER_PORT
from src.custom import TEXT_REPLACEMENT
from src.custom import verify_token
from src.encrypt import XBogus
from src.manager import Database
from src.manager import DownloadRecorder
from src.module import Cookie
from src.module import Register
from src.record import BaseLogger
from src.record import LoggerManager
from src.tools import Browser
from src.tools import ColorfulConsole
from src.tools import choose
from src.tools import safe_pop
# from .main_api_server import APIServer
from .main_complete import TikTok

# from .main_server import Server
# from .main_web_UI import WebUI

__all__ = ["TikTokDownloader"]


class TikTokDownloader:
    PLATFORM = (
        "cookie",
        "cookie_tiktok",
    )
    FUNCTION_OPTIONS = {
        1: "禁用",
        0: "启用",
    }
    NAME = PROJECT_NAME
    WIDTH = 50
    LINE = ">" * WIDTH

    def __init__(self, ):
        self.console = ColorfulConsole()
        self.logger = None
        self.recorder = None
        self.x_bogus = XBogus()
        self.settings = Settings(PROJECT_ROOT, self.console)
        self.event = Event()
        self.cookie = Cookie(self.settings, self.console)
        self.cookie_task = None
        self.parameter = None
        self.running = True
        self.default_mode = None
        self.database = Database()
        self.config = None
        self.__function_menu = None

    async def read_config(self):
        self.config = self.__format_config(await self.database.read_config_data())

    @staticmethod
    def __format_config(config: list) -> dict:
        return {i["NAME"]: i["VALUE"] for i in config}

    async def __aenter__(self):
        await self.database.__aenter__()
        await self.read_config()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.database.__aexit__(exc_type, exc_val, exc_tb)
        await self.parameter.close_session()
        self.close()

    def __update_menu(self):
        self.__function_menu = (
            ("复制粘贴写入 Cookie (抖音)", self.write_cookie),
            ("从浏览器获取 Cookie (抖音)", self.browser_cookie),
            ("扫码登录获取 Cookie (抖音)", self.auto_cookie),
            ("复制粘贴写入 Cookie (TikTok)", self.write_cookie_tiktok),
            ("从浏览器获取 Cookie (TikTok)", self.browser_cookie_tiktok),
            ("终端交互模式", self.complete),
            ("后台监测模式", self.temporary),
            ("Web API 模式", self.temporary),
            ("Web UI 模式", self.temporary),
            ("服务器部署模式", self.temporary),
            # ("Web API 模式", self.__api_object),
            # ("Web UI 模式", self.__web_ui_object),
            # ("服务器部署模式", self.__server_object),
            (f"{self.FUNCTION_OPTIONS[self.config["Update"]]
            }自动检查更新", self.__modify_update),
            (f"{self.FUNCTION_OPTIONS[self.config["Record"]]
            }作品下载记录", self.__modify_record),
            ("删除作品下载记录", self.delete_works_ids),
            (f"{self.FUNCTION_OPTIONS[self.config["Logger"]]
            }运行日志记录", self.__modify_logging),
        )

    async def temporary(self, *args, **kwargs, ):
        self.console.print("该功能暂不可用！", style=WARNING)

    # def __api_object(self):
    #     self.server(APIServer, SERVER_HOST)

    # def __web_ui_object(self):
    #     self.server(WebUI, token=False)

    # def __server_object(self):
    #     self.server(Server)

    async def __modify_update(self):
        await self.change_config("Update")

    async def __modify_record(self):
        await self.change_config("Record")

    async def __modify_logging(self):
        await self.change_config("Logger")

    async def disclaimer(self):
        if not self.config["Disclaimer"]:
            self.console.print(
                "\n".join(DISCLAIMER_TEXT),
                style=MASTER)
            if self.console.input(
                    "是否已仔细阅读上述免责声明(YES/NO): ").upper() != "YES":
                return False
            await self.database.update_config_data("Disclaimer", 1)
            self.console.print()
        return True

    def project_info(self):
        self.console.print(f"{self.LINE}\n\n\n{self.NAME.center(
            self.WIDTH)}\n\n\n{self.LINE}\n", style=MASTER)
        self.console.print(f"项目地址: {REPOSITORY}", style=MASTER)
        self.console.print(f"项目文档: {DOCUMENTATION_URL}", style=MASTER)
        self.console.print(f"开源许可: {LICENCE}\n", style=MASTER)

    def check_config(self):
        self.recorder = DownloadRecorder(
            self.database,
            self.config["Record"],
            self.console, )
        self.logger = {1: LoggerManager, 0: BaseLogger}[self.config["Logger"]]

    async def check_update(self):
        if not self.config["Update"]:
            return
        try:
            async with self.parameter.session.get(RELEASES, timeout=5) as response:
                latest_major, latest_minor = map(
                    int, str(response.url).split("/")[-1].split(".", 1))
                if latest_major > VERSION_MAJOR or latest_minor > VERSION_MINOR:
                    self.console.print(
                        f"检测到新版本: {latest_major}.{latest_minor}", style=WARNING)
                    self.console.print(RELEASES)
                elif latest_minor == VERSION_MINOR and VERSION_BETA:
                    self.console.print(
                        "当前版本为开发版, 可更新至正式版", style=WARNING)
                    self.console.print(RELEASES)
                elif VERSION_BETA:
                    self.console.print("当前已是最新开发版", style=WARNING)
                else:
                    self.console.print("当前已是最新正式版", style=INFO)
        except (ClientError, TimeoutError,):
            self.console.print("检测新版本失败", style=ERROR)
        self.console.print()

    async def main_menu(self, default_mode=""):
        """选择运行模式"""
        while self.running:
            self.__update_menu()
            if not default_mode:
                default_mode = choose(
                    "请选择 TikTokDownloader 运行模式",
                    [i for i, _ in self.__function_menu],
                    self.console,
                    separate=(
                        4,
                        9))
            await self.compatible(default_mode)
            default_mode = None

    # @start_cookie_task
    async def complete(self):
        """终端交互模式"""
        example = TikTok(self.parameter, self.database, )
        try:
            await example.run(self.default_mode)
            self.running = example.running
        except KeyboardInterrupt:
            self.running = False

    # @start_cookie_task
    # def server(
    #         self,
    #         server: Type[APIServer | WebUI | Server],
    #         host="0.0.0.0",
    #         token=True):
    #     """
    #     服务器模式
    #     """
    #     self.console.print(
    #         "如果您看到 WARNING: This is a development server. 提示，这并不是异常错误！\n如需关闭服务器，可以在终端按下 Ctrl + C 快捷键！",
    #         style=INFO)
    #     master = server(self.parameter)
    #     app = master.run_server(Flask("__main__"))
    #     register(self.recorder.close)
    #     if token:
    #         app.before_request(self.verify_token)
    #     open(f"http://127.0.0.1:{SERVER_PORT}")
    #     app.run(host=host, port=SERVER_PORT)

    @staticmethod
    def verify_token():
        if request.method == "POST" and not verify_token(
                request.json.get("token")):
            return abort(403)

    async def change_config(self, key: str, ):
        self.config[key] = 0 if self.config[key] else 1
        await self.database.update_config_data(key, self.config[key])
        self.console.print("修改设置成功！")
        self.check_config()
        await self.check_settings()

    async def write_cookie(self):
        await self.__write_cookie()

    async def write_cookie_tiktok(self):
        await self.__write_cookie(1)

    async def __write_cookie(self, index=0):
        self.console.print(
            "Cookie 获取教程：https://github.com/JoeanAmier/TikTokDownloader/blob/master/docs/Cookie%E8%8E%B7%E5%8F%96%E6"
            "%95%99%E7%A8%8B.md")
        if self.cookie.run(self.PLATFORM[index]):
            await self.check_settings()
            # await self.parameter.update_cookie()

    async def auto_cookie(self):
        self.console.print(
            "该功能为实验性功能，仅适用于学习和研究目的；目前仅支持抖音平台，建议使用其他方式获取 Cookie，未来可能会禁用或移除该功能！",
            style=ERROR)
        if self.console.input("是否返回上一级菜单(YES/NO)").upper() != "NO":
            return
        if cookie := await Register(
                self.parameter,
                self.settings,
        ).run():
            self.cookie.extract(cookie)
            await self.check_settings()
            # await self.parameter.update_cookie()
        else:
            self.console.print("扫码登录失败，未写入 Cookie！", style=WARNING)

    async def compatible(self, mode: str):
        with suppress(ValueError):
            if mode in {"Q", "q", ""}:
                self.running = False
            elif (n := int(mode) - 1) in range(len(self.__function_menu)):
                await self.__function_menu[n][1]()

    async def delete_works_ids(self):
        if not self.config["Record"]:
            self.console.print("作品下载记录功能已禁用！", style=WARNING)
            return
        self.recorder.delete_ids(self.console.input("请输入需要删除的作品 ID："))
        self.console.print("删除作品下载记录成功！", style=INFO)

    async def check_settings(self, restart=True):
        if restart:
            await self.parameter.close_session()
        self.parameter = Parameter(
            self.settings,
            self.cookie,
            logger=self.logger,
            xb=self.x_bogus,
            console=self.console,
            **self.settings.read(),
            recorder=self.recorder,
        )
        await self.parameter.check_proxy()
        self.restart_cycle_task(restart, )
        await asleep(5)
        if not restart:
            self.default_mode = self.parameter.default_mode.copy()
        self.parameter.cleaner.set_rule(TEXT_REPLACEMENT, True)

    async def run(self):
        self.project_info()
        self.console.print(
            "注意：本项目正在重构代码，功能尚不稳定，不适合日常使用！\n",
            style=ERROR,
        )  # 正式发布后移除该提示
        self.check_config()
        await self.check_settings(False, )
        await self.check_update()
        if await self.disclaimer():
            await self.main_menu(safe_pop(self.default_mode))

    def delete_temp(self):
        rmtree(self.parameter.temp.resolve())

    def periodic_update_cookie(self):
        async def inner():
            while not self.event.is_set():
                await self.parameter.update_cookie()
                self.event.wait(COOKIE_UPDATE_INTERVAL)

        with suppress(RuntimeError):
            run(inner())

    def restart_cycle_task(self, restart=True, ):
        if restart:
            self.event.set()
            while self.cookie_task.is_alive():
                sleep(1)
        self.cookie_task = Thread(target=self.periodic_update_cookie)
        self.event.clear()
        self.cookie_task.start()

    def close(self):
        self.event.set()
        self.delete_temp()
        self.parameter.logger.info("程序即将关闭")

    async def browser_cookie(self, ):
        if Browser(self.parameter, self.cookie).run():
            await self.check_settings()

    async def browser_cookie_tiktok(self, ):
        if Browser(self.parameter, self.cookie).run(True):
            await self.check_settings()
