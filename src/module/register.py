from pathlib import Path
from platform import system
from subprocess import run
from time import sleep
from typing import TYPE_CHECKING

from qrcode import QRCode
from requests import exceptions
from requests import get
from rich.progress import (
    SpinnerColumn,
    BarColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)

from src.custom import ERROR
from src.custom import PROGRESS
from src.custom import USERAGENT
from src.custom import WARNING
from src.encrypt import MsToken
from src.encrypt import VerifyFp
from src.tools import cookie_str_to_str

if TYPE_CHECKING:
    from src.config import Settings
    from src.tools import ColorfulConsole
    from src.encrypt import XBogus

__all__ = ["Register"]


class Register:
    get_url = "https://sso.douyin.com/get_qrcode/"
    check_url = "https://sso.douyin.com/check_qrconnect/"
    url_params = {
        "service": "https://www.douyin.com",
        "need_logo": "false",
        "need_short_url": "true",
        "account_sdk_source": "sso",
        "aid": "6383",
        "language": "zh",
        "sdk_version": "2.2.7-beta.6",
        "device_platform": "web_app",
    }

    def __init__(
            self,
            settings: "Settings",
            console: "ColorfulConsole",
            xb: "XBogus"):
        self.xb = xb
        self.settings = settings
        self.console = console
        self.headers = {
            "User-Agent": USERAGENT,
            "Referer": "https://www.douyin.com/",
        }
        self.verify_fp = None
        self.temp = None

    def __check_progress_object(self):
        return Progress(
            TextColumn(
                "[progress.description]{task.description}",
                style=PROGRESS,
                justify="left"),
            SpinnerColumn(),
            BarColumn(
                bar_width=20),
            "•",
            TimeElapsedColumn(),
            console=self.console,
            transient=True,
        )

    def generate_qr_code(self, url: str):
        qr_code = QRCode()
        # assert url, "无效的登录二维码数据"
        qr_code.add_data(url)
        qr_code.make(fit=True)
        qr_code.print_ascii(invert=True)
        img = qr_code.make_image()
        img.save(self.temp)
        self.console.print(
            "请使用抖音 APP 扫描二维码登录，如果二维码无法识别，请尝试更换终端或者选择其他方式写入 Cookie！")
        self._open_qrcode_image()

    def _open_qrcode_image(self):
        if (s := system()) == "Darwin":  # macOS
            run(["open", self.temp])
        elif s == "Windows":  # Windows
            run(["start", self.temp], shell=True)
        elif s == "Linux":  # Linux
            run(["xdg-open", self.temp])

    def get_qr_code(self):
        self.verify_fp = VerifyFp.get_verify_fp()
        self.url_params["verifyFp"] = self.verify_fp
        self.url_params["fp"] = self.verify_fp
        self.url_params["X-Bogus"] = self.xb.get_x_bogus(self.url_params)
        if not (
                data := self.request_data(
                    url=self.get_url,
                    params=self.url_params)):
            return None, None
        url = data["data"]["qrcode_index_url"]
        token = data["data"]["token"]
        return url, token

    def __set_ms_token(self):
        if isinstance(t := MsToken.get_real_ms_token(), dict):
            self.url_params["msToken"] = t["msToken"]

    def check_register(self, token):
        self.url_params["token"] = token
        with self.__check_progress_object() as progress:
            task_id = progress.add_task(
                "正在检查登录状态", total=None)
            second = 0
            while second < 30:
                sleep(1)
                progress.update(task_id)
                if not (
                        response := self.request_data(
                            False,
                            url=self.check_url,
                            params=self.url_params)):
                    self.console.print("网络异常，无法获取登录状态！", style=WARNING)
                    second = 30
                    continue
                # print(response.json())  # 调试使用
                json_data: dict = response.json()
                if json_data.get("error_code"):
                    self.console.print(
                        f"该账号疑似被风控，建议近期避免扫码登录账号！\n响应数据: {json_data}",
                        style=WARNING)
                    second = 30
                elif not (data := json_data.get("data")):
                    self.console.print(
                        f"响应内容异常: {json_data}",
                        style=ERROR)
                    second = 30
                elif (s := data["status"]) == "3":
                    redirect_url = data["redirect_url"]
                    cookie = response.headers.get("Set-Cookie")
                    break
                elif s in ("4", "5",):
                    second = 30
                else:
                    second += 1
            else:
                self.console.print(
                    "扫码登录失败，请手动获取 Cookie 并写入配置文件！", style=WARNING)
                return None, None
            return redirect_url, cookie

    def get_cookie(self, url, cookie):
        self.headers["Cookie"] = cookie_str_to_str(cookie)
        if not (response := self.request_data(False, url=url)):
            return False
        elif response.history[0].status_code != 302:
            return False
        return cookie_str_to_str(response.history[1].headers.get("Set-Cookie"))

    def request_data(self, json=True, **kwargs):
        try:
            response = get(timeout=10, headers=self.headers, **kwargs)
            return response.json() if json else response
        except (
                exceptions.ReadTimeout,
                exceptions.ChunkedEncodingError,
                exceptions.ConnectionError,
                exceptions.JSONDecodeError
        ):
            return None

    def run(self, temp: Path):
        self.temp = str(temp.joinpath("扫码后请关闭该图片.png"))
        url, token = self.get_qr_code()
        if not url:
            return False
        self.generate_qr_code(url)
        url, cookie = self.check_register(token)
        return self.get_cookie(url, cookie) if url else False
