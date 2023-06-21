from src.Configuration import Settings
from src.DataAcquirer import UserData
from src.DataDownloader import Download
from src.Recorder import BaseLogger
from src.Recorder import CSVLogger
from src.Recorder import LoggerManager
from src.Recorder import NoneLogger
from src.Recorder import RecordManager
from src.Recorder import SQLLogger
from src.Recorder import XLSXLogger


class TikTok:
    CLEAN_PATCH = {
        " ": " ",
    }  # 过滤字符
    DataLogger = {
        "csv": CSVLogger,
        "xlsx": XLSXLogger,
        "sql": SQLLogger,
    }

    def __init__(self):
        self.record = None
        self.request = None
        self.download = None
        self.settings = Settings()
        self.accounts = []  # 账号数据
        self.__number = 0  # 账号数量
        self.__data = {}  # 其他配置数据

    def check_config(self):
        print("正在读取配置文件！")
        settings = self.settings.read()
        if not isinstance(settings, dict):
            return False
        try:
            return self.read_data(settings)
        except KeyError as e:
            print(f"读取配置文件发生错误：{e}")
            select = input(
                "配置文件存在错误！是否需要重新生成默认配置文件？（Y/N）")
            if select == "Y":
                self.settings.create()
            print("程序即将关闭，请检查配置文件后再重新运行程序！")
            return False

    def read_data(self, settings):
        def get_data(key, value, items, index=False):
            for i in items:
                key[i] = value[i][0] if index else value[i]

        self.accounts = settings["accounts"]
        self.__number = len(self.accounts)
        get_data(
            self.__data,
            settings,
            ("root",
             "folder",
             "name",
             "time",
             "split",
             "save",
             "log"))
        get_data(
            self.__data,
            settings,
            ("music",
             "cookie",
             "dynamic",
             "original",
             "proxies"),
            True)
        print("读取配置文件成功！")
        return True

    def batch_acquisition(self):
        self.set_parameters()
        self.record.info(f"共有 {self.__number} 个账号的作品等待下载")
        for index in range(self.__number):
            self.account_download(index + 1, *self.accounts[index])

    def account_download(
            self,
            num: int,
            url: str,
            mode: str,
            earliest: str,
            latest: str):
        self.request.url = url
        self.request.api = mode
        self.request.earliest = earliest
        self.request.latest = latest
        type_ = {"post": "发布页", "favorite": "喜欢页"}[mode]
        if not self.request.run(num):
            return False
        self.record.info(f"账号 {self.request.name} 开始批量下载{type_}作品")
        self.download.nickname = self.request.name
        self.download.favorite = self.request.favorite
        data_root = RecordManager.run(self.__data["root"])
        save_file = self.DataLogger.get(self.__data["save"], NoneLogger)
        with save_file(data_root, self.download.nickname) as data:
            self.download.data = data
            self.download.run(
                self.request.video_data,
                self.request.image_data)
        self.record.info(f"账号 {self.request.name} 批量下载{type_}作品结束")
        self.download._nickname, self.request.favorite, self.download.favorite = None, None, None  # 重置数据
        return True

    def single_acquisition(self):
        self.set_parameters()
        data_root = RecordManager.run(self.__data["root"])
        save_file = self.DataLogger.get(self.__data["save"], NoneLogger)
        with save_file(data_root) as data:
            self.download.data = data
            while True:
                url = input("请输入分享链接：")
                if url in ("Q", "q", ""):
                    break
                id_ = self.request.run_alone(url)
                if not id_:
                    self.record.error(f"{url} 获取 aweme_id 失败")
                    continue
                self.download.run_alone(id_)

    def live_acquisition(self):
        def choice_quality(items: dict) -> str:
            try:
                choice = int(input("请选择下载清晰度(输入对应索引，直接回车代表不下载): "))
                if not 0 <= choice < len(items):
                    raise ValueError
            except ValueError:
                return ""
            keys = list(items.keys())
            return items[keys[choice]]

        self.set_parameters()
        link = input("请输入直播链接：")
        if not (data := self.request.get_live_data(link)):
            self.record.warning("获取直播数据失败")
            return
        if not (data := self.request.deal_live_data(data)):
            return
        self.record.info(f"主播昵称: {data[0]}")
        self.record.info(f"直播名称: {data[1]}")
        self.record.info("推流地址: \n" +
                         "\n".join([f"{i}: {j}" for i, j in data[2].items()]))
        if l := choice_quality(data[2]):
            self.download.download_live(l, f"{data[0]}-{data[1]}")

    def initialize(self, root="./", folder="Log", name="%Y-%m-%d %H.%M.%S"):
        self.record = LoggerManager() if self.__data["log"] else BaseLogger()
        self.record.root = root  # 日志根目录
        self.record.folder = folder  # 日志文件夹名称
        self.record.name = name  # 日志文件名称格式
        self.record.run()
        self.request = UserData(self.record)
        self.download = Download(self.record, None)
        self.download.clean.set_rule(self.CLEAN_PATCH, True)  # 设置文本过滤规则

    def set_parameters(self):
        self.download.root = self.__data["root"]
        self.download.folder = self.__data["folder"]
        self.download.name = self.__data["name"]
        self.download.music = self.__data["music"]
        self.download.time = self.__data["time"]
        self.download.split = self.__data["split"]
        self.download.cookie = self.__data["cookie"]
        self.request.cookie = self.__data["cookie"]
        self.download.dynamic = self.__data["dynamic"]
        self.download.original = self.__data["original"]
        self.request.proxies = self.__data["proxies"]
        self.download.proxies = self.request.proxies

    def run(self):
        if not self.check_config():
            return False
        self.initialize()
        select = input(
            "请选择下载模式：\n1. 批量下载账号作品\n2. 单独下载链接作品\n3. 获取直播推流地址\n输入序号：")
        match select:
            case "1":
                self.record.info("已选择批量下载作品模式")
                self.batch_acquisition()
            case "2":
                self.record.info("已选择单独下载作品模式")
                self.single_acquisition()
            case "3":
                self.record.info("已选择直播下载模式")
                self.live_acquisition()
            case _:
                pass
        self.record.info("程序运行结束")


def main():
    example = TikTok()
    example.run()


if __name__ == '__main__':
    main()
