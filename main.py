from Configuration import Settings
from DataAcquirer import UserData
from DataDownloader import Download
from Recorder import Logger


class TikTok:
    def __init__(self):
        self.record = None
        self.request = None
        self.download = None
        self.settings = Settings()
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
            self.record.info("读取配置文件成功")
            return True
        except KeyError as e:
            self.record.error(f"读取配置文件发生错误：{e}")
            select = input(
                "读取配置文件发生异常！是否需要重新生成默认配置文件？（Y/N）")
            if select == "Y":
                self.settings.create()
            print("程序即将关闭，请检查配置文件后再重新运行程序！")
            return False

    def batch_acquisition(self):
        if not self.request.run():
            return False
        self.record.info(f"账号({self.request.name})开始批量下载{self.type_}资源！")
        self.download.run(
            self.request.name,
            self.request.video_data,
            self.request.image_data)
        self.record.info(f"账号({self.request.name})批量下载{self.type_}资源结束！")

    def single_acquisition(self):
        while True:
            url = input("请输入分享链接：")
            if url in ("Q", "q", ""):
                break
            id_ = self.request.run_alone(url)
            if not id_:
                self.record.error(f"{url} 获取 sec_uid 失败！")
                continue
            self.record.info(f"{url} 对应的 sec_uid: {id_}")
            self.download.run_alone(id_)
            self.request.sec_uid = None

    def initialize(self, **kwargs):
        self.record = Logger()
        self.record.root = kwargs["root"]
        self.record.name = kwargs["name"]
        self.record.run()
        self.request = UserData(self.record)
        self.download = Download(self.record)

    def run(self, root="./", name="%Y-%m-%d %H.%M.%S"):
        self.initialize(root=root, name=name)
        self.record.info("程序开始运行")
        if not self.check_config():
            return False
        select = input("请选择下载模式：\n1. 批量下载用户资源\n2. 单独下载链接资源\n输入序号：")
        match select:
            case "1":
                self.record.info("已选择批量下载资源模式")
                self.batch_acquisition()
            case "2":
                self.record.info("已选择单独下载资源模式")
                self.single_acquisition()
            case "Q" | "q" | "":
                pass
            case _:
                self.record.warning(f"选择下载模式时输入了无效的内容: “{select}”")
        self.record.info("程序运行结束")


def main():
    example = TikTok()
    example.run()


if __name__ == '__main__':
    main()
