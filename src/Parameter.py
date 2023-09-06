from hashlib import md5
from random import randint
from random import random
from string import ascii_letters
from string import digits
from time import time
from urllib.parse import urlencode

# from execjs import compile
from requests import exceptions
from requests import post

__all__ = ['generate_user_agent', 'NewXBogus', 'MsToken', 'TtWid', 'VerifyFp']


def generate_user_agent() -> tuple[str, tuple]:
    user_agent = (
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183",
            ((86,
              138),
             (238,
              238,
              ),
             )),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            ((42,
              110),
             (95,
              187),
             )),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            ((115,
              235,
              ),
             (151,
              95),
             )),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188",
            ((155,
              54),
             (11,
              101))),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1788.0",
            ((56,
              22),
             (77,
              86)),
        ),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.0.0",
            ((116,
              247),
             (11,
              146))),
        (
            "Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5666.197 Safari/537.36",
            ((244,
              163),
             (18,
              102))),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            ((107,
              91),
             (236,
              31))),
    )

    return user_agent[randint(0, len(user_agent) - 1)]


def run_time(function):
    def inner(self, *args, **kwargs):
        start = time()
        result = function(self, *args, **kwargs)
        print(f"{function.__name__}运行耗时: {time() - start}s")
        return result

    return inner


class NewXBogus:
    __string = "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe="
    __array = [None for _ in range(
        48)] + list(range(10)) + [None for _ in range(39)] + list(range(10, 16))
    __canvas = {
        23: 1256363761,
        20: None,
        174: 1256363761,
    }
    __params = {
        23: 14,
        174: 4,
        20: None,
    }
    __index = {
        23: 0,
        174: 1,
        20: None,
    }

    @staticmethod
    def disturb_array(
            a, b, e, d, c, f, t, n, o, i, r, _, x, u, s, l, v, h, g
    ):
        array = [0] * 19
        array[0] = a
        array[10] = b
        array[1] = e
        array[11] = d
        array[2] = c
        array[12] = f
        array[3] = t
        array[13] = n
        array[4] = o
        array[14] = i
        array[5] = r
        array[15] = _
        array[6] = x
        array[16] = u
        array[7] = s
        array[17] = l
        array[8] = v
        array[18] = h
        array[9] = g
        return array

    @staticmethod
    def generate_garbled_1(
            a,
            b,
            e,
            d,
            c,
            f,
            t,
            n,
            o,
            i,
            r,
            _,
            x,
            u,
            s,
            l,
            v,
            h,
            g):
        array = [0] * 19
        array[0] = a
        array[1] = r
        array[2] = b
        array[3] = _
        array[4] = e
        array[5] = x
        array[6] = d
        array[7] = u
        array[8] = c
        array[9] = s
        array[10] = f
        array[11] = l
        array[12] = t
        array[13] = v
        array[14] = n
        array[15] = h
        array[16] = o
        array[17] = g
        array[18] = i
        return "".join(map(chr, map(int, array)))

    @staticmethod
    def generate_num(text):
        return [
            ord(text[i]) << 16 | ord(text[i + 1]) << 8 | ord(text[i + 2]) << 0
            for i in range(0, 21, 3)
        ]

    @staticmethod
    def generate_garbled_2(a, b, c):
        return chr(a) + chr(b) + c

    @staticmethod
    def generate_garbled_3(a, b):
        d = list(range(256))
        c = 0
        f = ""
        for a_idx in range(256):
            d[a_idx] = a_idx
        for b_idx in range(256):
            c = (c + d[b_idx] + ord(a[b_idx % len(a)])) % 256
            e = d[b_idx]
            d[b_idx] = d[c]
            d[c] = e
        t = 0
        c = 0
        for b_idx in range(len(b)):
            t = (t + 1) % 256
            c = (c + d[t]) % 256
            e = d[t]
            d[t] = d[c]
            d[c] = e
            f += chr(ord(b[b_idx]) ^ d[(d[t] + d[c]) % 256])
        return f

    def calculate_md5(self, input_string):
        if isinstance(input_string, str):
            array = self.md5_to_array(input_string)
        elif isinstance(input_string, list):
            array = input_string
        else:
            raise TypeError

        md5_hash = md5()
        md5_hash.update(bytes(array))
        return md5_hash.hexdigest()

    def md5_to_array(self, md5_str):
        if isinstance(md5_str, str) and len(md5_str) > 32:
            return [ord(char) for char in md5_str]
        else:
            return [
                (self.__array[ord(md5_str[index])] << 4)
                | self.__array[ord(md5_str[index + 1])]
                for index in range(0, len(md5_str), 2)
            ]

    def process_url_path(self, url_path):
        return self.md5_to_array(
            self.calculate_md5(self.md5_to_array(self.calculate_md5(url_path)))
        )

    def generate_str(self, num):
        string = [num & 16515072, num & 258048, num & 4032, num & 63]
        string = [i >> j for i, j in zip(string, range(18, -1, -6))]
        return "".join([self.__string[i] for i in string])

    # @run_time
    def generate_x_bogus(
            self,
            query: list,
            version: int,
            code: tuple,
            timestamp: int):
        array = [
            64,
            0.00390625,
            1,
            self.__params[version],
            query[-2],
            query[-1],
            69,
            63,
            *code,
            timestamp >> 24 & 255,
            timestamp >> 16 & 255,
            timestamp >> 8 & 255,
            timestamp >> 0 & 255,
            self.__canvas[version] >> 24 & 255,
            self.__canvas[version] >> 16 & 255,
            self.__canvas[version] >> 8 & 255,
            self.__canvas[version] >> 0 & 255,
            None,
        ]
        zero = 0
        for i in array[:-1]:
            if isinstance(i, float):
                i = int(i)
            zero ^= i
        array[-1] = zero
        garbled = self.generate_garbled_1(*self.disturb_array(*array))
        garbled = self.generate_garbled_2(
            2, 255, self.generate_garbled_3("ÿ", garbled))
        return "".join(self.generate_str(i)
                       for i in self.generate_num(garbled))

    def get_x_bogus(
            self,
            query: dict,
            user_agent: tuple,
            version=23,
            test_time=None):
        timestamp = int(test_time or time())
        query = self.process_url_path(urlencode(query))
        return self.generate_x_bogus(
            query, version, user_agent[self.__index[version]], timestamp)


# class XBogus:
#     """代码参考: https://github.com/B1gM8c/X-Bogus/blob/main/X-Bogus.js"""
#
#     def __init__(self, pc_js=None, app_path=None):
#         self.pc_path = Path(pc_js or "./static/js/X-Bogus.js")
#         self.pc_file = self.pc_path.open()
#         self.pc_js = compile(self.pc_file.read())
#         self.app_path = Path(app_path or "")
#         self.app_file = None
#         self.app_js = None
#
#     @run_time
#     def get_x_bogus(self, query: dict, user_agent: str, platform="PC"):
#         if platform == "PC":
#             return self.pc_js.call("sign", urlencode(query), user_agent)
#         elif platform == "APP":
#             return ""
#         raise ValueError
#
#     def close(self):
#         self.pc_file.close()


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

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188",
        }
        api = "https://ttwid.bytedance.com/ttwid/union/register/"
        data = '{"region":"cn","aid":1768,"needFid":false,"service":"www.ixigua.com","migrate_info":{"ticket":"","source":"node"},"cbUrlProtocol":"https","union":true}'
        try:
            response = post(api, data=data, headers=headers, timeout=10)
        except (exceptions.ReadTimeout, exceptions.ConnectionError):
            print("获取 ttwid 参数失败！")
            return None
        return clean(response.headers) or None


class WebID:
    @staticmethod
    def get_web_id(ua: str) -> str | None:
        headers = {"User-Agent": ua}
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


class VerifyFp:
    """代码参考: https://github.com/Johnserf-Seed/TikTokDownload/blob/main/Util/Cookies.py"""

    @staticmethod
    def get_verify_fp():
        e = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        t = len(e)
        milliseconds = int(round(time() * 1000))
        base36 = ''
        while milliseconds > 0:
            remainder = milliseconds % 36
            if remainder < 10:
                base36 = str(remainder) + base36
            else:
                base36 = chr(ord('a') + remainder - 10) + base36
            milliseconds //= 36
        r = base36
        o = [''] * 36
        o[8] = o[13] = o[18] = o[23] = '_'
        o[14] = '4'

        for i in range(36):
            if not o[i]:
                n = 0 or int(random() * t)
                if i == 19:
                    n = 3 & n | 8
                o[i] = e[n]
        return f"verify_{r}_" + ''.join(o)


class SVWebId:
    """代码参考: https://github.com/Johnserf-Seed/TikTokDownload/blob/main/Util/algorithm/s_v_web_id.py"""

    @staticmethod
    def generate_s_v_web_id():
        e = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
        t = len(e)
        n = SVWebId.base36_encode(int(time() * 1000))

        r = [''] * 36
        r[8] = r[13] = r[18] = r[23] = "_"
        r[14] = "4"

        for i in range(36):
            if not r[i]:
                o = int(random() * t)
                r[i] = e[3 & o | 8 if i == 19 else o]

        return f"verify_{n}_" + "".join(r)

    @staticmethod
    def base36_encode(number):
        alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
        base36 = []

        while number:
            number, i = divmod(number, 36)
            base36.append(alphabet[i])

        return ''.join(reversed(base36))


if __name__ == "__main__":
    # params = {
    #     "device_platform": "webapp",
    #     "aid": "6383",
    #     "channel": "channel_pc_web",
    #     "pc_client_type": "1",
    # }
    # example = XBogus("../static/js/X-Bogus.js")
    # print("X-Bogus", example.get_x_bogus(params, HEADERS["User-Agent"]))
    # example.close()
    # print(MsToken.get_ms_token())
    # print(TtWid.get_tt_wid())
    # print("webid", WebID.get_web_id(
    #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188"))
    # print(NewXBogus().get_x_bogus(params, ((86,
    #                                         138),
    #                                        (238,
    #                                         238,
    #                                         )), 23))
    print(VerifyFp.get_verify_fp())
    print(SVWebId.generate_s_v_web_id())
