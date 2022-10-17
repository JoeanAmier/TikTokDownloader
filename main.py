from Configuration import Settings
from DataAcquirer import UserData
from DataDownloader import Download
from Recorder import Record


class TikTok:
    def __init__(self):
        self.request = UserData()
        self.download = Download()
        self.settings = Settings()
        self.record = Record()

    def check_config(self):
        settings = self.settings.read_file()
        try:
            self.request.url = settings["url"]
            self.request.api = settings["mode"]
            self.download.set_rename(settings["rename"])
            self.download.music = settings["music"]
            return True
        except KeyError:
            select = input(
                "Configuration file error, whether to regenerate the configuration file? (Y/N)")
            if select == "Y":
                self.settings.delete_file()
            return False

    def batch_acquisition(self):
        pass

    def single_acquisition(self):
        pass

    def run(self):
        if not self.check_config():
            return False
        select = input("1. 批量下载用户资源\n2. 单独下载链接资源\n\n输入序号后确认进入下一步！")
        match select:
            case "1":
                self.batch_acquisition()
            case "2":
                self.single_acquisition()


def main():
    example = TikTok()
    example.run()


if __name__ == '__main__':
    main()
