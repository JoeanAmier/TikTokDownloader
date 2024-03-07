from src.config import Parameter

__all__ = ["API"]


class API:
    domain = "https://www.douyin.com/"
    base_params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "cursor": "0",
        "count": "20",
        "item_type": "0",
        "insert_ids": "",
        "whale_cut_token": "",
        "cut_version": "1",
        "rcFT": "",
        "pc_client_type": "1",
        "version_code": "170400",
        "version_name": "17.4.0",
        "cookie_enabled": "true",
        "screen_width": "1536",
        "screen_height": "864",
        "browser_language": "zh-CN",
        "browser_platform": "Win32",
        "browser_name": "Chrome",
        "browser_version": "122.0.0.0",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "122.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "cpu_core_num": "16",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "10",
        "effective_type": "3g",
        "round_trip_time": "300",
    }

    def __init__(self, params: Parameter, cookie: str = None, *args, **kwargs):
        self.headers = params.headers
        self.log = params.logger
        self.xb = params.xb
        self.console = params.console
        self.proxies = params.proxies
        self.max_retry = params.max_retry
        self.timeout = params.timeout
        self.cookie = params.cookie
        self.cursor = 0
        self.response = []
        self.finished = False
        self.__set_temp_cookie(cookie)

    def __set_temp_cookie(self, cookie: str):
        if cookie:
            self.headers["Cookie"] = cookie

    def generate_init_params(self):
        return self.base_params

    def run(self):
        pass

    def get_data(self):
        pass

    def deal_url_params(self, params: dict, number=8):
        self.__add_ms_token(params)
        params["X-Bogus"] = self.xb.get_x_bogus(params, number)

    def __add_ms_token(self, params: dict):
        if isinstance(self.cookie, dict) and "msToken" in self.cookie:
            params["msToken"] = self.cookie["msToken"]


class APITikTok(API):
    domain = "https://www.tiktok.com/"
