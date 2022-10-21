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
        settings = self.settings.read()
        try:
            self.request.url = settings["url"]
            self.request.api = settings["mode"]
            self.download.root = settings["root"]
            self.download.folder = settings["folder"]
            self.download.name = settings["name"]
            self.download.music = settings["music"]
            self.download.time = settings["time"]
            self.download.split = settings["split"]
            return True
        except KeyError:
            select = input(
                "读取配置文件发生异常！是否需要重新生成默认配置文件？（Y/N）")
            if select == "Y":
                self.settings.create()
            print("程序即将关闭，请检查配置文件后再重新运行程序！")
            return False

    def batch_acquisition(self):
        pass

    def single_acquisition(self):
        pass

    def run(self):
        if not self.check_config():
            return False
        select = input("1. 批量下载用户资源\n2. 单独下载链接资源\n输入序号：")
        match select:
            case "1":
                self.batch_acquisition()
            case "2":
                self.single_acquisition()
        print("程序运行结束！")


def main():
    example = TikTok()
    example.run()


if __name__ == '__main__':
    main()
