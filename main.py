from atexit import register
from pathlib import Path
from shutil import rmtree
from threading import Event
from threading import Thread
from webbrowser import open

from flask import Flask
from flask import abort
from flask import request
from requests import exceptions
from requests import get
from rich.console import Console

from src.Configuration import Parameter
from src.Configuration import Settings
from src.CookieTool import Cookie
from src.CookieTool import Register
from src.FileManager import DownloadRecorder
from src.FileManager import FileManager
from src.Parameter import Headers
from src.Parameter import XBogus
from src.Recorder import BaseLogger
from src.Recorder import LoggerManager
from src.custom import BACKUP_RECORD_INTERVAL
from src.custom import COOKIE_UPDATE_INTERVAL
from src.custom import (
    MASTER,
    WARNING,
    PROMPT,
    INFO,
    ERROR,
    GENERAL
)
from src.custom import SERVER_HOST
from src.custom import SERVER_PORT
from src.custom import TEXT_REPLACEMENT
from src.custom import verify_token
from src.main_api_server import APIServer
from src.main_complete import TikTok
from src.main_complete import prompt
from src.main_server import Server
from src.main_web_UI import WebUI

__all__ = []


class ColorfulConsole(Console):
    def print(self, *args, style=GENERAL, highlight=False, **kwargs):
        super().print(*args, style=style, highlight=highlight, **kwargs)

    def input(self, prompt_="", *args, **kwargs):
        return super().input(
            f"[{PROMPT}]{prompt_}[/{PROMPT}]", *args, **kwargs)


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
    PROJECT_ROOT = Path(__file__).resolve().parent
    VERSION_MAJOR = 5
    VERSION_MINOR = 3
    VERSION_BETA = True

    REPOSITORY = "https://github.com/JoeanAmier/TikTokDownloader"
    LICENCE = "GNU General Public License v3.0"
    DOCUMENTATION_URL = "https://github.com/JoeanAmier/TikTokDownloader/wiki/Documentation"
    RELEASES = "https://github.com/JoeanAmier/TikTokDownloader/releases/latest"
    NAME = f"TikTokDownloader v{VERSION_MAJOR}.{
    VERSION_MINOR}{" Beta" if VERSION_BETA else ""}"
    WIDTH = 50
    LINE = ">" * WIDTH

    UPDATE = {"path": PROJECT_ROOT.joinpath("./src/config/Disable_Update")}
    RECORD = {"path": PROJECT_ROOT.joinpath("./src/config/Disable_Record")}
    LOGGING = {"path": PROJECT_ROOT.joinpath("./src/config/Enable_Logging")}
    DISCLAIMER = {"path": PROJECT_ROOT.joinpath(
        "./src/config/Consent_Disclaimer")}

    DISCLAIMER_TEXT = (
        "关于 TikTokDownloader 的 免责声明：",
        "",
        "1. 使用者对本项目的使用由使用者自行决定，并自行承担风险。作者对使用者使用本项目所产生的任何损失、责任、或风险概不负责。",
        "2. 本项目的作者提供的代码和功能是基于现有知识和技术的开发成果。作者尽力确保代码的正确性和安全性，但不保证代码完全没有错误或缺陷。",
        "3. 使用者在使用本项目时必须严格遵守 GNU General Public License v3.0 的要求，并在适当的地方注明使用了 GNU General Public License v3.0 的代码。",
        "4. 使用者在任何情况下均不得将本项目的作者、贡献者或其他相关方与使用者的使用行为联系起来，或要求其对使用者使用本项目所产生的任何损失或损害负责。",
        "5. 使用者在使用本项目的代码和功能时，必须自行研究相关法律法规，并确保其使用行为合法合规。任何因违反法律法规而导致的法律责任和风险，均由使用者自行承担。",
        "6. 本项目的作者不会提供 TikTokDownloader 项目的付费版本，也不会提供与 TikTokDownloader 项目相关的任何商业服务。",
        "7. 基于本项目进行的任何二次开发、修改或编译的程序与原创作者无关，原创作者不承担与二次开发行为或其结果相关的任何责任，使用者应自行对因"
        "二次开发可能带来的各种情况负全部责任。",
        "",
        "在使用本项目的代码和功能之前，请您认真考虑并接受以上免责声明。如果您对上述声明有任何疑问或不同意，请不要使用本项目的代码和功能。如果"
        "您使用了本项目的代码和功能，则视为您已完全理解并接受上述免责声明，并自愿承担使用本项目的一切风险和后果。",
        "",
    )

    def __init__(self):
        self.console = ColorfulConsole()
        self.logger = None
        self.blacklist = None
        self.user_agent, self.ua_code = Headers.generate_user_agent()
        self.x_bogus = XBogus()
        self.settings = Settings(self.PROJECT_ROOT, self.console)
        self.cookie = Cookie(self.settings, self.console)
        self.register = Register(
            self.settings,
            self.console,
            self.x_bogus,
            self.user_agent,
            self.ua_code)
        self.parameter = None
        self.running = True
        self.event = Event()
        self.cookie_task = Thread(target=self.periodic_update_cookie)
        self.backup_task = None
        self._abnormal = None

    @property
    def abnormal(self):
        return self._abnormal

    @abnormal.setter
    def abnormal(self, value: bool):
        if not isinstance(self._abnormal, bool):
            self._abnormal = value

    def disclaimer(self):
        if not self.DISCLAIMER["path"].exists():
            self.console.print(
                "\n".join(
                    self.DISCLAIMER_TEXT),
                style=MASTER)
            if self.console.input(
                    "是否已仔细阅读上述免责声明(YES/NO): ").upper() != "YES":
                return False
            FileManager.deal_config(self.DISCLAIMER["path"])
            self.console.print()
        return True

    def version(self):
        self.console.print(f"{self.LINE}\n\n\n{self.NAME.center(
            self.WIDTH)}\n\n\n{self.LINE}\n", style=MASTER)
        self.console.print(f"项目地址: {self.REPOSITORY}", style=MASTER)
        self.console.print(f"项目文档: {self.DOCUMENTATION_URL}", style=MASTER)
        self.console.print(f"开源许可: {self.LICENCE}\n", style=MASTER)

    def check_config(self):
        folder = ("./src", "./src/config", "./cache", "./cache/temp")
        self.abnormal = self.PROJECT_ROOT.joinpath(folder[-1]).exists()
        for i in folder:
            self.PROJECT_ROOT.joinpath(i).mkdir(exist_ok=True)
        self.UPDATE["tip"] = "启用" if self.UPDATE["path"].exists() else "禁用"
        self.RECORD["tip"] = "启用" if (
            b := self.RECORD["path"].exists()) else "禁用"
        self.LOGGING["tip"] = "禁用" if (
            l := self.LOGGING["path"].exists()) else "启用"
        self.blacklist = DownloadRecorder(
            not b, self.PROJECT_ROOT.joinpath("./cache"), not self.abnormal)
        self.backup_task = Thread(
            target=self.periodic_backup_record,
        )
        self.logger = {True: LoggerManager, False: BaseLogger}[l]

    def check_update(self):
        if self.UPDATE["path"].exists():
            return
        try:
            response = get(self.RELEASES, timeout=5)
            latest_major, latest_minor = map(
                int, response.url.split("/")[-1].split(".", 1))
            if latest_major > self.VERSION_MAJOR or latest_minor > self.VERSION_MINOR:
                self.console.print(
                    f"检测到新版本: {latest_major}.{latest_minor}", style=WARNING)
                self.console.print(self.RELEASES)
            elif latest_minor == self.VERSION_MINOR and self.VERSION_BETA:
                self.console.print(
                    "当前版本为开发版, 可更新至正式版", style=WARNING)
                self.console.print(self.RELEASES)
            elif self.VERSION_BETA:
                self.console.print("当前已是最新开发版", style=WARNING)
            else:
                self.console.print("当前已是最新正式版", style=INFO)
        except (exceptions.ReadTimeout, exceptions.ConnectionError):
            self.console.print("检测新版本失败", style=ERROR)
        self.console.print()

    def main_menu(self, default_mode="0"):
        """选择运行模式"""
        while self.running:
            if default_mode not in {"3", "4", "5", "6"}:
                default_mode = prompt(
                    "请选择 TikTokDownloader 运行模式",
                    ("复制粘贴写入 Cookie",
                     "扫码登录写入 Cookie",
                     "终端命令行模式",
                     "Web API 接口模式",
                     "Web UI 交互模式",
                     "服务器部署模式",
                     f"{self.UPDATE['tip']}自动检查更新",
                     f"{self.RECORD['tip']}作品下载记录",
                     f"{self.LOGGING['tip']}运行日志记录",),
                    self.console,
                    separate=(
                        1,
                        5))
            self.compatible(default_mode)
            default_mode = "0"

    @start_cookie_task
    def complete(self):
        """终端命令行模式"""
        example = TikTok(self.parameter)
        register(self.blacklist.close)
        try:
            example.run()
            self.running = example.running
        except KeyboardInterrupt:
            self.running = False

    @start_cookie_task
    def server(
            self,
            server: APIServer | WebUI | Server,
            host="0.0.0.0",
            token=True):
        """
        服务器模式
        """
        self.console.print(
            "如果您看到 WARNING: This is a development server. 提示，这并不是异常错误！\n如需关闭服务器，可以在终端按下 Ctrl + C 快捷键！",
            style=INFO)
        master = server(self.parameter)
        app = master.run_server(Flask(__name__))
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
        FileManager.deal_config(file)
        self.console.print("修改设置成功！")
        if self.blacklist:
            self.blacklist.close()
        self.check_config()
        self.check_settings()

    def write_cookie(self):
        self.cookie.run()
        self.check_settings()
        self.parameter.update_cookie()

    def auto_cookie(self):
        if cookie := self.register.run(self.parameter.temp):
            self.cookie.extract(cookie, False)
            self.check_settings()
            self.parameter.update_cookie()
        else:
            self.console.print("扫码登录失败，未写入 Cookie！", style=WARNING)

    def compatible(self, mode: str):
        if mode in {"Q", "q", ""}:
            self.running = False
        elif mode == "1":
            self.write_cookie()
        elif mode == "2":
            self.auto_cookie()
        elif mode == "3":
            self.complete()
        elif mode == "4":
            self.server(APIServer, SERVER_HOST)
        elif mode == "5":
            self.server(WebUI, token=False)
        elif mode == "6":
            self.server(Server)
        elif mode == "7":
            self.change_config(self.UPDATE["path"])
        elif mode == "8":
            self.change_config(self.RECORD["path"])
        elif mode == "9":
            self.change_config(self.LOGGING["path"])

    def check_settings(self):
        self.parameter = Parameter(
            self.settings,
            self.cookie,
            main_path=self.PROJECT_ROOT,
            user_agent=self.user_agent,
            ua_code=self.ua_code,
            logger=self.logger,
            xb=self.x_bogus,
            console=self.console,
            **self.settings.read(),
            blacklist=self.blacklist,
        )
        self.parameter.cleaner.set_rule(TEXT_REPLACEMENT, True)

    def run(self):
        self.check_config()
        self.version()
        self.check_update()
        self.check_settings()
        if self.disclaimer():
            self.main_menu(self.parameter.default_mode)
        self.close()

    def delete_temp(self):
        rmtree(self.PROJECT_ROOT.joinpath("./cache/temp").resolve())

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


if __name__ == '__main__':
    TikTokDownloader().run()
