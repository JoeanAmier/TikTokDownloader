from Configuration import Settings
from DataAcquirer import UserData
from DataDownloader import Download
from Recorder import RunLogger

CLEAN_PATCH = {
    " ": " ",
}


class TikTok:
    def __init__(self):
        self.record = None
        self.request = None
        self.download = None
        self.settings = Settings()
        self.accounts = []  # 账号数据
        self.__number = 0  # 账号数量
        self.__data = {}  # 其他配置数据

    def check_config(self):
        settings = self.settings.read()
        try:
            self.accounts = settings["accounts"]
            self.__number = len(self.accounts)
            self.__data["root"] = settings["root"]
            self.__data["folder"] = settings["folder"]
            self.__data["name"] = settings["name"]
            self.__data["music"] = settings["music"]
            self.__data["time"] = settings["time"]
            self.__data["split"] = settings["split"]
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
        self.set_parameters()
        self.record.info(f"共有 {self.__number} 个账号的作品等待下载")
        for index in range(self.__number):
            self.account_download(index + 1, *self.accounts[index])

    def account_download(self, num: int, url: str, mode: str):
        self.request.url = url
        self.request.api = mode
        type_ = {"post": "发布页", "like": "喜欢页"}[mode]
        if not self.request.run(num):
            return False
        self.record.info(f"账号 {self.request.name} 开始批量下载{type_}作品！")
        self.download.nickname = self.request.name
        self.download.run(
            self.request.video_data,
            self.request.image_data)
        self.record.info(f"账号 {self.request.name} 批量下载{type_}作品结束！")
        self.download._nickname = None
        return True

    def single_acquisition(self):
        self.set_parameters()
        while True:
            url = input("请输入分享链接：")
            if url in ("Q", "q", ""):
                break
            id_ = self.request.run_alone(url)
            if not id_:
                self.record.error(f"{url} 获取 item_ids 失败！")
                continue
            self.download.run_alone(id_)

    def initialize(self, **kwargs):
        self.record = RunLogger()
        self.record.root = kwargs["root"]
        self.record.name = kwargs["name"]
        self.record.run()
        self.request = UserData(self.record)
        self.download = Download(self.record)
        self.download.clean.set_rule(CLEAN_PATCH, True)

    def set_parameters(self):
        self.download.root = self.__data["root"]
        self.download.folder = self.__data["folder"]
        self.download.name = self.__data["name"]
        self.download.music = self.__data["music"]
        self.download.time = self.__data["time"]
        self.download.split = self.__data["split"]

    def run(self, root="./", name="%Y-%m-%d %H.%M.%S"):
        self.initialize(root=root, name=name)
        self.record.info("程序开始运行")
        if not self.check_config():
            return False
        select = input("请选择下载模式：\n1. 批量下载用户作品源\n2. 单独下载链接作品\n输入序号：")
        match select:
            case "1":
                self.record.info("已选择批量下载作品模式")
                self.batch_acquisition()
            case "2":
                self.record.info("已选择单独下载作品模式")
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
