from pathlib import Path
from random import randint
from string import ascii_letters
from string import digits
from time import time

from execjs import compile
from requests import exceptions
from requests import post

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
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

    def __init__(self):
        self.path = Path("./static/js/X-Bogus.js")
        self.file = self.path.open()
        self.js = compile(self.file.read())

    def get_x_bogus(self, params: str, user_agent: str):
        return self.js.call("sign", params, user_agent)


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
    print(MsToken.get_ms_token())
    print(TtWid.get_tt_wid())
    print(WebID.get_web_id(HEADERS["User-Agent"]))
