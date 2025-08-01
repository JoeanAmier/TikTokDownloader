from time import time
from typing import TYPE_CHECKING, Callable, Coroutine, Type, Union
from urllib.parse import quote, urlencode

from httpx import AsyncClient, get, post
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)

from ..custom import PROGRESS, USERAGENT, wait
from ..tools import Retry, DownloaderError, capture_error_request, FakeProgress
from ..translation import _

if TYPE_CHECKING:
    from ..config import Parameter
    from ..testers import Params

__all__ = [
    "API",
    "APITikTok",
]


class API:
    domain = "https://www.douyin.com/"
    short_domain = "https://www.iesdouyin.com/"
    referer = f"{domain}?recommend=1"
    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "update_version_code": "170400",
        "pc_client_type": "1",
        "pc_libra_divert": "Windows",
        "version_code": "290100",
        "version_name": "29.1.0",
        "cookie_enabled": "true",
        "screen_width": "1536",
        "screen_height": "864",
        "browser_language": "zh-SG",
        "browser_platform": "Win32",
        "browser_name": "Chrome",
        "browser_version": "136.0.0.0",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "136.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "cpu_core_num": "16",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "10",
        "effective_type": "4g",
        "round_trip_time": "200",
        # "webid": "",
        "uifid": "",
        "msToken": "",
    }
    progress_object: Callable

    def __init__(
        self,
        params: Union["Parameter", "Params"],
        cookie: str = "",
        proxy: str = None,
        *args,
        **kwargs,
    ):
        self.headers = params.headers.copy()
        self.log = params.logger
        self.ab = params.ab
        self.xb = params.xb
        self.console = params.console
        self.api = ""
        self.proxy = proxy
        self.max_retry = params.max_retry
        self.timeout = params.timeout
        self.cookie = cookie
        self.client: AsyncClient = params.client
        self.pages = 99999
        self.cursor = 0
        self.response = []
        self.finished = False
        self.text = ""
        self.set_temp_cookie(cookie)

    def set_temp_cookie(self, cookie: str = ""):
        if cookie:
            self.headers["Cookie"] = cookie

    def generate_params(
        self,
    ) -> dict:
        return self.params

    def generate_data(self, *args, **kwargs) -> dict:
        return {}

    async def run(
        self,
        referer: str = None,
        single_page=False,
        data_key: str = "",
        error_text="",
        cursor="cursor",
        has_more="has_more",
        params: Callable = lambda: {},
        data: Callable = lambda: {},
        method="GET",
        headers: dict = None,
        *args,
        **kwargs,
    ):
        self.set_referer(referer)
        match single_page:
            case True:
                await self.run_single(
                    data_key,
                    error_text,
                    cursor,
                    has_more,
                    params,
                    data,
                    method,
                    headers,
                    *args,
                    **kwargs,
                )
            case False:
                await self.run_batch(
                    data_key,
                    error_text,
                    cursor,
                    has_more,
                    params,
                    data,
                    method,
                    headers,
                    *args,
                    **kwargs,
                )
            case _:
                raise DownloaderError
        return self.response

    async def run_single(
        self,
        data_key: str,
        error_text="",
        cursor="cursor",
        has_more="has_more",
        params: Callable = lambda: {},
        data: Callable = lambda: {},
        method="GET",
        headers: dict = None,
        *args,
        **kwargs,
    ):
        if data := await self.request_data(
            self.api,
            params=params() or self.generate_params(),
            data=data() or self.generate_data(),
            method=method,
            headers=headers,
            finished=True,
        ):
            self.check_response(
                data, data_key, error_text, cursor, has_more, *args, **kwargs
            )
        else:
            self.log.warning(_("获取{self_text}数据失败").format(self_text=self.text))

    async def run_batch(
        self,
        data_key: str,
        error_text="",
        cursor="cursor",
        has_more="has_more",
        params: Callable = lambda: {},
        data: Callable = lambda: {},
        method="GET",
        headers: dict = None,
        callback: Type[Coroutine] = None,
        *args,
        **kwargs,
    ):
        with self.progress_object() as progress:
            task_id = progress.add_task(
                _("正在获取{text}数据").format(text=self.text),
                total=None,
            )
            while not self.finished and self.pages > 0:
                progress.update(task_id)
                await self.run_single(
                    data_key,
                    error_text,
                    cursor,
                    has_more,
                    params,
                    data,
                    method,
                    headers,
                    *args,
                    **kwargs,
                )
                self.pages -= 1
                if callback:
                    await callback()

    def check_response(
        self,
        data_dict: dict,
        data_key: str,
        error_text="",
        cursor="cursor",
        has_more="has_more",
        *args,
        **kwargs,
    ):
        try:
            if not (d := data_dict[data_key]):
                self.log.warning(error_text)
                self.finished = True
            else:
                self.cursor = data_dict[cursor]
                self.append_response(d)
                self.finished = not data_dict[has_more]
        except KeyError:
            self.log.error(
                _("数据解析失败，请告知作者处理: {data}").format(data=data_dict)
            )
            self.finished = True

    def set_referer(self, url: str = None) -> None:
        self.headers["Referer"] = url or self.referer

    async def request_data(
        self,
        url: str,
        params: dict = None,
        data: dict = None,
        method="GET",
        headers: dict = None,
        encryption="GET",
        finished=False,
        *args,
        **kwargs,
    ):
        params = self.deal_url_params(
            params,
            encryption,
        )
        match (method, bool(self.proxy)):
            case ("GET", False):
                return await self.request_data_get(
                    url,
                    params,
                    headers or self.headers,
                    finished=finished,
                    *args,
                    **kwargs,
                )
            case ("GET", True):
                return await self.request_data_get_proxy(
                    url,
                    params,
                    headers or self.headers,
                    finished=finished,
                    *args,
                    **kwargs,
                )
            case ("POST", False):
                return await self.request_data_post(
                    url,
                    params,
                    data,
                    headers or self.headers,
                    finished=finished,
                    *args,
                    **kwargs,
                )
            case ("POST", True):
                return await self.request_data_post_proxy(
                    url,
                    params,
                    data,
                    headers or self.headers,
                    finished=finished,
                    *args,
                    **kwargs,
                )
            case _:
                raise DownloaderError

    @Retry.retry
    @capture_error_request
    async def request_data_get(
        self,
        url: str,
        params: str,
        headers: dict,
        finished=False,
        **kwargs,
    ):
        self.__record_request_messages(
            url,
            params,
            None,
            headers,
            **kwargs,
        )
        response = await self.client.get(
            f"{url}?{params}",
            headers=headers,
            **kwargs,
        )
        return await self.__return_response(response)

    @Retry.retry
    @capture_error_request
    async def request_data_get_proxy(
        self,
        url: str,
        params: str,
        headers: dict,
        finished=False,
        **kwargs,
    ):
        self.__record_request_messages(
            url,
            params,
            None,
            headers,
            **kwargs,
        )
        response = get(
            f"{url}?{params}",
            headers=headers,
            proxy=self.proxy,
            follow_redirects=True,
            verify=False,
            timeout=self.timeout,
            **kwargs,
        )
        return await self.__return_response(response)

    @Retry.retry
    @capture_error_request
    async def request_data_post(
        self, url: str, params: str, data: dict, headers: dict, finished=False, **kwargs
    ):
        self.__record_request_messages(
            url,
            params,
            data,
            headers,
            **kwargs,
        )
        response = await self.client.post(
            f"{url}?{params}",
            data=data,
            headers=headers,
            **kwargs,
        )
        return await self.__return_response(response)

    @Retry.retry
    @capture_error_request
    async def request_data_post_proxy(
        self, url: str, params: str, data: dict, headers: dict, finished=False, **kwargs
    ):
        self.__record_request_messages(
            url,
            params,
            data,
            headers,
            **kwargs,
        )
        response = post(
            f"{url}?{params}",
            data=data,
            headers=headers,
            proxy=self.proxy,
            follow_redirects=True,
            verify=False,
            timeout=self.timeout,
            **kwargs,
        )
        return await self.__return_response(response)

    async def __return_response(self, response):
        self.log.info(f"Response URL: {response.url}", False)
        self.log.info(f"Response Code: {response.status_code}", False)
        self.log.info(f"Response Headers: {dict(response.headers)}", False)
        # 记录请求体数据会导致日志文件体积过大，仅在必要时记录
        # self.log.info(f"Response Content: {response.content}", False)
        response.raise_for_status()
        await wait()
        # if response.status_code != 200:
        #     self.log.error(f"请求 {url} 失败，响应码 {response.status_code}")
        #     return
        return response.json()

    def __record_request_messages(
        self,
        url: str,
        params: str | None,
        data: dict | None,
        headers: dict,
        **kwargs,
    ):
        self.log.info(f"URL: {url}", False)
        self.log.info(f"Params: {params}", False)
        self.log.info(f"Data: {data}", False)
        # 请求头脱敏处理，不记录 Cookie
        desensitize = {k: v for k, v in headers.items() if k != "Cookie"}
        self.log.info(f"Headers: {desensitize}", False)
        self.log.info(f"Other: {kwargs}", False)

    def deal_url_params(
        self,
        params: dict,
        method="GET",
        **kwargs,
    ) -> str:
        if params:
            params = urlencode(
                params,
                quote_via=quote,
            )
            params += f"&a_bogus={self.ab.get_value(params, method)}"
            return params
        return ""

    def summary_works(
        self,
    ) -> None:
        self.log.info(
            _("共获取到 {count} 个{text}").format(
                count=len(self.response), text=self.text
            )
        )

    @classmethod
    def init_progress_object(
        cls,
        server_mode: bool = False,
    ) -> None:
        if server_mode:
            cls.progress_object = cls.__fake_progress_object
        else:
            cls.progress_object = cls.__general_progress_object

    def __general_progress_object(self):
        return Progress(
            TextColumn(
                "[progress.description]{task.description}",
                style=PROGRESS,
                justify="left",
            ),
            "•",
            BarColumn(),
            "•",
            TimeElapsedColumn(),
            console=self.console,
            transient=True,
            expand=True,
        )

    @staticmethod
    def __fake_progress_object(*args, **kwargs):
        return FakeProgress()

    def append_response(
        self,
        data: list[dict],
        start: int = None,
        end: int = None,
        *args,
        **kwargs,
    ) -> None:
        for item in data[start:end]:
            self.response.append(item)
        # self.response.extend(data[start:end])


class APITikTok(API):
    domain = "https://www.tiktok.com/"
    short_domain = ""
    referer = f"{domain}explore"
    params = {
        "WebIdLastTime": int(time()),
        "aid": "1988",
        "app_language": "en",
        "app_name": "tiktok_web",
        "browser_language": "zh-SG",
        "browser_name": "Mozilla",
        "browser_online": "true",
        "browser_platform": "Win32",
        "browser_version": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "channel": "tiktok_web",
        "cookie_enabled": "true",
        "data_collection_enabled": "true",
        "device_id": "",
        "device_platform": "web_pc",
        "focus_state": "true",
        "from_page": "user",
        "history_len": "4",
        "is_fullscreen": "false",
        "is_page_visible": "true",
        "language": "en",
        "os": "windows",
        "priority_region": "CN",
        "referer": "",
        "region": "JP",
        "screen_height": "864",
        "screen_width": "1536",
        "tz_name": "Asia/Shanghai",
        "user_is_login": "true",
        "webcast_language": "en",
        "msToken": "",
    }

    def __init__(
        self,
        params: Union["Parameter", "Params"],
        cookie: str = "",
        proxy: str = None,
        *args,
        **kwargs,
    ):
        super().__init__(params, cookie, proxy, *args, **kwargs)
        self.headers = params.headers_tiktok.copy()
        self.cookie = cookie
        self.client: AsyncClient = params.client_tiktok
        self.set_temp_cookie(cookie)

    async def request_data(
        self,
        url: str,
        params: dict = None,
        data: dict = None,
        method="GET",
        headers: dict = None,
        encryption=8,
        finished=False,
        *args,
        **kwargs,
    ):
        return await super().request_data(
            url=url,
            params=params,
            data=data,
            method=method,
            headers=headers,
            encryption=encryption,
            finished=finished,
            *args,
            **kwargs,
        )

    def deal_url_params(
        self,
        params: dict,
        number=8,
        **kwargs,
    ) -> str:
        if params:
            params = urlencode(
                params,
                quote_via=quote,
            )
            params += f"&X-Bogus={
                self.xb.get_x_bogus(
                    params, number, self.headers.get('User-Agent', USERAGENT)
                )
            }"
            return params
        return ""
