import json
from pathlib import Path


class Settings:
    def __init__(self):
        self.file = Path("./settings.json")  # 配置文件
        self.__default = {
            "accounts": [
                ["账号标识，可以设置为空字符串",
                 "账号主页链接",
                 "账号主页类型",
                 "作品最早发布日期",
                 "作品最晚发布日期"],
            ],
            "mix": [
                ["合集标识，可以设置为空字符串", "合集链接或者作品链接"],
            ],
            "root": "./",
            "folder": "Download",
            "name": "create_time nickname desc",
            "time": "%Y-%m-%d %H.%M.%S",
            "split": "-",
            "music": False,
            "save": "",
            "cookie": None,
            "dynamic": False,
            "original": False,
            "proxies": "",
            "log": False,
            "download": True,
            "max_size": 0,
            "chunk": 512 * 1024,  # 每次从服务器接收的数据块大小
            "retry": 10,  # 重试最大次数
            "pages": 0,
            "thread": False,
        }  # 默认配置

    def create(self):
        """创建默认配置文件"""
        with self.file.open("w", encoding="UTF-8") as f:
            json.dump(self.__default, f, indent=4)
        print("创建默认配置文件成功！")

    def read(self):
        """读取配置文件，如果没有配置文件，则生成配置文件"""
        try:
            if self.file.exists():
                with self.file.open("r", encoding="UTF-8") as f:
                    return json.load(f)
            else:
                print("配置文件读取失败，文件不存在！")
                self.create()
                return False  # 生成的默认配置文件必须要设置 cookie 才可以正常运行
        except json.decoder.JSONDecodeError:
            return {}  # 读取配置文件发生错误时返回空配置

    def update(self, settings: dict):
        """更新配置文件"""
        with self.file.open("w", encoding="UTF-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        print("保存配置成功！")
