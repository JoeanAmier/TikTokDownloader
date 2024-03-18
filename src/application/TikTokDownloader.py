from atexit import register
from contextlib import suppress
from pathlib import Path
from shutil import rmtree
from threading import Event
from threading import Thread
from typing import Type
from webbrowser import open

from flask import Flask
from flask import abort
from flask import request
from requests import exceptions
from requests import get

from src.config import Parameter
from src.config import Settings
from src.custom import BACKUP_RECORD_INTERVAL
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
from src.custom import SERVER_HOST
from src.custom import SERVER_PORT
from src.custom import TEXT_REPLACEMENT
from src.custom import verify_token
from src.encrypt import XBogus
from src.manager import DownloadRecorder
from src.module import Cookie
from src.module import Register
from src.record import BaseLogger
from src.record import LoggerManager
from src.tools import Browser
from src.tools import ColorfulConsole
from src.tools import FileSwitch
from src.tools import choose
from src.tools import safe_pop
from .main_api_server import APIServer
from .main_complete import TikTok
from .main_server import Server
from .main_web_UI import WebUI

__all__ = ["TikTokDownloader"]


def start_cookie_task(function):
    def inner(self, *args, **kwargs):
        if not self.cookie_task.is_alive():
            self.cookie_task.start()
        if isinstance(
                self.backup_task,
                Thread) and not self.backup_task.is_alive():
            self.backup_task.start()
        return function(self, *args, **kwargs)

    return inner


class TikTokDownloader:
    REDUCED = (1, 1, 1, 1, 0, 1, 0, 0, 1, 1)  # 禁用项目部分功能
    # REDUCED = False  # 启用项目全部功能

    PLATFORM = {
        "1": "cookie",
        "2": "cookie_tiktok",
    }

    NAME = PROJECT_NAME
    WIDTH = 50
    LINE = ">" * WIDTH

    UPDATE = {
        "path": PROJECT_ROOT.joinpath("./src/config/Disable_Update"),
        "tip": "",
    }
    RECORD = {
        "path": PROJECT_ROOT.joinpath("./src/config/Disable_Record"),
        "tip": "",
    }
    LOGGING = {
        "path": PROJECT_ROOT.joinpath("./src/config/Enable_Logging"),
        "tip": "",
    }
    DISCLAIMER = {"path": PROJECT_ROOT.joinpath(
        "./src/config/Consent_Disclaimer")}

    FUNCTION_OPTIONS = {
        True: "禁用",
        False: "启用",
    }

    def __init__(self, **kwargs):
        self.console = ColorfulConsole()
        self.logger = None
        self.blacklist = None
        self.x_bogus = XBogus()
        self.settings = Settings(PROJECT_ROOT, self.console)
        self.cookie = Cookie(self.settings, self.console)
        self.parameter = None
        self.running = True
        self.default_mode = None
        self.event = Event()
        self.cookie_task = Thread(target=self.periodic_update_cookie)
        self.backup_task = None
        self.__abnormal = None
        self.__function = None

    @property
    def abnormal(self):
        return self.__abnormal

    @abnormal.setter
    def abnormal(self, value: bool):
        if not isinstance(self.__abnormal, bool):
            self.__abnormal = value

    def __update_menu(self):
        self.__function = (
            ("复制粘贴写入 Cookie", self.write_cookie),
            ("从浏览器获取 Cookie", self.browser_cookie),
            ("扫码登录获取 Cookie", self.auto_cookie),
            ("终端交互模式", self.complete),
            ("后台监测模式", lambda: self.console.print("敬请期待！")),
            ("Web API 模式", self.__api_object),
            ("Web UI 模式", self.__web_ui_object),
            ("服务器部署模式", self.__server_object),
            (f"{self.UPDATE['tip']}自动检查更新", self.__modify_update),
            (f"{self.RECORD['tip']}作品下载记录", self.__modify_recode),
            ("删除指定下载记录", self.delete_works_ids),
            (f"{self.LOGGING['tip']}运行日志记录", self.__modify_logging),
        )

    def __api_object(self):
        self.server(APIServer, SERVER_HOST)

    def __web_ui_object(self):
        self.server(WebUI, token=False)

    def __server_object(self):
        self.server(Server)

    def __modify_update(self):
        self.change_config(self.UPDATE["path"])

    def __modify_recode(self):
        self.change_config(self.RECORD["path"])

    def __modify_logging(self):
        self.change_config(self.LOGGING["path"])

    def disclaimer(self):
        if not self.DISCLAIMER["path"].exists():
            self.console.print(
                "\n".join(DISCLAIMER_TEXT),
                style=MASTER)
            if self.console.input(
                    "是否已仔细阅读上述免责声明(YES/NO): ").upper() != "YES":
                return False
            FileSwitch.deal_config(self.DISCLAIMER["path"])
            self.console.print()
        return True

    def version(self):
        self.console.print(f"{self.LINE}\n\n\n{self.NAME.center(
            self.WIDTH)}\n\n\n{self.LINE}\n", style=MASTER)
        self.console.print(f"项目地址: {REPOSITORY}", style=MASTER)
        self.console.print(f"项目文档: {DOCUMENTATION_URL}", style=MASTER)
        self.console.print(f"开源许可: {LICENCE}\n", style=MASTER)

    def check_config(self):
        folder = ("./src", "./src/config", "./cache", "./cache/temp")
        self.abnormal = PROJECT_ROOT.joinpath(folder[-1]).exists()
        for i in folder:
            PROJECT_ROOT.joinpath(i).mkdir(exist_ok=True)
        self.UPDATE["tip"] = self.FUNCTION_OPTIONS[not self.UPDATE["path"].exists()]
        self.RECORD["tip"] = self.FUNCTION_OPTIONS[not (
            b := self.RECORD["path"].exists())]
        self.LOGGING["tip"] = self.FUNCTION_OPTIONS[(
            l := self.LOGGING["path"].exists())]
        self.blacklist = DownloadRecorder(
            not b,
            PROJECT_ROOT.joinpath("./cache"),
            not self.abnormal,
            self.console)
        self.backup_task = Thread(
            target=self.periodic_backup_record,
        )
        self.logger = {True: LoggerManager, False: BaseLogger}[l]

    def check_update(self):
        if self.UPDATE["path"].exists():
            return
        try:
            response = get(RELEASES, timeout=5)
            latest_major, latest_minor = map(
                int, response.url.split("/")[-1].split(".", 1))
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
        except (exceptions.ReadTimeout, exceptions.ConnectionError):
            self.console.print("检测新版本失败", style=ERROR)
        self.console.print()

    def main_menu(self, default_mode=""):
        """选择运行模式"""
        while self.running:
            self.__update_menu()
            if not default_mode:
                default_mode = choose(
                    "请选择 TikTokDownloader 运行模式",
                    [i for i, _ in self.__function],
                    self.console,
                    separate=(
                        2,
                        7))
            self.compatible(default_mode)
            default_mode = None

    @start_cookie_task
    def complete(self):
        """终端交互模式"""
        example = TikTok(self.parameter, self.REDUCED)
        register(self.blacklist.close)
        try:
            example.run(self.default_mode)
            self.running = example.running
        except KeyboardInterrupt:
            self.running = False

    @start_cookie_task
    def server(
            self,
            server: Type[APIServer | WebUI | Server],
            host="0.0.0.0",
            token=True):
        """
        服务器模式
        """
        self.console.print(
            "如果您看到 WARNING: This is a development server. 提示，这并不是异常错误！\n如需关闭服务器，可以在终端按下 Ctrl + C 快捷键！",
            style=INFO)
        master = server(self.parameter)
        app = master.run_server(Flask("__main__"))
        register(self.blacklist.close)
        if token:
            app.before_request(self.verify_token)
        open(f"http://127.0.0.1:{SERVER_PORT}")
        app.run(host=host, port=SERVER_PORT)

    @staticmethod
    def verify_token():
        if request.method == "POST" and not verify_token(
                request.json.get("token")):
            return abort(403)

    def change_config(self, file: Path):
        FileSwitch.deal_config(file)
        self.console.print("修改设置成功！")
        if self.blacklist:
            self.blacklist.close()
        self.check_config()
        self.check_settings()

    def write_cookie(self):
        self.console.print(
            "Cookie 获取教程：https://github.com/JoeanAmier/TikTokDownloader/blob/master/docs/Cookie%E8%8E%B7%E5%8F%96%E6"
            "%95%99%E7%A8%8B.md")
        if (p := self.__select_platform()) in self.PLATFORM:
            self.cookie.run(self.PLATFORM[p])
            self.check_settings()
            self.parameter.update_cookie()

    def auto_cookie(self):
        self.console.print(
            "警告：该功能可能会导致抖音账号被风控，建议使用其他方式获取 Cookie！",
            style=ERROR)
        self.console.print("该功能仅支持抖音平台，未来可能会禁用该功能！", style=WARNING)
        if cookie := Register(
                self.settings,
                self.console,
                self.x_bogus,
        ).run(self.parameter.temp):
            self.cookie.extract(cookie)
            self.check_settings()
            self.parameter.update_cookie()
        else:
            self.console.print("扫码登录失败，未写入 Cookie！", style=WARNING)

    def compatible(self, mode: str):
        with suppress(ValueError):
            if mode in {"Q", "q", ""}:
                self.running = False
            elif (n := int(mode) - 1) in range(len(self.__function)):
                self.__function[n][1]()

    def delete_works_ids(self):
        if self.RECORD["tip"] == "启用":
            self.console.print("作品下载记录功能已禁用！", style=WARNING)
            return
        self.blacklist.delete_ids(self.console.input("请输入需要删除的作品 ID："))
        self.console.print("删除作品下载记录成功！", style=INFO)

    def check_settings(self):
        self.parameter = Parameter(
            self.settings,
            self.cookie,
            main_path=PROJECT_ROOT,
            logger=self.logger,
            xb=self.x_bogus,
            console=self.console,
            **self.settings.read(),
            blacklist=self.blacklist,
            reduced=bool(self.REDUCED),
        )
        self.default_mode = self.parameter.default_mode.copy()
        self.parameter.cleaner.set_rule(TEXT_REPLACEMENT, True)

    def run(self):
        self.check_config()
        self.version()
        self.check_update()
        self.check_settings()
        if self.disclaimer():
            self.main_menu(safe_pop(self.default_mode))
        self.close()

    def delete_temp(self):
        rmtree(self.parameter.temp.resolve())

    def periodic_update_cookie(self):
        while not self.event.is_set():
            self.parameter.update_cookie()
            self.event.wait(COOKIE_UPDATE_INTERVAL)

    def periodic_backup_record(self):
        while not self.event.is_set():
            self.blacklist.backup_file()
            self.event.wait(BACKUP_RECORD_INTERVAL)
        self.blacklist.backup_file()

    def close(self):
        self.delete_temp()
        self.event.set()
        self.blacklist.close()
        self.parameter.logger.info("程序结束运行")

    def browser_cookie(self):
        if (p := self.__select_platform()) in self.PLATFORM:
            Browser(self.parameter, self.cookie).run(p == "2")

    def __select_platform(self) -> str:
        return choose(
            "请选择平台：",
            (
                "抖音平台",
                "TikTok 平台",
            ),
            self.console,
        )
