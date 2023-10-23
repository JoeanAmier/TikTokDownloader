from atexit import register
from pathlib import Path
from shutil import rmtree

from flask import Flask
from requests import exceptions
from requests import get
from rich.console import Console

from src.Configuration import Parameter
from src.Configuration import Settings
from src.CookieTool import Cookie
from src.CookieTool import Register
from src.Customizer import (
    MASTER,
    WARNING,
    INFO,
    ERROR,
    GENERAL
)
from src.Customizer import SERVER_HOST
from src.Customizer import SERVER_PORT
from src.FileManager import DownloadRecorder
from src.FileManager import FileManager
from src.Parameter import Headers
from src.Parameter import NewXBogus
from src.Recorder import BaseLogger
from src.Recorder import LoggerManager
from src.main_api_server import APIServer
from src.main_complete import TikTok
from src.main_complete import prompt
from src.main_server import Server
from src.main_web_UI import WebUI


class TikTokDownloader:
    PROJECT_ROOT = Path(__file__).resolve().parent
    # PROJECT_ROOT = Path.cwd()

    VERSION = 4.3
    STABLE = False

    REPOSITORY = "https://github.com/JoeanAmier/TikTokDownloader"
    LICENCE = "GNU General Public License v3.0"
    DOCUMENTATION = "https://github.com/JoeanAmier/TikTokDownloader/wiki/Documentation"
    RELEASES = "https://github.com/JoeanAmier/TikTokDownloader/releases/latest"
    NAME = f"TikTokDownloader v{VERSION}{'' if STABLE else ' Beta'}"
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
        self.console = Console()
        self.cookie = None
        self.logger = None
        self.register = None
        self.blacklist = None
        self.user_agent, self.ua_code = Headers.generate_user_agent()
        self.x_bogus = NewXBogus()
        self.settings = Settings(self.PROJECT_ROOT, self.console)
        self.register = Register(
            self.settings,
            self.console,
            self.x_bogus,
            self.user_agent,
            self.ua_code)
        self.parameter = None

    def disclaimer(self):
        if not self.DISCLAIMER["path"].exists():
            self.console.print(
                "\n".join(
                    self.DISCLAIMER_TEXT),
                style=MASTER)
            if self.console.input(
                    f"[{MASTER}]是否已仔细阅读上述免责声明(YES/NO): [/{MASTER}]").upper() != "YES":
                exit()
            FileManager.deal_config(self.DISCLAIMER["path"])
            self.console.print()

    def version(self):
        self.console.print(f"{self.LINE}\n\n\n{self.NAME.center(
            self.WIDTH)}\n\n\n{self.LINE}\n", style=MASTER)
        self.console.print(f"项目仓库: {self.REPOSITORY}", style=MASTER)
        self.console.print(f"项目文档: {self.DOCUMENTATION}", style=MASTER)
        self.console.print(f"开源许可: {self.LICENCE}\n", style=MASTER)

    def check_config(self):
        folder = ("./src/config", "./cache", "./cache/temp")
        for i in folder:
            self.PROJECT_ROOT.joinpath(i).mkdir(exist_ok=True)
        self.UPDATE["tip"] = "启用" if self.UPDATE["path"].exists() else "禁用"
        self.RECORD["tip"] = "启用" if (
            b := self.RECORD["path"].exists()) else "禁用"
        self.LOGGING["tip"] = "禁用" if (
            l := self.LOGGING["path"].exists()) else "启用"
        self.blacklist = DownloadRecorder(
            not b, self.PROJECT_ROOT.joinpath("./cache"))
        self.logger = {True: LoggerManager, False: BaseLogger}[l]
        self.cookie = Cookie(self.settings, self.console)

    def check_update(self):
        if self.UPDATE["path"].exists():
            return
        try:
            response = get(self.RELEASES, allow_redirects=False, timeout=10)
            tag = float(response.headers['Location'].split("/")[-1])
            if tag > self.VERSION:
                self.console.print(
                    f"检测到新版本: {tag}", style=WARNING)
                self.console.print(self.RELEASES)
            if tag == self.VERSION and not self.STABLE:
                self.console.print(
                    "当前版本为测试版, 可更新至稳定版", style=WARNING)
                self.console.print(self.RELEASES)
            else:
                self.console.print("当前已是最新版本", style=INFO)
        except (exceptions.ReadTimeout, exceptions.ConnectionError):
            self.console.print("检测新版本失败", style=ERROR)
        self.console.print()

    def main(self):
        """选择运行模式"""
        mode = prompt(
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
        self.compatible(mode)

    def complete(self):
        """终端命令行模式"""
        example = TikTok(
            self.colour,
            self.blacklist,
            self.x_bogus,
            self.user_agent,
            self.ua_code,
            self.settings)
        register(self.blacklist.close)
        example.run()

    def server(self, server):
        """
        服务器模式
        """
        master = server(
            self.colour,
            self.blacklist,
            self.x_bogus,
            self.user_agent,
            self.ua_code,
            self.settings)
        app = master.run_server(Flask(__name__))
        register(self.blacklist.close)
        app.run(host=SERVER_HOST, port=SERVER_PORT, debug=not self.STABLE)

    def change_config(self, file: Path):
        FileManager.deal_config(file)
        self.console.print("修改设置成功！", style=GENERAL)
        self.check_config()
        self.main()

    def write_cookie(self):
        self.cookie.run()
        self.main()

    def auto_cookie(self):
        if cookie := self.register.run():
            self.cookie.extract(cookie, False)
        else:
            self.console.print("扫码登录失败，未写入 Cookie！", style=WARNING)
        self.main()

    def compatible(self, mode: str):
        if mode == "1":
            self.write_cookie()
        elif mode == "2":
            self.auto_cookie()
        elif mode == "3":
            self.complete()
        elif mode == "4":
            self.console.print(
                "注意：该模式暂不支持并发请求！仅以 API 形式返回数据提供调用！", style=WARNING)
            self.server(APIServer)
        elif mode == "5":
            self.server(WebUI)
        elif mode == "6":
            self.server(Server)
        elif mode == "7":
            self.change_config(self.UPDATE["path"])
        elif mode == "8":
            self.change_config(self.RECORD["path"])

    def check_settings(self):
        self.parameter = Parameter(
            main_path=self.PROJECT_ROOT,
            user_agent=self.user_agent,
            ua_code=self.ua_code,
            xb=self.x_bogus,
            console=self.console,
            **self.settings.read(),
        )

    def run(self):
        self.check_config()
        self.version()
        self.check_update()
        self.check_settings()
        self.disclaimer()
        self.main()
        self.delete_temp()

    def delete_temp(self):
        rmtree(self.PROJECT_ROOT.joinpath("./cache/temp").resolve())


if __name__ == '__main__':
    TikTokDownloader().run()
