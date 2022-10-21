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
        self.type_ = None

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
            self.type_ = {"post": "发布页", "like": "喜欢页"}[settings["mode"]]
            return True
        except KeyError:
            select = input(
                "读取配置文件发生异常！是否需要重新生成默认配置文件？（Y/N）")
            if select == "Y":
                self.settings.create()
            print("程序即将关闭，请检查配置文件后再重新运行程序！")
            return False

    def batch_acquisition(self):
        if not self.request.run():
            return False
        print(f"账号({self.request.name})开始批量下载{self.type_}资源！")
        self.download.run(
            self.request.name,
            self.request.video_data,
            self.request.image_data)
        print(f"账号({self.request.name})批量下载{self.type_}资源结束！")

    def single_acquisition(self):
        while True:
            url = input("请输入分享链接：")
            if url in ("Q", "q"):
                break
            self.request.url = url
            id_ = self.request.run_alone()
            if not id_:
                print("获取资源信息失败！")
                continue
            self.download.run_alone(id_)

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
