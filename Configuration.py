import json
import os


class Settings:
    def __init__(self):
        self.file = "./settings.json"
        self.default = {
            "url": "https://v.douyin.com/XXXXXXX/",
            "mode": "post",
            "folder": "Download",
            "rename": "create_time-author-desc",
            "music": False,
        }

    def create_file(self):
        with open(self.file, "w") as f:
            json.dump(self.default, f)

    def read_file(self):
        try:
            if os.path.exists(self.file):
                with open(self.file, "r") as f:
                    self.default = json.load(f)
            else:
                self.create_file()
            return self.default
        except json.decoder.JSONDecodeError:
            return False

    def delete_file(self):
        os.remove(self.file)


if __name__ == "__main__":
    demo = Settings()
    print(demo.read_file())
