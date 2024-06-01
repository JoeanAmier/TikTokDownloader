from time import time
from typing import Coroutine
from typing import TYPE_CHECKING
from typing import Type
from urllib.parse import quote

from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)

from src.custom import PROGRESS
from src.custom import USERAGENT
from src.custom import wait
from src.encrypt import ABogus
from src.tools import PrivateRetry
from src.tools import capture_error_request

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["API", "APITikTok", ]


class API:
    domain = "https://www.douyin.com/"
    referer = f"{domain}?recommend=1"
    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "pc_client_type": "1",
        "version_code": "290100",
        "version_name": "29.1.0",
        "cookie_enabled": "true",
        "screen_width": "1536",
        "screen_height": "864",
        "browser_language": "zh-CN",
        "browser_platform": "Win32",
        "browser_name": "Edge",
        "browser_version": "124.0.0.0",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "124.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "cpu_core_num": "16",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "1.45",
        "effective_type": "3g",
        "round_trip_time": "350",
    }

    def __init__(
            self,
            params: "Parameter",
            cookie: str | dict = None,
            proxy: str = None,
            *args,
            **kwargs):
        self.headers = params.headers
        self.log = params.logger
        self.ab = ABogus()
        self.xb = params.xb
        self.console = params.console
        self.api = ""
        self.proxy = proxy or params.proxy
        self.max_retry = params.max_retry
        self.timeout = params.timeout
        self.cookie = cookie or params.cookie
        self.session = params.session
        self.pages = 99999
        self.cursor = 0
        self.response = []
        self.finished = False
        self.text = ""
        self.set_temp_cookie(cookie)

    def set_temp_cookie(self, cookie: str = None):
        if cookie:
            self.headers["Cookie"] = cookie

    def generate_params(self, *args, **kwargs) -> dict:
        return self.params

    async def run(self,
                  referer: str = None,
                  single_page=False,
                  data_key: str = "",
                  error_text="",
                  cursor="cursor",
                  has_more="has_more",
                  params: dict = None,
                  data: dict = None,
                  method="get",
                  headers: dict = None,
                  proxy: str = None,
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
                    proxy,
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
                    proxy,
                    *args,
                    **kwargs,
                )
            case _:
                raise ValueError
        return self.response

    async def run_single(self,
                         data_key: str,
                         error_text="",
                         cursor="cursor",
                         has_more="has_more",
                         params: dict = None,
                         data: dict = None,
                         method="get",
                         headers: dict = None,
                         proxy: str = None,
                         *args,
                         **kwargs,
                         ):
        if data := await self.request_data(self.api,
                                           params=params or self.generate_params(),
                                           data=data,
                                           method=method,
                                           headers=headers,
                                           proxy=proxy,
                                           finished=True,
                                           ):
            self.check_response(
                data,
                data_key,
                error_text,
                cursor,
                has_more,
                *args,
                **kwargs)
        else:
            self.log.warning(f"获取{self.text}失败")

    async def run_batch(self,
                        data_key: str,
                        error_text="",
                        cursor="cursor",
                        has_more="has_more",
                        params: dict = None,
                        data: dict = None,
                        method="get",
                        headers: dict = None,
                        proxy: str = None,
                        callback: Type[Coroutine] = None,
                        *args,
                        **kwargs, ):
        with self.progress_object() as progress:
            task_id = progress.add_task(
                f"正在获取{self.text}", total=None)
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
                    proxy,
                    *args,
                    **kwargs,
                )
                self.pages -= 1
                if callback:
                    await callback()
                # TODO: 调试代码，待注释
                break

    def check_response(self,
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
                self.log.info(error_text)
                self.finished = True
            else:
                self.cursor = data_dict[cursor]
                self.append_response(d)
                self.finished = not data_dict[has_more]
        except KeyError:
            self.log.error(f"数据解析失败，请告知作者处理: {data_dict}")
            self.finished = True

    def set_referer(self, url: str = None) -> None:
        self.headers["Referer"] = url or self.referer

    async def request_data(self,
                           url: str,
                           params: dict = None,
                           data: dict = None,
                           method="get",
                           headers: dict = None,
                           proxy: str = None,
                           number=8,
                           finished=False,
                           *args,
                           **kwargs):
        self.deal_url_params(params, number, )
        match method:
            case "get":
                return await self.__request_data_get(url, params, headers or self.headers, proxy or self.proxy,
                                                     finished, *args, **kwargs)
            case "post":
                return await self.__request_data_post(url, params, data, headers or self.headers, proxy or self.proxy,
                                                      finished, *args, **kwargs)
            case _:
                raise ValueError(f"尚未支持的请求方法 {method}")

    @PrivateRetry.retry
    @capture_error_request
    async def __request_data_get(self,
                                 url: str,
                                 params: dict,
                                 headers: dict,
                                 proxy: str,
                                 finished=False,
                                 **kwargs,
                                 ):
        async with self.session.get(url, params=params, headers=headers, proxy=proxy, **kwargs) as response:
            await wait()
            if response.status != 200:
                self.log.error(f"请求 {url} 失败，响应码 {response.status}")
                return
            return await response.json()

    @PrivateRetry.retry
    @capture_error_request
    async def __request_data_post(self,
                                  url: str,
                                  params: dict,
                                  data: dict,
                                  headers: dict,
                                  proxy: str,
                                  finished=False,
                                  **kwargs):
        async with self.session.post(url, params=params, data=data, headers=headers, proxy=proxy, **kwargs) as response:
            await wait()
            if response.status != 200:
                self.log.error(f"请求 {url} 失败，响应码 {response.status}")
                return
            return await response.json()

    def deal_url_params(self, params: dict, number=8):
        if params:
            self.__add_ms_token(params)
            params["a_bogus"] = self.ab.get_value(params)
            # X-Bogus 依旧可用
            # params["X-Bogus"] = quote(self.xb.get_x_bogus(params,
            #                                               number), safe="")

    def __add_ms_token(self, params: dict):
        if isinstance(self.cookie, dict) and "msToken" in self.cookie:
            params["msToken"] = self.cookie["msToken"]

    def summary_works(self, ) -> None:
        self.log.info(f"共获取到 {len(self.response)} 个{self.text}")

    def progress_object(self):
        return Progress(
            TextColumn(
                "[progress.description]{task.description}",
                style=PROGRESS,
                justify="left"),
            "•",
            BarColumn(),
            "•",
            TimeElapsedColumn(),
            console=self.console,
            transient=True,
            expand=True,
        )

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


class APITikTok(API):
    domain = "https://www.tiktok.com/"
    referer = domain
    params = {
        "WebIdLastTime": int(time()),
        "aid": "1988",
        "app_language": "zh-Hans",
        "app_name": "tiktok_web",
        "browser_language": "zh-CN",
        "browser_name": "Mozilla",
        "browser_online": "true",
        "browser_platform": "Win32",
        "browser_version": quote(USERAGENT.lstrip("Mozilla/"), safe=""),
        "channel": "tiktok_web",
        "cookie_enabled": "true",
        # "count": "35",
        # "coverFormat": "2",
        # "cursor": "0",
        "device_id": "7367953287817676308",
        "device_platform": "web_pc",
        "focus_state": "true",
        "from_page": "user",
        "history_len": "2",
        "is_fullscreen": "false",
        "is_page_visible": "true",
        "language": "zh-Hans",
        "odinId": "7367953265152525328",
        "os": "windows",
        "priority_region": "",
        "referer": "",
        "region": "SG",
        "screen_height": "864",
        "screen_width": "1536",
        "tz_name": quote("Asia/Shanghai", safe=""),
        "webcast_language": "zh-Hans",
        "msToken": "",
    }

    def __init__(self,
                 params: "Parameter",
                 cookie: str | dict = None,
                 proxy: str = None,
                 *args,
                 **kwargs,
                 ):
        super().__init__(params, cookie, proxy, *args, **kwargs, )
        self.headers = params.headers_tiktok
        self.cookie = cookie or params.cookie_tiktok
        self.proxy = proxy or params.proxy_tiktok
        self.set_temp_cookie(cookie)

    def deal_url_params(self, params: dict, number=8):
        if params:
            self.__add_ms_token(params)
            params["X-Bogus"] = quote(self.xb.get_x_bogus(params,
                                                          number), safe="")

    # async def run(self,
    #               referer: str = None,
    #               single_page=False,
    #               data_key: str = "",
    #               error_text="",
    #               cursor="cursor",
    #               has_more="hasMore",
    #               params: dict = None,
    #               *args,
    #               **kwargs,
    #               ):
    #     return await super().run(
    #         referer,
    #         single_page,
    #         data_key,
    #         error_text,
    #         cursor,
    #         has_more,
    #         params,
    #         *args,
    #         **kwargs, )
    #
    # async def run_single(self,
    #                      data_key: str,
    #                      error_text="",
    #                      cursor="cursor",
    #                      has_more="hasMore",
    #                      params: dict = None,
    #                      *args,
    #                      **kwargs,
    #                      ):
    #     await super().run_single(
    #         data_key,
    #         error_text,
    #         cursor,
    #         has_more,
    #         params,
    #         *args,
    #         **kwargs,
    #     )
    #
    # async def run_batch(self,
    #                     data_key: str,
    #                     error_text="",
    #                     cursor="cursor",
    #                     has_more="hasMore",
    #                     params: dict = None,
    #                     callback: Type[Coroutine] = None,
    #                     *args,
    #                     **kwargs, ):
    #     await super().run_batch(
    #         data_key,
    #         error_text,
    #         cursor,
    #         has_more,
    #         params,
    #         callback,
    #         *args,
    #         **kwargs,
    #     )
    #
    # def check_response(self,
    #                    data_dict: dict,
    #                    data_key: str,
    #                    error_text="",
    #                    cursor="cursor",
    #                    has_more="hasMore",
    #                    *args,
    #                    **kwargs,
    #                    ):
    #     super().check_response(
    #         data_dict,
    #         data_key,
    #         error_text,
    #         cursor,
    #         has_more,
    #         *args,
    #         **kwargs,
    #     )
