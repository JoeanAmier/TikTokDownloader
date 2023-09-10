from atexit import register
from pathlib import Path
from shutil import rmtree

from flask import Flask
from requests import exceptions
from requests import get

from src.Configuration import Settings
from src.CookieTool import Cookie
from src.CookieTool import Register
from src.FileManager import DownloadRecorder
from src.FileManager import deal_config
from src.Parameter import NewXBogus
from src.Parameter import generate_user_agent
from src.StringCleaner import Colour
from src.main_api_server import APIServer
from src.main_complete import TikTok
from src.main_complete import prompt
from src.main_server import Server
from src.main_web_UI import WebUI


class TikTokDownloader:
    VERSION = 4.2
    STABLE = True

    REPOSITORY = "https://github.com/JoeanAmier/TikTokDownloader"
    LICENCE = "GNU General Public License v3.0"
    DOCUMENTATION = "https://github.com/JoeanAmier/TikTokDownloader/wiki/Documentation"
    RELEASES = "https://github.com/JoeanAmier/TikTokDownloader/releases/latest"
    NAME = f"TikTokDownloader v{VERSION}{'' if STABLE else ' Beta'}"
    WIDTH = 50
    LINE = ">" * WIDTH

    UPDATE = {"path": Path("./src/config/Disable_Update")}
    COLOUR = {"path": Path("./src/config/Disable_Colour")}
    RECORD = {"path": Path("./src/config/Disable_Record")}
    DISCLAIMER = {"path": Path("./src/config/Consent_Disclaimer")}

    DISCLAIMER_TEXT = (
        "关于 TikTokDownloader 的 免责声明：",
        "",
        "1. 使用者对本项目的使用由使用者自行决定，并自行承担风险。作者对使用者使用本项目所产生的任何损失、责任、或风险概不负责。",
        "2. 本项目的作者提供的代码和功能是基于现有知识和技术的开发成果。作者尽力确保代码的正确性和安全性，但不保证代码完全没有错误或缺陷。",
        "3. 使用者在使用本项目时必须严格遵守 GNU General Public License v3.0 的要求，并在适当的地方注明使用了 GNU General Public License v3.0 的代码。",
        "4. 使用者在任何情况下均不得将本项目的作者、贡献者或其他相关方与使用者的使用行为联系起来，或要求其对使用者使用本项目所产生的任何损失或损害负责。",
        "5. 使用者在使用本项目的代码和功能时，必须自行研究相关法律法规，并确保其使用行为合法合规。任何因违反法律法规而导致的法律责任和风险，均由使用者自行承担。",
        "6. 本项目的作者不会提供 TikTokDownloader 项目的付费版本，也不会提供与 TikTokDownloader 项目相关的任何商业服务。",
        "7. 基于本项目进行的任何二次开发、修改或编译的程序与原创作者无关，原创作者不承担与二次开发行为或其结果相关的任何责任，使用者应自行对因二次开发可能带来的各种情况负全部责任。",
        "",
        "在使用本项目的代码和功能之前，请您认真考虑并接受以上免责声明。如果您对上述声明有任何疑问或不同意，请不要使用本项目的代码和功能。如果"
        "您使用了本项目的代码和功能，则视为您已完全理解并接受上述免责声明，并自愿承担使用本项目的一切风险和后果。",
        "",
    )

    def __init__(self):
        self.colour = None
        self.cookie = None
        self.register = None
        self.blacklist = None
        self.user_agent, self.code = generate_user_agent()
        self.x_bogus = NewXBogus()
        self.settings = Settings()
        self.register = Register(
            self.settings,
            self.x_bogus,
            self.user_agent,
            self.code)

    def disclaimer(self):
        if not self.DISCLAIMER["path"].exists():
            print(self.colour.colorize("\n".join(self.DISCLAIMER_TEXT), 93))
            if input(
                    self.colour.colorize(
                        "是否已仔细阅读上述免责声明(YES/NO)",
                        93)).upper() != "YES":
                exit()
            deal_config(self.DISCLAIMER["path"])
            print()

    def version(self):
        print(
            self.colour.colorize(
                f"{self.LINE}\n\n\n{self.NAME.center(self.WIDTH)}\n\n\n{self.LINE}\n",
                93,
                bold=1))
        print(self.colour.colorize(f"项目仓库: {self.REPOSITORY}", 93))
        print(self.colour.colorize(f"项目文档: {self.DOCUMENTATION}", 93))
        print(self.colour.colorize(f"开源许可: {self.LICENCE}\n", 93))

    def check_config(self):
        folder = ("./src/config", "./cache", "./cache/temp")
        for i in folder:
            if not (c := Path(i)).is_dir():
                try:
                    c.mkdir()
                except FileNotFoundError:
                    print(f"发生预期之外的错误，请联系作者寻求解决方案，工作路径: {Path.cwd()}")
                    exit()
        self.UPDATE["tip"] = "启用" if self.UPDATE["path"].exists() else "禁用"
        self.COLOUR["tip"] = "启用" if (
            c := self.COLOUR["path"].exists()) else "禁用"
        self.RECORD["tip"] = "启用" if (
            b := self.RECORD["path"].exists()) else "禁用"
        self.colour = Colour(not c)
        self.blacklist = DownloadRecorder(not b, "./cache")
        self.cookie = Cookie(self.settings, self.colour)

    def check_update(self):
        if self.UPDATE["path"].exists():
            return
        print(self.colour.colorize("正在检测新版本", 92), end="", flush=True)
        try:
            response = get(self.RELEASES, allow_redirects=False, timeout=10)
            tag = float(response.headers['Location'].split("/")[-1])
            if tag > self.VERSION:
                print(
                    self.colour.colorize(
                        f"\r检测到新版本: {tag}",
                        92),
                    flush=True)
                print(self.RELEASES)
            if tag == self.VERSION and not self.STABLE:
                print(
                    self.colour.colorize(
                        "\r当前版本为测试版, 可更新至稳定版",
                        92),
                    flush=True)
                print(self.RELEASES)
            else:
                print(self.colour.colorize("\r当前已是最新版本", 92), flush=True)
        except (exceptions.ReadTimeout, exceptions.ConnectionError):
            print(self.colour.colorize("\r检测新版本失败", 91), flush=True)
        print()

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
             f"{self.UPDATE['tip']}检查更新功能",
             f"{self.COLOUR['tip']}彩色交互提示",
             f"{self.RECORD['tip']}作品下载记录"),
            self.colour.colorize,
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
            self.code,
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
            self.code,
            self.settings)
        app = master.run_server(Flask(__name__))
        register(self.blacklist.close)
        app.run(host="0.0.0.0", debug=False)

    def change_config(self, file: Path, tip="修改设置成功！"):
        deal_config(file)
        print(tip)
        self.check_config()
        self.main()

    def write_cookie(self):
        self.cookie.run()
        self.main()

    def auto_cookie(self):
        if cookie := self.register.run():
            self.cookie.extract(cookie)
        else:
            print("扫码登录失败，未写入 Cookie！")
        self.main()

    def compatible(self, mode: str):
        if mode == "1":
            self.write_cookie()
        elif mode == "2":
            self.auto_cookie()
        elif mode == "3":
            self.complete()
        elif mode == "4":
            print(
                self.colour.colorize(
                    "注意：该模式暂不支持并发请求！仅以 API 形式返回数据提供调用！",
                    93))
            self.server(APIServer)
        elif mode == "5":
            self.server(WebUI)
        elif mode == "6":
            self.server(Server)
        elif mode == "7":
            self.change_config(self.UPDATE["path"])
        elif mode == "8":
            self.change_config(self.COLOUR["path"], "\x1b[0m修改设置成功！\x1b[0m")
        elif mode == "9":
            self.change_config(self.RECORD["path"])

    def check_settings(self):
        if not Path("./settings.json").exists():
            self.settings.create()

    def run(self):
        self.check_config()
        self.version()
        self.check_update()
        self.check_settings()
        self.disclaimer()
        self.main()
        self.delete_temp()

    @staticmethod
    def delete_temp():
        rmtree(Path("./cache/temp").resolve())


if __name__ == '__main__':
    TikTokDownloader().run()
