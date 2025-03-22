from base64 import b64encode
from hashlib import md5
from time import time
from urllib.parse import quote, urlencode

from ..custom import USERAGENT

__all__ = ["XBogus", "XBogusTikTok"]


class XBogus:
    __string = "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe="
    __array = (
        [None for _ in range(48)]
        + list(range(10))
        + [None for _ in range(39)]
        + list(range(10, 16))
    )
    __canvas = 3873194319

    @staticmethod
    def disturb_array(a, b, e, d, c, f, t, n, o, i, r, _, x, u, s, l, v, h, g):
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
    def generate_garbled_1(a, b, e, d, c, f, t, n, o, i, r, _, x, u, s, l, v, h, g):
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

    @staticmethod
    def handle_ua(a, b):
        d = list(range(256))
        c = 0
        result = bytearray(len(b))

        for i in range(256):
            c = (c + d[i] + ord(a[i % len(a)])) % 256
            d[i], d[c] = d[c], d[i]

        t = 0
        c = 0

        for i in range(len(b)):
            t = (t + 1) % 256
            c = (c + d[t]) % 256
            d[t], d[c] = d[c], d[t]
            result[i] = b[i] ^ d[(d[t] + d[c]) % 256]

        return result

    def generate_ua_array(self, user_agent: str, params: int) -> list:
        ua_key = ["\u0000", "\u0001", chr(params)]
        value = self.handle_ua(ua_key, user_agent.encode("utf-8"))
        value = b64encode(value)
        return list(md5(value).digest())

    def generate_x_bogus(
        self, query: list, params: int, user_agent: str, timestamp: int
    ):
        ua_array = self.generate_ua_array(user_agent, params)
        array = [
            64,
            0.00390625,
            1,
            params,
            query[-2],
            query[-1],
            69,
            63,
            ua_array[-2],
            ua_array[-1],
            timestamp >> 24 & 255,
            timestamp >> 16 & 255,
            timestamp >> 8 & 255,
            timestamp >> 0 & 255,
            self.__canvas >> 24 & 255,
            self.__canvas >> 16 & 255,
            self.__canvas >> 8 & 255,
            self.__canvas >> 0 & 255,
            None,
        ]
        zero = 0
        for i in array[:-1]:
            if isinstance(i, float):
                i = int(i)
            zero ^= i
        array[-1] = zero
        garbled = self.generate_garbled_1(*self.disturb_array(*array))
        garbled = self.generate_garbled_2(2, 255, self.generate_garbled_3("ÿ", garbled))
        return "".join(self.generate_str(i) for i in self.generate_num(garbled))

    def get_x_bogus(
        self, query: dict | str, params=8, user_agent=USERAGENT, test_time=None
    ):
        timestamp = int(test_time or time())
        query = self.process_url_path(
            urlencode(query, quote_via=quote) if isinstance(query, dict) else query
        )
        return self.generate_x_bogus(query, params, user_agent, timestamp)


class XBogusTikTok(XBogus):
    pass
