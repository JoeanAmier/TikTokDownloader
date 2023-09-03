from re import finditer
from time import sleep

from qrcode import QRCode
from requests import exceptions
from requests import get

from src.Customizer import check_login
from src.Parameter import TtWid
from src.Parameter import VerifyFp

__all__ = ["Cookie", "Register"]


class Cookie:
    pattern = r'(?P<key>[^=;,]+)=(?P<value>[^;,]+)'

    def __init__(self, settings, colour):
        self.settings = settings
        self.colour = colour

    def run(self):
        """提取 Cookie 并写入配置文件"""
        if not (cookie := input("请粘贴 Cookie 内容：")):
            return
        self.extract(cookie)

    def extract(self, cookie: str):
        get_key = {
            "passport_csrf_token": None,
            "passport_csrf_token_default": None,
            "passport_auth_status": None,
            "passport_auth_status_ss": None,
            "sid_guard": None,
            "uid_tt": None,
            "uid_tt_ss": None,
            "sid_tt": None,
            "sessionid": None,
            "sessionid_ss": None,
            "sid_ucp_v1": None,
            "ssid_ucp_v1": None,
            "csrf_session_id": None,
            "odin_tt": None,
        }
        matches = finditer(self.pattern, cookie)
        for match in matches:
            key = match.group('key').strip()
            value = match.group('value').strip()
            if key in get_key:
                get_key[key] = value
        self.check_key(get_key)
        self.write(get_key)
        print("写入 Cookie 成功！")

    @staticmethod
    def check_key(items):
        if not items["sessionid_ss"]:
            print("当前 Cookie 未登录")
        else:
            print("当前 Cookie 已登录")
        keys_to_remove = [key for key, value in items.items() if value is None]
        for key in keys_to_remove:
            del items[key]

    def write(self, text):
        data = self.settings.read()
        data["cookie"] = text
        self.settings.update(data)


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

    def __init__(self, settings, xb, user_agent, ua_code):
        self.xb = xb
        self.settings = settings
        self.headers = {
            "User-Agent": user_agent,
            "Referer": "https://www.douyin.com/",
            "Cookie": self.generate_cookie(TtWid.get_tt_wid()),
        }
        self.verify_fp = None
        self.ua_code = ua_code

    @staticmethod
    def generate_cookie(data: dict) -> str:
        result = [f"{k}={v}" for k, v in data.items()]
        return "; ".join(result)

    @staticmethod
    def generate_dict(data: str) -> dict:
        cookie = {}
        matches = finditer(Cookie.pattern, data)
        for match in matches:
            key = match.group('key').strip()
            value = match.group('value').strip()
            cookie[key] = value
        return cookie

    @staticmethod
    def generate_qr_code(url):
        qr_code = QRCode()
        assert url, "无效的登录二维码 URL，请联系作者处理！"
        qr_code.add_data(url)
        qr_code.make(fit=True)
        qr_code.print_ascii(invert=True)
        image = qr_code.make_image()
        try:
            image.show()
        except AttributeError:
            print("打开登录二维码图片失败，请扫描终端二维码！")

    def get_qr_code(self, version=23):
        self.verify_fp = VerifyFp.get_verify_fp()
        self.get_params["verifyFp"] = self.verify_fp
        self.get_params["fp"] = self.verify_fp
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

    def check_register(self, token):
        self.check_params["token"] = token
        self.check_params["verifyFp"] = self.verify_fp
        self.check_params["fp"] = self.verify_fp
        retry = 0
        while retry < 15:
            self.wait()
            if not (
                    response := self.request_data(
                        False,
                        url=self.check_url,
                        params=self.check_params)):
                continue
            # print(response.json())  # 调试使用
            data = response.json().get("data")
            if not data:
                print(f"发生未知错误: {response.json()}")
                retry = 15
            elif (s := data["status"]) == "3":
                redirect_url = data["redirect_url"]
                cookie = response.headers.get("Set-Cookie")
                break
            elif s in ("4", "5"):
                retry = 15
            else:
                retry += 1
        else:
            print("扫码登录失败，请手动获取 Cookie 并写入配置文件！")
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
        return response.history[1].headers.get("Set-Cookie")

    @staticmethod
    def wait():
        sleep(2)
        print("正在检查登录结果！")

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

    def run(self):
        url, token = self.get_qr_code()
        if not url:
            return False
        self.generate_qr_code(url)
        if check_login():
            return False
        url, cookie = self.check_register(token)
        return self.get_cookie(url, cookie) if url else False
