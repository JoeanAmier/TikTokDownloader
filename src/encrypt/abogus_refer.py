# path: f2/utils/abogus.py

# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description:abogus.py
@Date       :2024/06/16 11:21:14
@Author     :JohnserfSeed
@version    :0.0.1
@License    :Apache License 2.0
@Github     :https://github.com/johnserf-seed
@Mail       :johnserf-seed@foxmail.com
-------------------------------------------------
Change Log  :
2024/06/16 17:27:47 - Create ABogus algorithm & black style
2024/06/16 17:27:47 - Limit custom ua late open source full version
-------------------------------------------------
"""

import random
import time
from typing import Union, Callable, List, Dict

from gmssl import sm3, func


class StringProcessor:
    """
    StringProcessor 类用于计算ABogus算法中所需的字符串处理方法。
    包括字符串和 ASCII 码之间的转换、无符号右移运算等。

    类方法:

        to_ord_str(s: str) -> str:
            将字符串转换为 ASCII 码字符串。

        to_ord_array(s: str) -> List[int]:
            将字符串转换为 ASCII 码列表。

        to_char_str(s: str) -> str:
            将 ASCII 码列表转换为字符串。

        to_char_array(s: str) -> List[int]:
            将字符串转换为 ASCII 码列表。

        js_shift_right(val: int, n: int) -> int:
            实现 JavaScript 中的无符号右移运算。

        generate_random_bytes(length: int = 3) -> str:
            生成一组伪随机字节字符串，用于混淆数据。

    使用示例:
        # 将字符串转换为 ASCII 码字符串
        ord_str = StringProcessor.to_ord_str("Hello, World!")
        print(ord_str)

        # 将字符串转换为 ASCII 码列表
        ord_array = StringProcessor.to_ord_array("Hello, World!")
        print(ord_array)

        # 将 ASCII 码列表转换为字符串
        char_str = StringProcessor.to_char_str(ord_array)
        print(char_str)

        # 将字符串转换为 ASCII 码列表
        char_array = StringProcessor.to_char_array("Hello, World!")
        print(char_array)

        # 实现 JavaScript 中的无符号右移运算
        shifted_val = StringProcessor.js_shift_right(10, 2)
        print(shifted_val)

        # 生成一组伪随机字节字符串
        random_bytes = StringProcessor.generate_random_bytes(3)
        print(random_bytes)
    """

    @staticmethod
    def to_ord_str(s: str) -> str:
        """
        将字符串转换为 ASCII 码字符串 (Convert a string to an ASCII code string).

        Args:
            s (str): 输入字符串 (Input string).

        Returns:
            str: 转换后的 ASCII 码字符串 (Converted ASCII code string).
        """
        return "".join([chr(i) for i in s])

    @staticmethod
    def to_ord_array(s: str) -> List[int]:
        """
        将字符串转换为 ASCII 码列表 (Convert a string to a list of ASCII codes).

        Args:
            s (str): 输入字符串 (Input string).

        Returns:
            List[int]: 转换后的 ASCII 码列表 (Converted list of ASCII codes).
        """
        return [ord(char) for char in s]

    @staticmethod
    def to_char_str(s: str) -> str:
        """
        将 ASCII 码列表转换为字符串 (Convert a list of ASCII codes to a string).

        Args:
            s (str): ASCII 码列表 (List of ASCII codes).

        Returns:
            str: 转换后的字符串 (Converted string).
        """
        return "".join([chr(i) for i in s])

    @staticmethod
    def to_char_array(s: str) -> List[int]:
        """
        将字符串转换为 ASCII 码列表 (Convert a string to a list of ASCII codes).

        Args:
            s (str): 输入字符串 (Input string).

        Returns:
            List[int]: 转换后的 ASCII 码列表 (Converted list of ASCII codes).
        """
        return [ord(char) for char in s]

    @staticmethod
    def js_shift_right(val: int, n: int) -> int:
        """
        实现 JavaScript 中的无符号右移运算 (Implement the unsigned right shift operation in JavaScript).

        Args:
            val (int): 输入值 (Input value).
            n (int): 右移位数 (Number of bits to shift right).

        Returns:
            int: 右移后的值 (Value after right shift).
        """
        return (val % 0x100000000) >> n

    @staticmethod
    def generate_random_bytes(length: int = 3) -> str:
        """
        生成一组伪随机字节字符串，用于混淆数据 (Generate a pseudo-random byte string to obfuscate the data).

        Args:
            length (int): 生成的字节序列长度 (Length of the byte sequence to generate).

        Returns:
            str: 生成的伪随机字节字符串 (Generated pseudo-random byte string).
        """

        def generate_byte_sequence() -> List[str]:
            _rd = int(random.random() * 10000)
            return [
                chr(((_rd & 255) & 170) | 1),
                chr(((_rd & 255) & 85) | 2),
                chr((StringProcessor.js_shift_right(_rd, 8) & 170) | 5),
                chr((StringProcessor.js_shift_right(_rd, 8) & 85) | 40),
            ]

        result = []
        for _ in range(length):
            result.extend(generate_byte_sequence())

        return "".join(result)


class CryptoUtility:
    """
    CryptoUtility 类用于提供加密和编码的工具方法，包括 SM3 哈希、添加盐值、Base64 编码和 RC4 加密等。
    """

    def __init__(self, salt: str, custom_base64_alphabet: List[str]):
        """
        初始化 CryptoUtility 类
        Initialize the CryptoUtility class.

        Args:
            salt (str): 加密盐值 (Encryption salt).
            custom_base64_alphabet (List[str]): 自定义 Base64 字符表 (Custom Base64 alphabet).
        """
        self.salt = salt
        self.base64_alphabet = custom_base64_alphabet

        # fmt: off
        self.big_array = [
            121, 243, 55, 234, 103, 36, 47, 228, 30, 231, 106, 6, 115, 95, 78, 101, 250, 207, 198, 50,
            139, 227, 220, 105, 97, 143, 34, 28, 194, 215, 18, 100, 159, 160, 43, 8, 169, 217, 180, 120,
            247, 45, 90, 11, 27, 197, 46, 3, 84, 72, 5, 68, 62, 56, 221, 75, 144, 79, 73, 161,
            178, 81, 64, 187, 134, 117, 186, 118, 16, 241, 130, 71, 89, 147, 122, 129, 65, 40, 88, 150,
            110, 219, 199, 255, 181, 254, 48, 4, 195, 248, 208, 32, 116, 167, 69, 201, 17, 124, 125, 104,
            96, 83, 80, 127, 236, 108, 154, 126, 204, 15, 20, 135, 112, 158, 13, 1, 188, 164, 210, 237,
            222, 98, 212, 77, 253, 42, 170, 202, 26, 22, 29, 182, 251, 10, 173, 152, 58, 138, 54, 141,
            185, 33, 157, 31, 252, 132, 233, 235, 102, 196, 191, 223, 240, 148, 39, 123, 92, 82, 128, 109,
            57, 24, 38, 113, 209, 245, 2, 119, 153, 229, 189, 214, 230, 174, 232, 63, 52, 205, 86, 140,
            66, 175, 111, 171, 246, 133, 238, 193, 99, 60, 74, 91, 225, 51, 76, 37, 145, 211, 166, 151,
            213, 206, 0, 200, 244, 176, 218, 44, 184, 172, 49, 216, 93, 168, 53, 21, 183, 41, 67, 85,
            224, 155, 226, 242, 87, 177, 146, 70, 190, 12, 162, 19, 137, 114, 25, 165, 163, 192, 23, 59,
            9, 94, 179, 107, 35, 7, 142, 131, 239, 203, 149, 136, 61, 249, 14, 156
        ]
        # fmt: on

    @staticmethod
    def sm3_to_array(input_data: Union[str, List[int]]) -> List[int]:
        """
        计算请求体的 SM3 哈希值，并将结果转换为整数数组 (Calculate the SM3 hash value of the request body and convert the result to an array of integers).

        Args:
            input_data (Union[str, List[int]]): 输入数据 (Input data).

        Returns:
            List[int]: 哈希值的整数数组 (Array of integers representing the hash value).
        """
        # 如果输入是字符串，则将其编码为字节数组
        if isinstance(input_data, str):
            input_data_bytes = input_data.encode("utf-8")
        else:
            input_data_bytes = bytes(input_data)  # 将 List[int] 转换为字节数组

        # 将字节数组转换为适合 sm3.sm3_hash 函数处理的列表格式
        hex_result = sm3.sm3_hash(func.bytes_to_list(input_data_bytes))

        # 将十六进制字符串结果转换为十进制整数列表
        return [int(hex_result[i: i + 2], 16)
                for i in range(0, len(hex_result), 2)]

    def add_salt(self, param: str) -> str:
        """
        为字符串参数添加盐值 (Add salt to the string parameter).

        Args:
            param (str): 输入字符串 (Input string).

        Returns:
            str: 添加盐值后的字符串 (String with added salt).
        """
        return param + self.salt

    def process_param(
            self, param: Union[str, List[int]], add_salt: bool
    ) -> Union[str, List[int]]:
        """
        处理输入参数，根据需要添加盐值 (Process input parameter and add salt if needed).

        Args:
            param (Union[str, List[int]]): 输入参数 (Input parameter).
            add_salt (bool): 是否添加盐值 (Whether to add salt).

        Returns:
            Union[str, List[int]]: 处理后的参数 (Processed parameter).
        """
        if isinstance(param, str) and add_salt:
            param = self.add_salt(param)
        return param

    def params_to_array(
            self, param: Union[str, List[int]], add_salt: bool = True
    ) -> List[int]:
        """
        获取输入参数的哈希数组 (Get the hash array of the input parameter).

        Args:
            param (Union[str, List[int]]): 输入参数 (Input parameter).
            add_salt (bool): 是否添加盐值 (Whether to add salt).

        Returns:
            List[int]: 哈希数组 (Hash array).
        """
        processed_param = self.process_param(param, add_salt)
        return self.sm3_to_array(processed_param)

    def transform_bytes(self, bytes_list: List[int]) -> str:
        """
        对输入的字节列表进行加密/解密操作，返回处理后的字符串 (Encrypt/decrypt the input byte list and return the processed string).

        Args:
            bytes_list (List[int]): 输入的字节列表 (Input byte list).

        Returns:
            str: 处理后的字符串 (Processed string).
        """
        # 将字节列表转换为字符字符串
        bytes_str = StringProcessor.to_char_str(bytes_list)
        result_str = []
        index_b = self.big_array[1]
        initial_value = 0

        for index, char in enumerate(bytes_str):
            if index == 0:
                initial_value = self.big_array[index_b]
                sum_initial = index_b + initial_value

                self.big_array[1] = initial_value
                self.big_array[index_b] = index_b
            else:
                sum_initial = initial_value + value_e

            char_value = ord(char)
            sum_initial %= len(self.big_array)
            value_f = self.big_array[sum_initial]
            encrypted_char = char_value ^ value_f
            result_str.append(chr(encrypted_char))

            # 交换数组元素
            value_e = self.big_array[(index + 2) % len(self.big_array)]
            sum_initial = (index_b + value_e) % len(self.big_array)
            initial_value = self.big_array[sum_initial]
            self.big_array[sum_initial] = self.big_array[
                (index + 2) % len(self.big_array)
                ]
            self.big_array[(index + 2) % len(self.big_array)] = initial_value
            index_b = sum_initial

        return "".join(result_str)

    def base64_encode(
            self,
            input_string: str,
            selected_alphabet: int = 0) -> str:
        """
        使用自定义字符表对输入字符串进行 Base64 编码 (Encode the input string using a custom Base64 alphabet).

        Args:
            input_string (str): 输入字符串 (Input string).
            selected_alphabet (int): 选择的自定义 Base64 字符表索引 (Selected custom Base64 alphabet index).

        Returns:
            str: 编码后的字符串 (Encoded string).
        """

        # 将输入字符串转换为ASCII码的二进制形式
        binary_string = "".join(["{:08b}".format(ord(char))
                                 for char in input_string])

        # 补全二进制字符串使其长度为6的倍数
        padding_length = (6 - len(binary_string) % 6) % 6
        binary_string += "0" * padding_length

        # 将二进制字符串分割为6位一组
        base64_indices = [int(binary_string[i: i + 6], 2)
                          for i in range(0, len(binary_string), 6)]

        # 根据自定义字符表生成输出字符串
        output_string = "".join(
            [self.base64_alphabet[selected_alphabet][index] for index in base64_indices]
        )

        # 添加等号填充，使符合 Base64 编码规范
        output_string += "=" * (padding_length // 2)

        return output_string

    def abogus_encode(
            self,
            abogus_bytes_str: str,
            selected_alphabet: int) -> str:
        """
        对输入的字节字符串进行自定义 Base64 编码，并添加位移和填充 (Encode the input byte string using a custom Base64 alphabet, and add shifts and padding).

        Args:
            abogus_bytes_str (str): 输入的字节字符串 (Input byte string).
            selected_alphabet (int): 选择的自定义 Base64 字符表索引 (Selected custom Base64 alphabet index).

        Returns:
            str: 编码后的字符串 (Encoded string).
        """
        abogus = []

        for i in range(0, len(abogus_bytes_str), 3):
            if i + 2 < len(abogus_bytes_str):
                n = (
                        (ord(abogus_bytes_str[i]) << 16)
                        | (ord(abogus_bytes_str[i + 1]) << 8)
                        | ord(abogus_bytes_str[i + 2])
                )
            elif i + 1 < len(abogus_bytes_str):
                n = (ord(abogus_bytes_str[i]) << 16) | (
                        ord(abogus_bytes_str[i + 1]) << 8
                )
            else:
                n = ord(abogus_bytes_str[i]) << 16

            for j, k in zip(range(18, -1, -6),
                            (0xFC0000, 0x03F000, 0x0FC0, 0x3F)):
                if j == 6 and i + 1 >= len(abogus_bytes_str):
                    break
                if j == 0 and i + 2 >= len(abogus_bytes_str):
                    break
                abogus.append(
                    self.base64_alphabet[selected_alphabet][(n & k) >> j])

        abogus.append("=" * ((4 - len(abogus) % 4) % 4))
        return "".join(abogus)

    @staticmethod
    def rc4_encrypt(key: bytes, plaintext: str) -> bytes:
        """
        使用 RC4 算法加密数据 (Encrypt data using the RC4 algorithm).

        Args:
            key (bytes): 加密密钥 (Encryption key).
            plaintext (str): 明文数据 (Plaintext data).

        Returns:
            bytes: 加密后的数据 (Encrypted data).
        """
        S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]

        i = j = 0
        ciphertext = []
        for char in plaintext:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            K = S[(S[i] + S[j]) % 256]
            ciphertext.append(ord(char) ^ K)

        return bytes(ciphertext)


class BrowserFingerprintGenerator:
    """
    BrowserFingerprintGenerator 用于生成模拟的浏览器指纹信息，用于在不同浏览器环境中进行测试和数据采集。

    类属性:
        browsers (Dict[str, Callable[[], str]]): 浏览器类型和生成浏览器指纹的映射关系。

    方法:
        generate_fingerprint(browser_type="Edge"):
            根据指定的浏览器类型生成浏览器指纹。

        generate_chrome_fingerprint():
            生成 Chrome 浏览器指纹。

        generate_firefox_fingerprint():
            生成 Firefox 浏览器指纹。

        generate_safari_fingerprint():
            生成 Safari 浏览器指纹。

        generate_edge_fingerprint():
            生成 Edge 浏览器指纹。

        _generate_fingerprint(platform="Win32"):
            根据给定的参数生成浏览器指纹字符串。

    使用示例:
        chrome_fp = BrowserFingerprintGenerator.generate_fingerprint("Chrome")
        print(chrome_fp)
    """

    @classmethod
    def generate_fingerprint(cls, browser_type: str = "Edge") -> str:
        """
        根据指定的浏览器类型生成浏览器指纹。 (Generate a browser fingerprint based on the specified browser type.)

        Args:
            browser_type (str): 浏览器类型 (Browser type).

        Returns:
            str: 生成的浏览器指纹字符串 (Generated browser fingerprint string).
        """
        cls.browsers: Dict[str, Callable[[], str]] = {
            "Chrome": cls.generate_chrome_fingerprint,
            "Firefox": cls.generate_firefox_fingerprint,
            "Safari": cls.generate_safari_fingerprint,
            "Edge": cls.generate_edge_fingerprint,
        }
        return cls.browsers.get(
            browser_type,
            cls.generate_chrome_fingerprint)()

    @classmethod
    def generate_chrome_fingerprint(cls) -> str:
        return cls._generate_fingerprint(platform="Win32")

    @classmethod
    def generate_firefox_fingerprint(cls) -> str:
        return cls._generate_fingerprint(platform="Win32")

    @classmethod
    def generate_safari_fingerprint(cls) -> str:
        return cls._generate_fingerprint(platform="MacIntel")

    @classmethod
    def generate_edge_fingerprint(cls) -> str:
        return cls._generate_fingerprint(platform="Win32")

    @staticmethod
    def _generate_fingerprint(platform: str) -> str:
        """
        根据给定的参数生成浏览器指纹字符串。 (Generate a browser fingerprint string based on the given parameters.)

        Args:
            platform (str): 操作系统平台 (Operating system platform).

        Returns:
            str: 生成的浏览器指纹字符串 (Generated browser fingerprint string).
        """
        inner_width = random.randint(1024, 1920)
        inner_height = random.randint(768, 1080)
        outer_width = inner_width + random.randint(24, 32)
        outer_height = inner_height + random.randint(75, 90)
        screen_x = 0
        screen_y = random.choice([0, 30])
        avail_width = random.randint(1280, 1920)
        avail_height = random.randint(800, 1080)

        fingerprint = (
            f"{inner_width}|{inner_height}|{outer_width}|{outer_height}|"
            f"{screen_x}|{screen_y}|0|0|{avail_width}|{avail_height}|"
            f"{avail_width}|{avail_height}|{inner_width}|{inner_height}|24|24|{platform}")
        return fingerprint


class ABogus:
    """
    ABogus 类用于生成 ABogus 参数。

    类属性:
        array1 (List[int]): 加密请求体 (Encrypted request body).
        array2 (List[int]): 加密请求头 (Encrypted request header).
        array3 (List[int]): 加密 UA (Encrypted User-Agent).
        aid (int): AID 值 (AID value).
        pageId (int): 页面 ID (Page ID).
        salt (str): 加密盐值 (Encryption salt).
        options (List[int]): 请求选项 (Request options).
        ua_key (bytes): UA 加密密钥 (UA encryption key).
        character (str): 自定义 Base64 字符表 (Custom Base64 alphabet).
        character2 (str): 自定义 Base64 字符表 (Custom Base64 alphabet).
        character_list (List[str]): 自定义 Base64 字符表列表 (List of custom Base64 alphabets).
        crypto_utility (CryptoUtility): 加密工具类 (Encryption utility).
        user_agent (str): 自定义 UA (Custom User-Agent).
        browser_fp (str): 浏览器指纹 (Browser fingerprint).
        sort_index (List[int]): 排序索引 (Sort index).
        sort_index_2 (List[int]): 排序索引 (Sort index).

    方法:
        encode_data(data: str, alphabet_index: int = 0) -> str:
            使用指定的字符表对数据进行 Base64 编码 (Encode the data using the specified Base64 alphabet).

        generate_abogus(params: str, request: str = "") -> str:
            生成 ABogus 参数 (Generate the ABogus parameter).

    使用示例:
        # 生成 ABogus 参数，置空使用默认 UA 和浏览器指纹
        abogus = ABogus(user_agent="xxx", fp="xxx")
        abogus_param = abogus.generate_abogus("device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7380308675841297704……省略……")
        print(abogus_param[1])
    """

    def __init__(self, fp: str = "", user_agent: str = ""):
        self.aid = 6383
        self.pageId = 0
        self.salt = "cus"  # 加密盐
        self.array1 = []  # 加密请求体
        self.array2 = []  # 加密请求头 为空
        # fmt: off
        self.array3 = []  # 加密UA
        # fmt: on
        self.options = [0, 1, 14]  # GET, POST, JSON

        self.character = (
            "Dkdpgh2ZmsQB80/MfvV36XI1R45-WUAlEixNLwoqYTOPuzKFjJnry79HbGcaStCe"
        )
        self.character2 = (
            "ckdp1h4ZKsUB80/Mfvw36XIgR25+WQAlEi7NLboqYTOPuzmFjJnryx9HVGDaStCe"
        )
        self.character_list = [self.character, self.character2]  # 自定义base64字符表

        self.crypto_utility = CryptoUtility(
            self.salt, self.character_list
        )  # 加密工具类

        self.user_agent = (
            user_agent
            if user_agent is not None and user_agent != ""
            else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
        )  # 自定义ua，为空则设置一个默认ua

        self.browser_fp = (
            fp
            if fp is not None and fp != ""
            else BrowserFingerprintGenerator.generate_fingerprint("Edge")
        )  # 自定义浏览器指纹，为空则生成Edge指纹

        # fmt: off
        self.sort_index = [
            18, 20, 52, 26, 30, 34, 58, 38, 40, 53, 42, 21, 27, 54, 55, 31, 35, 57, 39, 41, 43, 22, 28,
            32, 60, 36, 23, 29, 33, 37, 44, 45, 59, 46, 47, 48, 49, 50, 24, 25, 65, 66, 70, 71
        ]
        self.sort_index_2 = [
            18, 20, 26, 30, 34, 38, 40, 42, 21, 27, 31, 35, 39, 41, 43, 22, 28, 32, 36, 23, 29, 33, 37,
            44, 45, 46, 47, 48, 49, 50, 24, 25, 52, 53, 54, 55, 57, 58, 59, 60, 65, 66, 70, 71
        ]
        # fmt: on

    def encode_data(self, data: str, alphabet_index: int = 0) -> str:
        """
        使用指定的字符表对数据进行 Base64 编码 (Encode the data using the specified Base64 alphabet).

        Args:
            data (str): 输入数据 (Input data).
            alphabet_index (int): 自定义字符表索引 (Custom alphabet index).

        Returns:
            str: 编码后的数据 (Encoded data).
        """
        return self.crypto_utility.abogus_encode(data, alphabet_index)

    def generate_abogus(self, params: str, request: str = "") -> tuple:
        """
        生成 abogus 参数 (Generate the ABogus parameter).

        Args:
            params (str): 请求参数 (Request parameters).
            request (str): 请求方法，不明确则为空 (Request method, empty if unclear).

        Returns:
            tuple: params 生成的 abogus 参数 和 ua (ABogus parameter generated by params and ua).
        """
        ab_dir = {
            8: 3,  # 固定
            15: {
                "aid": self.aid,
                "pageId": self.pageId,
                "boe": False,
                "ddrt": 7,
                "paths": {
                    "include": [{} for _ in range(7)],
                    "exclude": [],
                },
                "track": {"mode": 0, "delay": 300, "paths": []},
                "dump": True,
                "rpU": "",
            },
            18: 44,
            19: [1, 0, 1, 5],
            66: 0,  # 固定
            69: 0,  # 固定
            70: 0,  # 固定
            71: 0,  # 固定
        }

        # 开始加密时间
        start_encryption = int(time.time() * 1000)

        array1 = self.crypto_utility.params_to_array(
            self.crypto_utility.params_to_array(params)
        )
        array2 = self.crypto_utility.params_to_array(
            self.crypto_utility.params_to_array(request)
        )
        # fmt: off
        # 24/06/16 晚点开源自定义ua
        # 配置文件请使用该ua "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
        array3 = [
            34, 167, 211, 143, 231, 217, 33, 244,
            208, 33, 142, 226, 219, 0, 182, 214,
            50, 32, 197, 93, 75, 3, 223, 172,
            226, 95, 80, 143, 61, 49, 216, 112
        ]
        # fmt: on

        # 结束加密时间
        end_encryption = int(time.time() * 1000)

        # 插入加密开始时间
        ab_dir[20] = (start_encryption >> 24) & 255
        ab_dir[21] = (start_encryption >> 16) & 255
        ab_dir[22] = (start_encryption >> 8) & 255
        ab_dir[23] = start_encryption & 255
        ab_dir[24] = int(start_encryption / 256 / 256 / 256 / 256) >> 0
        ab_dir[25] = int(start_encryption / 256 / 256 / 256 / 256 / 256) >> 0

        # 插入请求头配置
        ab_dir[26] = (self.options[0] >> 24) & 255
        ab_dir[27] = (self.options[0] >> 16) & 255
        ab_dir[28] = (self.options[0] >> 8) & 255
        ab_dir[29] = self.options[0] & 255

        # 插入请求方法
        ab_dir[30] = int(self.options[1] / 256) & 255
        ab_dir[31] = (self.options[1] % 256) & 255
        ab_dir[32] = (self.options[1] >> 24) & 255
        ab_dir[33] = (self.options[1] >> 16) & 255

        # 插入请求头加密
        ab_dir[34] = (self.options[2] >> 24) & 255
        ab_dir[35] = (self.options[2] >> 16) & 255
        ab_dir[36] = (self.options[2] >> 8) & 255
        ab_dir[37] = self.options[2] & 255

        # 插入请求体加密
        ab_dir[38] = array1[21]
        ab_dir[39] = array1[22]
        # 插入body加密
        ab_dir[40] = array2[21]
        ab_dir[41] = array2[22]
        # 插入ua加密
        ab_dir[42] = array3[23]
        ab_dir[43] = array3[24]

        # 插入加密结束时间
        ab_dir[44] = (end_encryption >> 24) & 255
        ab_dir[45] = (end_encryption >> 16) & 255
        ab_dir[46] = (end_encryption >> 8) & 255
        ab_dir[47] = end_encryption & 255
        ab_dir[48] = ab_dir[8]
        ab_dir[49] = int(end_encryption / 256 / 256 / 256 / 256) >> 0
        ab_dir[50] = int(end_encryption / 256 / 256 / 256 / 256 / 256) >> 0

        # 插入固定值
        ab_dir[51] = (self.pageId >> 24) & 255
        ab_dir[52] = (self.pageId >> 16) & 255
        ab_dir[53] = (self.pageId >> 8) & 255
        ab_dir[54] = self.pageId & 255
        ab_dir[55] = self.pageId
        ab_dir[56] = self.aid
        ab_dir[57] = self.aid & 255
        ab_dir[58] = (self.aid >> 8) & 255
        ab_dir[59] = (self.aid >> 16) & 255
        ab_dir[60] = (self.aid >> 24) & 255

        # 插入浏览器指纹
        ab_dir[64] = len(self.browser_fp)
        ab_dir[65] = len(self.browser_fp)

        # 获取 ab_dir 中 sort_index 的值
        sorted_values = [ab_dir.get(i, 0) for i in self.sort_index]

        # 将浏览器指纹转换为 ASCII 码列表
        edge_fp_array = StringProcessor.to_char_array(self.browser_fp)

        # 将浏览器指纹长度的低 8 位作为异或值
        ab_xor = (len(self.browser_fp) & 255) >> 8 & 255

        # 进行异或计算
        for index in range(len(self.sort_index_2) - 1):
            if index == 0:
                ab_xor = ab_dir.get(self.sort_index_2[index], 0)
            ab_xor ^= ab_dir.get(self.sort_index_2[index + 1], 0)

        sorted_values.extend(edge_fp_array)
        sorted_values.append(ab_xor)

        abogus_bytes_str = (
                StringProcessor.generate_random_bytes()
                + self.crypto_utility.transform_bytes(sorted_values)
        )

        abogus = self.crypto_utility.abogus_encode(abogus_bytes_str, 0)
        params = "%s&a_bogus=%s" % (params, abogus)
        return (params, abogus, self.user_agent)


if __name__ == "__main__":
    # 24/06/16 晚点开源自定义ua
    # 配置文件请使用该ua "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
    # (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    url = "https://www.douyin.com/aweme/v1/web/aweme/detail/?"
    params = "device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7380308675841297704&update_version_code=170400&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Edge&browser_version=125.0.0.0&browser_online=true&engine_name=Blink&engine_version=125.0.0.0&os_name=Windows&os_version=10&cpu_core_num=12&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7376294349792396827"
    request = "GET"

    chrome_fp = BrowserFingerprintGenerator.generate_fingerprint("Chrome")
    abogus = ABogus(user_agent=user_agent, fp=chrome_fp)
    print(abogus.generate_abogus(params=params, request=request))

    # # 测试生成100个abogus参数 和 100个指纹所需时间
    # start = time.time()
    # for _ in range(100):
    #     abogus.generate_abogus(params=params, request=request)
    # end = time.time()
    # print("生成100个abogus参数和指纹所需时间:", end - start)  # 生成100个abogus参数和指纹所需时间:
    # 2.203000783920288

    # start = time.time()
    # for _ in range(100):
    #     BrowserFingerprintGenerator.generate_fingerprint("Chrome")
    # end = time.time()
    # print("生成100个指纹所需时间:", end - start)  # 生成100个指纹所需时间: 0.00400090217590332
