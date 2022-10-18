import json
import os


class Settings:
    def __init__(self):
        self.file = "./settings.json"
        self.__default = {
            "url": "https://v.douyin.com/XXXXXXX/",
            "mode": "post",
            "folder": "Download",
            "name": "create_time author desc",
            "time": "%Y-%m-%d %H:%M:%S",
            "split": "-",
            "music": False,
        }

    def create_file(self):
        with open(self.file, "w") as f:
            print(
                "Create the default configuration file successfully, if you need to modify the configuration, "
                "please modify the \"settings.json\" file and run the program again!")
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
            return False

    def delete_file(self):
        os.remove(self.file)
        self.create_file()


if __name__ == "__main__":
    demo = Settings()
    print(demo.read_file())
