from hashlib import md5
from json import dumps
from random import randint
from random import random
from string import ascii_letters
from string import digits
from time import time
from urllib.parse import urlencode

from requests import exceptions
from requests import post
from rich import print

from src.custom import ERROR

__all__ = ['Headers', 'XBogus', 'MsToken', 'TtWid', 'VerifyFp']
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                  "120.0.0.0 Safari/537.36 Edg/120.0.0.0"}
RETRY = 3


def retry(function):
    def inner(*args, **kwargs):
        if r := function(*args, **kwargs):
            return r
        for _ in range(RETRY):
            if r := function(*args, **kwargs):
                return r
        return r

    return inner


@retry
def send_request(url: str, headers: dict, data: str):
    try:
        return post(url, data=data, timeout=10, headers=headers)
    except (
            exceptions.ProxyError,
            exceptions.SSLError,
            exceptions.ChunkedEncodingError,
            exceptions.ConnectionError,
            exceptions.ReadTimeout,
    ):
        return False


class Headers:
    USER_AGENT = (
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
            "/115.0.0.0 Safari/537.36 Edg/115.0.1901.183",
            ((86,
              138),
             (238,
              238,
              ),
             )),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
            "/114.0.0.0 Safari/537.36",
            ((42,
              110),
             (95,
              187),
             )),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
            "/115.0.0.0 Safari/537.36",
            ((115,
              235,
              ),
             (151,
              95),
             )),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
            "/115.0.0.0 Safari/537.36 Edg/115.0.1901.188",
            ((155,
              54),
             (11,
              101))),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
            "/114.0.0.0 Safari/537.36 Edg/114.0.1788.0",
            ((56,
              22),
             (77,
              86)),
        ),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
            "/114.0.0.0 Safari/537.36 Edg/114.0.0.0",
            ((116,
              247),
             (11,
              146))),
        (
            "Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
            "/113.0.5666.197 Safari/537.36",
            ((244,
              163),
             (18,
              102))),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
            "/113.0.0.0 Safari/537.36",
            ((107,
              91),
             (236,
              31))),
    )

    @staticmethod
    def generate_user_agent() -> tuple[str, tuple]:
        return Headers.USER_AGENT[randint(0, len(Headers.USER_AGENT) - 1)]


def run_time(function):
    def inner(self, *args, **kwargs):
        start = time()
        result = function(self, *args, **kwargs)
        print(f"{function.__name__}运行耗时: {time() - start}s")
        return result

    return inner


class XBogus:
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


class MsToken:
    """代码参考: https://github.com/Johnserf-Seed/f2/blob/main/f2/apps/douyin/utils.py"""
    HEADERS = HEADERS | {"Content-Type": "text/plain;charset=UTF-8"}
    API = "https://mssdk.bytedance.com/web/report"
    DATA = {
        "magic": 538969122,
        "version": 1,
        "dataType": 8,
        "strData": "ffCJfaRnsiaCC7Z1m27OlyfKMI4ndizyh4Z3LVK3nsH/UTJxAaH0T0rKODVorSPVikYLqq7kEsFuK1csceuUdpnQuefocHNU"
                   "sd2dFd1v6ivDLqYX8bHsqeUKtymNpWSLly6vtMmFJNt/RSt9jNtPwVudNryDE25R5fzN+QKbqL0NeKl7e+U2GJnnsXQ4dwV4"
                   "o8rTkBgPWBrTpdaulo8t9Pcy/iq10lQaJdZ5BhuEQHwmfxZRa+aYeMa5qvgL+8Ec6QYRAS3nk6wPd1KBmUyP9saCEAFFd+y5"
                   "Wgs6JZgsr92gSdniu6/zTdhKdvv889JQMFVSPlKoVL6lTv8ms7Dpz0VuOdsM85Xl3NrL1U/XonP892COp4soTe1d7+ROWesR"
                   "kOzUV1A+6fbi2zHofJGGPe7RCK2GpC8ztsaxA9X7Ib33SLZkbtLoYLcX7osQpNvORVxXc8WcZ8ULD4k+WdPLfGHTs56N06Kr"
                   "qjNy3HsalyWD8vqVnR+g7DtmCXnYlkyLNCXZtSiIrSju0RJStaNZ0QCLykxsUPFcqsZcI7f5scbNgNlVWnXCRep7+dSjcRMr"
                   "t1nKacLpditv+HzjYXGJPmJnf8m288ljPU93uF1pOF5ciRt4TccPTCmxpbokhhkziJGCXafEvGsWsvbY9lkbXh+UDTnUBri1"
                   "WF2gHJwkOG7EDMBT9tI6UbAkS7l/dhb0tCQLETwfAa12oPu2KmhePes5pa0ZF6KlqfS+7Q1Yoy/Pm2O39q+Dl4M0oGXEcdeO"
                   "2N543Tqm6OMNr1oPizzLa6SJ88c0WTJXrvcXOedHw82FJI3fvKyP9UPP+i7Ya7bLzSdt8jPn4BkpxgUbzg5q7kV99qImwIkh"
                   "UKeksM7mA9rQxmfE9+mrsOF9+JMeA5rGNJgLe+OgyAQsw8MhACUmhOrF1NCV8CKLlKMKGDpKPbbMPbC6L9dRQgV+ebUTUBzq"
                   "Qnju/W9S/Oq8yh3rn7cpS/XKJr6gr17VyME/uGVA46ZY3c/czc3FCe6eomYTeslQLVxyv1N5RITmXPDPDkuiAlK/USA/ryXH"
                   "31FZ1XuYRkVZJpDP8MU7wRGL0GgovXLpcwj39G1oH5SiezUsha63Kqk9QkYlOvTg4hy7bFFJfHFSiHWQmv6xlhRvF326pBm3"
                   "dglRYEmeVMTZcZvCkRR42dgwxGL3rwTK7OlWQouc2mqerXV7XkIqzFJhkKM/laGbqUC8VhV0B/ywf+sm/4+u+5tqeU5eelX1"
                   "wlTKv1gWwys+KQUPNiwL8ZFoh6oUP7INHb1Kg1O5S/JnqHK1Z8J+JvVlnCeu6WSnB1AW4jpGmBzeeEpdsa9t0hwBMtMtt8JY"
                   "8Jt/QmNUTmqQnSgaQFeOSD/DdgtRWNGxq/M6mOA+eIj6Y+aFmldMGn+8Ar4YCeadwtQF0iPbRSmfzOg+3u4lI0lB1z3PRirT"
                   "pSmBX02R6UXhL3PpDy83J9OhEtXw/1yTd9soAHgNCU6jHM3dlaUAX0tD6A98wvZ6/FEJRAxzEjFmyc2uXqNw2ivvOQ0dz+nF"
                   "5AkWZS+owpq/zTTPk7MImmU1W+Ty/GV4tVGFjwsbreSjYu5ZOR35JFgXxUk93MlVLh8JEq5SJjlGtco5YCBaqaI9SXUeNrOk"
                   "mDVbUO+Q/91PyJ/j0e41jEEvtgDLlKPaY7Dj2OBCGSYag8Xw4byUdtEzj79wZaQXUn0XsWna+EUX5zeaxOGD5nXDg3uIp42K"
                   "asi2s7iAPZE5ruFzcF38tmzO60i97i9YjrhcBg+tOR6eU/deFKI211Od9wYYmaUV82ku77csJW5nsK6I78Uh4XvJyfxGvXh3"
                   "HatoIqprpHViak3CghueF3jPAzgNa6nIHXZzmPGxe5iTK8LfFnGNRB6b9JAv8EYd3QEtgjjUKu2rQ9KXxINMjCiS7rPmbVbN"
                   "O9XqJxAFub4Q9lAWZ7TqFmAR1/0Fv9DPJ7uLMI7kib/OhV0zNHLLc69G3qyqFTrNyZtqtX03oY0ZhX13ylYp9oZsaoHla3KG"
                   "hTPnxx8zaqq7o5IOppPAlWyHMd5M1Nn+F/HegOviMaGWyHBqo6aZkC6Mjh9gL5ewO8994Xd7aEVfM3dRr30oZfGlSSMl4MVq"
                   "CqGIQkTradIBvEYXv4+2Q4MgbB1YJunNIucwUmW5qtuCh4i/OcRyhjnImjfGwJHRI+h5cBNEWa34UDa9NXNrnE7k+QzjTDXQ"
                   "lT1LPjyY9NfSiVKwOWKQMFhdmhmX7RkB300VVydgb21ZSIGu3/+8LvrKHiHi+u7H+RNXO7Cvfe9IaMyL/66x9PfA3SBEC4Uz"
                   "/j3SIBXAKSRhC0MSuFTRK3IRyRefubMQoI9Qpltulin5oc7SiOfiTC9s6ODEKMn+5DOu/yEqsQdczJqxD1YAIUeff8xzl2b3"
                   "uVQY0qV2Shzwwfp6DHTvwoqSyCxAGUEop9hR7CqsMw91CHoX0OA6/T1ZBOIm0FWAwx98hXfJv7eDGJv6uTWVUbXmf4g4/KsA"
                   "caESrhawo91AVt0NpS/GRuIAgNAsI75SM7w8ya3tKY0FszWNA8S6X2Shb+vBTDwLcBAHSUdCx/aquqStWk8/sk8nPK5NtaJO"
                   "uMJQNxAfVUDQVveb+5il8+HBv4XYVv4LPtdtMX9VUIdGmCPcvJDi2KM/eHNckhwYuA+vm0Ft9wbBXACV1rivBpXv5tqmx/X3"
                   "kqPZ0Bz6oFZ+yphD1RZEe0WFxDKPxFeeeJehDRjWmgTVkAqb3SVFMY/aY3nYUrLWtiofDr5MBBqCeRijraHM2XqXtyl2iefY"
                   "mioadXMSdaTDOEGzCuy6dbTPImIiX8jos3fK6tzVTTlwaWbb2mlfn+EcgJzRPfudOYKnnN9x/UF7gFEYbLtxgsnWl8MFDivt"
                   "6DupxBVQRGNTQ3pWAsRW3jK3xBdCOV4Q9FjVN1jRWdNx/ywhcqxYhynAjt7yOADK2j9GlVEfKjL1MwYyJYrpxKBIKczzrtl+"
                   "BAmet4+WOnygMHko9sFQnly8JxuGiOhytGoGtfBespYkMFZISJif/8D+NHKAd3TbcH3Oy2C6NU/+rWZe3riVlvrvtPTN6RVg"
                   "9ChrCsum+xobNS//sFpwvbdS0VfDd4g3efbFgILB40Y+XgdZ+jJVshHscEqr2rlK7CbVk1IYImx5Bb+NBtYqZvDdV04mszCD"
                   "dlFUdxpq06sIpYqM0kPRefdnmS4Sc8NKzEz8ZvWyxAzdSLhC65peOi31+qNtVNaqT7fXzNueAUKGPiWH7qmaKRDPT8Twf3YB"
                   "/up3vDh9Q9WD9FzUTRjF+2JMSgKko37vcs14ZzgexI+20l8DTZmOiSc2uP8v9xI4K8q3AZr+hgpJoKqCc2rYfKhE33X2Lhm8"
                   "LRRfT2QWCGr7ygI0IVq5WqaVLLZ17xRicGga8mCGz8QpKGTgXtccNcJIrXETGrDGdQzPXKo80LF4P4uf2w2yi/iXzw4DCZn4"
                   "yuKdj9pyxtWHzKUBHHc3csh7ym5Z6KkG4bzvOAxjmMx8pGffRXuD56VIahFwiAB3RlN4ngEWeoyOd2ZsyuxMfKxfJlg9IKUP"
                   "JMub5Qrq56HJqDF9ireVCJmzkGreRHd/HFYXafDHKEA6rBkeAcbS23LWZT2+47u8dfsNjcS+mrfLfemFMP9wTX1QR2mtosvF"
                   "Ipf6RkbQezIfjiyjbk8DEzU9GLxWaS2Th6esWr963c+yvMWDPHrlVRyTTTcgc/2HEuEt+CEXvJRWMq7d27kXHdZbJJZ/YVTy"
                   "65mve38FT5X1xUsvM9jSYCCmKL1u/T61CpUfBVBpvu1QR5t2IcasKH1QMw7pgu1v2sJ2VGO3JRk0UJ6aQtppnjlRfMm4wW2T"
                   "mZ94mOemIYMb5GXG/fXTGo4NKX1SO+DtnkKWP2jVK1RDVW5AGfaG+/6OsjDyf57oeW0gySAM7knXQg+r01+nzPjlWrZEstl2"
                   "as+xosFeGG0WVmVlTR6KC2xdzA6EiOENk6GzWhNa2WJAZB6HHTEuExNvUstyFxh0vldqdAXaJFpa0Q03XE1+pFWkdUEEU7Oi"
                   "qIfRZzE=",
    }

    @staticmethod
    def get_fake_ms_token(key="msToken", size=128) -> dict:
        """
        根据传入长度产生随机字符串
        """
        base_str = ascii_letters + digits
        length = len(base_str) - 1
        return {key: "".join(base_str[randint(0, length)]
                             for _ in range(size))}

    @staticmethod
    def get_real_ms_token() -> dict | None:
        if response := send_request(
                MsToken.API,
                MsToken.HEADERS,
                dumps(MsToken.DATA | {"tspFromClient": int(time() * 1000)}),
        ):
            return TtWid.extract(response.headers, "msToken")


class TtWid:
    """代码参考: https://github.com/Johnserf-Seed/f2/blob/main/f2/apps/douyin/utils.py"""
    API = "https://ttwid.bytedance.com/ttwid/union/register/"
    DATA = (
        '{"region":"cn","aid":1768,"needFid":false,"service":"www.ixigua.com","migrate_info":'
        '{"ticket":"","source":"node"},"cbUrlProtocol":"https","union":true}')

    @staticmethod
    def get_tt_wid() -> dict | None:
        if response := send_request(TtWid.API, HEADERS, TtWid.DATA):
            return TtWid.extract(response.headers, "ttwid")

    @staticmethod
    def extract(value, name: str) -> dict | None:
        if c := value.get("Set-Cookie"):
            try:
                temp = c.split("; ")[0].split("=", 1)
                return {temp[0]: temp[1]}
            except IndexError:
                print(f"[{ERROR}]获取 {name} 参数失败！[/{ERROR}]")


class WebID:
    API = "https://mcs.zijieapi.com/webid"

    @staticmethod
    def get_web_id(user_agent: str) -> str | None:
        headers = {"User-Agent": user_agent}
        data = (f'{{"app_id":6383,"url":"https://www.douyin.com/","user_agent":'
                f'"{user_agent}","referer":"https://www.douyin.com/","user_unique_id":""}}')
        try:
            if response := send_request(WebID.API, headers, data):
                return response.json().get("web_id")
            raise KeyError
        except (exceptions.JSONDecodeError, KeyError):
            print(f"[{ERROR}]获取 webid 参数失败！[/{ERROR}]")


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
    # print(VerifyFp.get_verify_fp())
    # print(SVWebId.generate_s_v_web_id())
    # print(TtWid.get_tt_wid())
    # print(MsToken.get_fake_ms_token())
    # print(MsToken.get_real_ms_token())
    print(WebID.get_web_id(HEADERS["User-Agent"]))
