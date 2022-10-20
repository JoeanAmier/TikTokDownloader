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
            "time": "%Y-%m-%d",
            "split": "-",
            "music": False,
        }

    def create_file(self):
        with open(self.file, "w") as f:
            print("创建默认配置成功，如需修改配置，请修改“settings.json”文件后重新运行程序！")
            json.dump(self.__default, f)

    def read_file(self):
        try:
            if os.path.exists(self.file):
                with open(self.file, "r") as f:
                    return json.load(f)
            else:
                self.create_file()
                return self.__default
        except json.decoder.JSONDecodeError:
            return {}


if __name__ == "__main__":
    demo = Settings()
    print(demo.read_file())
