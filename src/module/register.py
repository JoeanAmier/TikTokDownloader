from platform import system
from subprocess import run
from time import sleep
from typing import TYPE_CHECKING
from urllib.parse import quote

from httpx import HTTPError
from qrcode import QRCode
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from ..custom import ERROR, PROGRESS, QRCODE_HEADERS, WARNING
from ..encrypt import MsToken

# from ..encrypt import VerifyFp
from ..tools import Retry, cookie_str_to_str

if TYPE_CHECKING:
    from ..config import Parameter, Settings

__all__ = ["__Register"]


class __Register:
    """
    扫码登录功能已过期
    """

    get_url = "https://sso.douyin.com/get_qrcode/"
    check_url = "https://sso.douyin.com/check_qrconnect/"

    def __init__(
        self,
        params: "Parameter",
        settings: "Settings",
    ):
        self.ab = params.ab
        self.xb = params.xb
        self.client = params.client
        self.settings = settings
        self.console = params.console
        self.log = params.logger
        self.headers = QRCODE_HEADERS
        self.proxy = params.proxy
        # self.verify_fp = None
        self.cache = params.cache
        self.url_params = {
            "service": "https://www.douyin.com",
            "need_logo": "false",
            "need_short_url": "true",
            "passport_jssdk_version": "1.0.22",
            "passport_jssdk_type": "pro",
            "aid": "6383",
            "language": "zh",
            "account_sdk_source": "sso",
            "account_sdk_source_info": "7e276d64776172647760466a6b66707777606b667c273f3433292772606761776c736077273"
            "f63646976602927756970626c6b76273f5e2755414325536c60726077272927466d776a6860"
            "2555414325536c60726077272927466d776a686c70682555414325536c60726077272927486"
            "c66776a766a637125406162602555414325536c607260772729275260674e6c712567706c69"
            "71286c6b2555414327582927756077686c76766c6a6b76273f5e7e276b646860273f2762606"
            "a696a6664716c6a6b2729277671647160273f2761606b6c60612778297e276b646860273f27"
            "6b6a716c636c6664716c6a6b762729277671647160273f2775776a6875712778297e276b646"
            "860273f27736c61606a5a666475717077602729277671647160273f2761606b6c6061277829"
            "7e276b646860273f276470616c6a5a666475717077602729277671647160273f2761606b6c6"
            "06127785829276c6b6b60774d606c626d71273f32313729276c6b6b6077526c61716d273f34"
            "30363329276a707160774d606c626d71273f3d333129276a70716077526c61716d273f34303"
            "633292767606d64736c6a77273f7e27716a70666d273f63646976602927686a707660273f71"
            "77706029276e607c476a647761273f717770607829277260676269273f7e27736077766c6a6"
            "b273f27526067424925342b35252d4a75606b424925405625372b3525466d776a686c70682c"
            "27292773606b616a77273f275260674e6c7127292777606b6160776077273f275260674e6c7"
            "125526067424927782927776074706076715a6d6a7671273f277272722b616a707c6c6b2b66"
            "6a68272927776074706076715a7564716d6b646860273f272a2778",
            "passport_ztsdk": "0",
            "passport_verify": "1.0.14",
            # "biz_trace_id": "26eba5d6",
            "device_platform": "web_app",
            "msToken": "",
        }

    def __check_progress_object(self):
        return Progress(
            TextColumn(
                "[progress.description]{task.description}",
                style=PROGRESS,
                justify="left",
            ),
            SpinnerColumn(),
            BarColumn(),
            "•",
            TimeElapsedColumn(),
            console=self.console,
            transient=True,
            expand=True,
        )

    def generate_qr_code(self, url: str):
        qr_code = QRCode()
        # assert url, "无效的登录二维码数据"
        qr_code.add_data(url)
        qr_code.make(fit=True)
        qr_code.print_ascii(invert=True)
        img = qr_code.make_image()
        img.save(self.cache)
        self.console.print(
            "请使用抖音 APP 扫描二维码登录，如果二维码无法识别，请尝试更换终端或者选择其他方式写入 Cookie！"
        )
        self._open_qrcode_image()

    def _open_qrcode_image(self):
        if (s := system()) == "Darwin":  # macOS
            run(["open", self.cache])
        elif s == "Windows":  # Windows
            run(["start", self.cache], shell=True)
        elif s == "Linux":  # Linux
            run(["xdg-open", self.cache])

    async def get_qr_code(self):
        # self.verify_fp = VerifyFp.get_verify_fp()
        # self.url_params["verifyFp"] = self.verify_fp
        # self.url_params["fp"] = self.verify_fp
        await self.__set_ms_token()
        self.url_params["a_bogus"] = quote(self.ab.get_value(self.url_params), safe="")
        # self.url_params["X-Bogus"] = self.xb.get_x_bogus(self.url_params)
        data, _, _ = await self.request_data(
            url=self.get_url,
            params=self.url_params,
        )
        if not data:
            return None, None
        try:
            url = data["data"]["qrcode_index_url"]
            token = data["data"]["token"]
            return url, token
        except KeyError:
            return None, None

    async def __set_ms_token(self):
        if isinstance(
            t := await MsToken.get_real_ms_token(
                self.log,
                self.headers,
                **self.proxy,
            ),
            dict,
        ):
            self.url_params["msToken"] = t["msToken"]

    async def check_register(self, token):
        self.url_params["token"] = token
        self.url_params |= {"is_frontier": "false"}
        with self.__check_progress_object() as progress:
            task_id = progress.add_task("正在检查登录状态", total=None)
            second = 0
            while second < 30:
                sleep(1)
                progress.update(task_id)
                data, headers, _ = await self.request_data(
                    url=self.check_url, params=self.url_params
                )
                if not data:
                    self.console.print("网络异常，无法获取登录状态！", style=WARNING)
                    second = 30
                    continue
                # print(response.json())  # 调试使用
                if data.get("error_code"):
                    self.console.print(
                        f"该账号疑似被风控，建议近期避免扫码登录账号！\n响应数据: {data}",
                        style=WARNING,
                    )
                    second = 30
                elif not (data := data.get("data")):
                    self.console.print(f"响应内容异常: {data}", style=ERROR)
                    second = 30
                elif (s := data["status"]) == "3":
                    redirect_url = data["redirect_url"]
                    cookie = headers.get("Set-Cookie")
                    break
                elif s in (
                    "4",
                    "5",
                ):
                    second = 30
                else:
                    second += 1
            else:
                self.console.print(
                    "扫码登录失败，请使用其他方式获取 Cookie 并写入配置文件！",
                    style=WARNING,
                )
                return None, None
            return redirect_url, cookie

    async def get_cookie(self, url, cookie):
        self.headers["Cookie"] = cookie_str_to_str(cookie)
        _, _, history = await self.request_data(False, url=url)
        if not history or history[0].status_code != 302:
            return False
        return cookie_str_to_str(history[1].headers.get("Set-Cookie"))

    @Retry.retry_lite
    async def request_data(self, json=True, **kwargs):
        try:
            response = await self.client.get(headers=self.headers, **kwargs)
            data = response.json() if json else None
            headers = response.headers
            history = response.history
            return data, headers, history
        except HTTPError as e:
            self.console.print(
                f"扫码登录发生异常，请向作者反馈，错误信息: {e}", style=ERROR
            )
            return None, None, None

    async def run(
        self,
    ):
        self.cache = str(self.cache.joinpath("扫码后请关闭该图片.png"))
        url, token = await self.get_qr_code()
        if not url:
            return False
        self.generate_qr_code(url)
        url, cookie = await self.check_register(token)
        return await self.get_cookie(url, cookie) if url else False
