from contextlib import suppress
from hashlib import md5
from random import randint
from string import ascii_letters
from string import digits
from time import time

from requests import exceptions
from requests import post

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}


class XBogus:
    """代码参考: https://github.com/Johnserf-Seed/TikTokDownload/blob/main/Util/XB.py"""

    def __init__(self) -> None:

        self.Array = [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            10,
            11,
            12,
            13,
            14,
            15]
        self.character = "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe="

    def md5_str_to_array(self, md5_str):
        """
        将字符串使用md5哈希算法转换为整数数组。
        Convert a string to an array of integers using the md5 hashing algorithm.
        """
        if isinstance(md5_str, str) and len(md5_str) > 32:
            return [ord(char) for char in md5_str]
        else:
            return [
                (self.Array[ord(md5_str[idx])] << 4)
                | self.Array[ord(md5_str[idx + 1])]
                for idx in range(0, len(md5_str), 2)
            ]

    def md5_encrypt(self, url_path):
        """
        使用多轮md5哈希算法对URL路径进行加密。
        Encrypt the URL path using multiple rounds of md5 hashing.
        """
        return self.md5_str_to_array(
            self.md5(self.md5_str_to_array(self.md5(url_path)))
        )

    def md5(self, input_data):
        """
        计算输入数据的md5哈希值。
        Calculate the md5 hash value of the input data.
        """
        if isinstance(input_data, str):
            array = self.md5_str_to_array(input_data)
        elif isinstance(input_data, list):
            array = input_data
        else:
            raise ValueError("Invalid input type. Expected str or list.")

        md5_hash = md5()
        md5_hash.update(bytes(array))
        return md5_hash.hexdigest()

    @staticmethod
    def encoding_conversion(
            a,
            b,
            c,
            e,
            d,
            t,
            f,
            r,
            n,
            o,
            i,
            _,
            x,
            u,
            s,
            l,
            v,
            h,
            p):
        """
        第一次编码转换。
        Perform encoding conversion.
        """
        y = [a, int(i), *[b, _, c, x, e, u, d, s, t, l, f, v, r, h, n, p, o]]
        return bytes(y).decode('ISO-8859-1')

    @staticmethod
    def encoding_conversion2(a, b, c):
        """
        第三次编码转换。
        Perform an encoding conversion on the given input values and return the result.
        """
        return chr(a) + chr(b) + c

    @staticmethod
    def rc4_encrypt(key, data):
        """
        使用RC4算法对数据进行加密。
        Encrypt data using the RC4 algorithm.
        """
        s = list(range(256))
        j = 0
        encrypted_data = bytearray()

        # 初始化 S 盒
        # Initialize the S box
        for i in range(256):
            j = (j + s[i] + key[i % len(key)]) % 256
            s[i], s[j] = s[j], s[i]

        # 生成密文
        # Generate the ciphertext
        i = j = 0
        for byte in data:
            i = (i + 1) % 256
            j = (j + s[i]) % 256
            s[i], s[j] = s[j], s[i]
            encrypted_byte = byte ^ s[(s[i] + s[j]) % 256]
            encrypted_data.append(encrypted_byte)

        return encrypted_data

    def calculation(self, a1, a2, a3):
        """
        对给定的输入值执行位运算计算，并返回结果。
        Perform a calculation using bitwise operations on the given input values and return the result.
        """
        x1 = (a1 & 255) << 16
        x2 = (a2 & 255) << 8
        x3 = x1 | x2 | a3
        return self.character[(x3 & 16515072) >> 18] + self.character[(x3 & 258048)
                                                                      >> 12] + self.character[(x3 & 4032) >> 6] + \
            self.character[x3 & 63]

    def get_x_bogus(self, url_path):
        """
        获取 X-Bogus 值。
        Get the X-Bogus value.
        """
        array1 = self.md5_str_to_array("d88201c9344707acde7261b158656c0e")
        array2 = self.md5_str_to_array(
            self.md5(self.md5_str_to_array("d41d8cd98f00b204e9800998ecf8427e")))
        url_path_array = self.md5_encrypt(url_path)

        timer = int(time())
        ct = 536919696
        array3 = []
        array4 = []
        xb_ = ""

        new_array = [
            64,
            0.00390625,
            1,
            8,
            url_path_array[14],
            url_path_array[15],
            array2[14],
            array2[15],
            array1[14],
            array1[15],
            timer >> 24 & 255,
            timer >> 16 & 255,
            timer >> 8 & 255,
            timer & 255,
            ct >> 24 & 255,
            ct >> 16 & 255,
            ct >> 8 & 255,
            ct & 255]

        xor_result = new_array[0]
        for i in range(1, len(new_array)):
            b = new_array[i]
            if isinstance(b, float):
                b = int(b)
            xor_result ^= b

        new_array.append(xor_result)

        idx = 0
        while idx < len(new_array):
            array3.append(new_array[idx])
            with suppress(IndexError):
                array4.append(new_array[idx + 1])
            idx += 2

        merge_array = array3 + array4

        garbled_code = self.encoding_conversion2(
            2,
            255,
            self.rc4_encrypt(
                "ÿ".encode('ISO-8859-1'),
                self.encoding_conversion(
                    *
                    merge_array).encode('ISO-8859-1')).decode('ISO-8859-1'))

        idx = 0
        while idx < len(garbled_code):
            xb_ += self.calculation(ord(garbled_code[idx]), ord(
                garbled_code[idx + 1]), ord(garbled_code[idx + 2]))
            idx += 3
        return xb_


class MsToken:
    """代码参考: https://github.com/B1gM8c/X-Bogus"""

    @staticmethod
    def get_ms_token(start="msToken", size=107) -> dict:
        """
        根据传入长度产生随机字符串
        """
        base_str = f"{ascii_letters}{digits}="
        length = len(base_str) - 1
        return {start: "".join(base_str[randint(0, length)]
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
        url = "https://mcs.zijieapi.com/webid"
        data = f'{{"app_id":6383,"url":"https://www.douyin.com/","user_agent":"{ua}","referer":"https://www.douyin.com/","user_unique_id":""}}'
        try:
            response = post(url, data=data, headers=HEADERS, timeout=10)
            return response.json()["web_id"]
        except (exceptions.ReadTimeout, exceptions.ConnectionError):
            print("获取 web_id 参数失败！")
            return None
        except (exceptions.JSONDecodeError, KeyError):
            print("web_id 参数格式异常，疑似失效！")
            return None


if __name__ == "__main__":
    print(XBogus().get_x_bogus(input("输入URL: ")))
    print(MsToken.get_ms_token())
    print(TtWid.get_tt_wid())
    print(WebID.get_web_id(HEADERS["User-Agent"]))
