import json
import os


class Settings:
    def __init__(self):
        self.file = "./settings.json"
        self.__default = {
            "url": "https://v.douyin.com/XXXXXXX/",
            "mode": "post",
            "root": "./",
            "folder": "Download",
            "name": "create_time author desc",
            "time": "%Y-%m-%d %H.%M.%S",
            "split": "-",
            "music": False,
        }

    def create(self):
        with open(self.file, "w") as f:
            json.dump(self.__default, f)
        print("创建默认配置成功，如需修改配置，请修改“settings.json”文件后重新运行程序！")

    def read(self):
        try:
            if os.path.exists(self.file):
                with open(self.file, "r") as f:
                    return json.load(f)
            else:
                self.create()
                return self.__default
        except json.decoder.JSONDecodeError:
            return {}

    def update(self, settings: dict):
        with open(self.file, "w") as f:
            json.dump(settings, f)
        print("保存配置成功！")


if __name__ == "__main__":
    demo = Settings()
    print(demo.read())
