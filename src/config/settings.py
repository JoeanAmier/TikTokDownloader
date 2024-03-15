from json import dump
from json import load
from json.decoder import JSONDecodeError
from platform import system
from types import SimpleNamespace
from typing import TYPE_CHECKING

from src.custom import INFO, ERROR

if TYPE_CHECKING:
    from src.tools import ColorfulConsole
    from pathlib import Path

__all__ = ["Settings"]


class Settings:
    encode = "UTF-8-SIG" if system() == "Windows" else "UTF-8"
    default = {
        "accounts_urls": [
            {"mark": "账号标识，可以设置为空字符串",
             "url": "账号主页链接",
             "tab": "账号主页类型",
             "earliest": "作品最早发布日期",
             "latest": "作品最晚发布日期"},
        ],
        "accounts_urls_tiktok": [
            {"mark": "账号标识，可以设置为空字符串",
             "url": "账号主页链接",
             "tab": "账号主页类型",
             "earliest": "作品最早发布日期",
             "latest": "作品最晚发布日期"},
        ],
        "mix_urls": [
            {"mark": "合集标识，可以设置为空字符串",
             "url": "合集链接或者作品链接"},
        ],
        "mix_urls_tiktok": [
            {"mark": "合集标识，可以设置为空字符串",
             "url": "合集链接或者作品链接"},
        ],
        "owner_url": {"mark": "账号标识，可以设置为空字符串",
                      "url": "账号主页链接", },
        "owner_url_tiktok": None,
        "root": "",
        "folder_name": "Download",
        "name_format": "create_time type nickname desc",
        "date_format": "%Y-%m-%d %H:%M:%S",
        "split": "-",
        "folder_mode": False,
        "music": False,
        "storage_format": "",
        "cookie": "",
        "cookie_tiktok": "",
        "dynamic_cover": False,
        "original_cover": False,
        "proxies": "",
        "proxies_tiktok": "",
        "download": True,
        "max_size": 0,
        "chunk": 1024 * 1024,  # 每次从服务器接收的数据块大小
        "max_retry": 5,  # 重试最大次数
        "max_pages": 0,
        "default_mode": "",
        "ffmpeg": "",
    }  # 默认配置

    def __init__(self, root: "Path", console: "ColorfulConsole"):
        self.file = root.joinpath("./settings.json")  # 配置文件
        self.console = console

    def __create(self) -> dict:
        """创建默认配置文件"""
        with self.file.open("w", encoding=self.encode) as f:
            dump(self.default, f, indent=4, ensure_ascii=False)
        self.console.print(
            "创建默认配置文件 settings.json 成功！\n请参考项目文档的快速入门部分，设置 Cookie 后重新运行程序！\n建议根据实际使用需求"
            "修改配置文件 settings.json！\n")
        return self.default

    def read(self) -> dict:
        """读取配置文件，如果没有配置文件，则生成配置文件"""
        try:
            if self.file.exists():
                with self.file.open("r", encoding=self.encode) as f:
                    return self.__check(load(f))
            return self.__create()  # 生成的默认配置文件必须设置 cookie 才可以正常运行
        except JSONDecodeError:
            self.console.print(
                "配置文件 settings.json 格式错误，请检查 JSON 格式！",
                style=ERROR)
            return self.default  # 读取配置文件发生错误时返回空配置

    def __check(self, data: dict) -> dict:
        default_keys = self.default.keys()
        data_keys = set(data.keys())
        if not (miss := default_keys - data_keys):
            return data
        if self.console.input(f"[{ERROR}]配置文件 settings.json 缺少 {"、".join(
                i for i in miss)} 参数，是否需要生成默认配置文件(YES/NO): [/{ERROR}]").upper() == "YES":
            self.__create()
        self.console.print("本次运行将会使用各项参数默认值，程序功能可能无法正常使用！")
        return self.default

    def update(self, settings: dict | SimpleNamespace):
        """更新配置文件"""
        with self.file.open("w", encoding=self.encode) as f:
            dump(
                settings if isinstance(
                    settings,
                    dict) else vars(settings),
                f,
                indent=4,
                ensure_ascii=False)
        self.console.print("保存配置成功！", style=INFO)
