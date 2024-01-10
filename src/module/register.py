from pathlib import Path
from platform import system
from re import finditer
from subprocess import run
from time import sleep

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
from src.custom import WARNING
from src.encrypt import MsToken
from src.encrypt import TtWid
from src.encrypt import VerifyFp
from src.module.cookie import Cookie

__all__ = ["Register"]


class Register:
    """
    逻辑参考: https://github.com/Johnserf-Seed/TikTokDownload/blob/main/Util/Login.py
    """
    get_url = "https://sso.douyin.com/get_qrcode/"
    check_url = "https://sso.douyin.com/check_qrconnect/"
    get_params = {
        "service": "https://www.douyin.com",
        "need_logo": "false",
        "need_short_url": "true",
        "device_platform": "web_app",
        "aid": "6383",
        "account_sdk_source": "sso",
        "sdk_version": "2.2.5",
        "language": "zh",
    }
    check_params = {
        "service": "https://www.douyin.com",
        "need_logo": "false",
        "need_short_url": "false",
        "device_platform": "web_app",
        "aid": "6383",
        "account_sdk_source": "sso",
        "sdk_version": "2.2.5",
        "language": "zh",
    }

    def __init__(self, settings, console, xb, user_agent, ua_code):
        self.xb = xb
        self.settings = settings
        self.console = console
        self.headers = {
            "User-Agent": user_agent,
            "Referer": "https://www.douyin.com/",
            "Cookie": self.generate_cookie(TtWid.get_tt_wid()),
        }
        self.verify_fp = None
        self.ua_code = ua_code
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

    @staticmethod
    def generate_cookie(data: dict) -> str:
        if not isinstance(data, dict):
            return ""
        result = [f"{k}={v}" for k, v in data.items()]
        return "; ".join(result)

    @staticmethod
    def generate_dict(data: str) -> dict:
        cookie = {}
        if not isinstance(data, str):
            return cookie
        matches = finditer(Cookie.pattern, data)
        for match in matches:
            key = match.group('key').strip()
            value = match.group('value').strip()
            cookie[key] = value
        return cookie

    def generate_qr_code(self, url: str):
        qr_code = QRCode()
        # assert url, "无效的登录二维码数据"
        qr_code.add_data(url)
        qr_code.make(fit=True)
        qr_code.print_ascii(invert=True)
        img = qr_code.make_image()
        img.save(self.temp)
        self.console.print(
            "请使用抖音 APP 扫描二维码登录，如果二维码无法识别，请尝试更换终端或者手动复制粘贴写入 Cookie！")
        self._open_qrcode_image()

    def _open_qrcode_image(self):
        if (s := system()) == "Darwin":  # macOS
            run(["open", self.temp])
        elif s == "Windows":  # Windows
            run(["start", self.temp], shell=True)
        elif s == "Linux":  # Linux
            run(["xdg-open", self.temp])

    def get_qr_code(self, version=23):
        self.verify_fp = VerifyFp.get_verify_fp()
        self.get_params["verifyFp"] = self.verify_fp
        self.get_params["fp"] = self.verify_fp
        self.__set_ms_token()
        self.get_params["X-Bogus"] = self.xb.get_x_bogus(
            self.get_params, self.ua_code, version)
        if not (
                data := self.request_data(
                    url=self.get_url,
                    params=self.get_params)):
            return None, None
        url = data["data"]["qrcode_index_url"]
        token = data["data"]["token"]
        return url, token

    def __set_ms_token(self):
        if isinstance(t := MsToken.get_real_ms_token(), dict):
            self.get_params["msToken"] = t["msToken"]

    def check_register(self, token):
        self.check_params["token"] = token
        self.check_params["verifyFp"] = self.verify_fp
        self.check_params["fp"] = self.verify_fp
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
                            params=self.check_params)):
                    self.console.print("网络异常，无法获取登录状态！", style=WARNING)
                    second = 30
                    continue
                # print(response.json())  # 调试使用
                data = response.json().get("data")
                if not data:
                    self.console.print(
                        f"响应内容异常: {response.json()}",
                        style=ERROR)
                    second = 30
                elif (s := data["status"]) == "3":
                    redirect_url = data["redirect_url"]
                    cookie = response.headers.get("Set-Cookie")
                    break
                elif s in ("4", "5"):
                    second = 30
                else:
                    second += 1
            else:
                self.console.print(
                    "扫码登录失败，请手动获取 Cookie 并写入配置文件！", style=WARNING)
                return None, None
            return redirect_url, cookie

    def clean_cookie(self, cookie) -> str:
        return self.generate_cookie(self.generate_dict(cookie))

    def get_cookie(self, url, cookie):
        self.headers["Cookie"] = self.clean_cookie(cookie)
        if not (response := self.request_data(False, url=url)):
            return False
        elif response.history[0].status_code != 302:
            return False
        return self.clean_cookie(response.history[1].headers.get("Set-Cookie"))

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
