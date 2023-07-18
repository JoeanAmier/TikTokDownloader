from pathlib import Path
from random import randint
from string import ascii_letters
from string import digits
from time import time
from urllib.parse import urlencode

from execjs import compile
from requests import exceptions
from requests import post

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82",
}


def run_time(function):
    def inner(self, *args, **kwargs):
        start = time()
        result = function(self, *args, **kwargs)
        print(f"{function.__name__}运行耗时: {time() - start}s")
        return result

    return inner


class XBogus:
    """代码参考: https://github.com/B1gM8c/X-Bogus/blob/main/X-Bogus.js"""

    def __init__(self, path="./static/js/X-Bogus.js"):
        self.path = Path(path)
        self.file = self.path.open()
        self.js = compile(self.file.read())

    def get_x_bogus(self, params: dict, user_agent: str):
        return self.js.call("sign", urlencode(params), user_agent)


class MsToken:
    """代码参考: https://github.com/B1gM8c/X-Bogus"""

    @staticmethod
    def get_ms_token(key="msToken", size=107) -> dict:
        """
        根据传入长度产生随机字符串
        """
        base_str = ascii_letters + digits
        length = len(base_str) - 1
        return {key: "".join(base_str[randint(0, length)]
                             for _ in range(size))}


class TtWid:
    """代码参考: https://github.com/B1gM8c/X-Bogus"""

    @staticmethod
    def get_tt_wid() -> dict | None:
        def clean(value) -> dict | None:
            if s := value.get("Set-Cookie", None):
                try:
                    temp = s.split("; ")[0].split("=", 1)
                    return {temp[0]: temp[1]}
                except IndexError:
                    print("提取 ttwid 参数失败！")
                    return None

        api = "https://ttwid.bytedance.com/ttwid/union/register/"
        data = '{"region":"cn","aid":1768,"needFid":false,"service":"www.ixigua.com","migrate_info":{"ticket":"","source":"node"},"cbUrlProtocol":"https","union":true}'
        try:
            response = post(api, data=data, headers=HEADERS, timeout=10)
        except (exceptions.ReadTimeout, exceptions.ConnectionError):
            print("获取 ttwid 参数失败！")
            return None
        return clean(response.headers) or None


class WebID:
    @staticmethod
    def get_web_id(ua: str) -> str | None:
        headers = HEADERS
        headers["User-Agent"] = ua
        url = "https://mcs.zijieapi.com/webid"
        data = f'{{"app_id":6383,"url":"https://www.douyin.com/","user_agent":"{ua}","referer":"https://www.douyin.com/","user_unique_id":""}}'
        try:
            response = post(url, data=data, headers=headers, timeout=10)
            return response.json()["web_id"]
        except (exceptions.ReadTimeout, exceptions.ConnectionError):
            print("获取 web_id 参数失败！")
            return None
        except (exceptions.JSONDecodeError, KeyError):
            print("web_id 参数格式异常，疑似失效！")
            return None


if __name__ == "__main__":
    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "aweme_id": "7253799364072721723",
        "cursor": "0",
        "count": "20",
        "item_type": "0",
        "insert_ids": "",
        "rcFT": "",
        "pc_client_type": "1",
        "version_code": "170400",
        "version_name": "17.4.0",
        "cookie_enabled": "true",
        "screen_width": "1536",
        "screen_height": "864",
        "browser_language": "zh-CN",
        "browser_platform": "Win32",
        "browser_name": "Edge",
        "browser_version": "114.0.1823.82",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "114.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "cpu_core_num": "16",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "10",
        "effective_type": "4g",
        "round_trip_time": "150",
        "webid": "7255592572578842152",
        "msToken": "olsNApqh7VL0M3RwGRng5MPwYkPj3FttTnESDk-umJO2EC1AoT47bDf7NcDtp5AibszMtylOpE6A2q1NabOeJvYUs3XChN6yGDmleJYaPHFavf5cMRszzsvH2LjxFVmk",
    }
    example = XBogus("../static/js/X-Bogus.js")
    print("X-Bogus", example.get_x_bogus(params, HEADERS["User-Agent"]))
    example.file.close()
    print(MsToken.get_ms_token())
    print(TtWid.get_tt_wid())
    print("webid", WebID.get_web_id(HEADERS["User-Agent"]))
