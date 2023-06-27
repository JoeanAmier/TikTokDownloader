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
    Comment_Title = (
        "评论ID",
        "评论时间",
        "用户昵称",
        "IP归属地",
        "评论内容",
        "评论图片",
        "点赞数量",
        "回复数量",
        "回复ID")
    Comment_Type = (
        "CHARACTER(19) PRIMARY KEY",
        "CHARACTER(20) NOT NULL",
        "CHARACTER(20) NOT NULL",
        "CHARACTER(10) NOT NULL",
        "CHARACTER(256) NOT NULL",
        "CHARACTER(256) NOT NULL",
        "INTEGER NOT NULL",
        "INTEGER NOT NULL",
        "CHARACTER(19) NOT NULL",
    )

    def __init__(self):
        self.record = None
        self.request = None
        self.download = None
        self.settings = Settings()
        self.accounts = []  # 账号数据
        self._number = 0  # 账号数量
        self._data = {}  # 其他配置数据

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
        self._number = len(self.accounts)
        get_data(
            self._data,
            settings,
            ("root",
             "folder",
             "name",
             "time",
             "split",
             "save",
             "log"))
        get_data(
            self._data,
            settings,
            ("music",
             "cookie",
             "dynamic",
             "original",
             "proxies",
             "download"),
            True)
        print("读取配置文件成功！")
        return True

    def batch_acquisition(self):
        self.record.info(f"共有 {self._number} 个账号的作品等待下载")
        for index in range(self._number):
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
        data_root = RecordManager.run(self._data["root"])
        save_file = self.DataLogger.get(self._data["save"], NoneLogger)
        with save_file(data_root, self.download.nickname) as data:
            self.download.data = data
            self.download.run(num,
                              self.request.video_data,
                              self.request.image_data)
        self.record.info(f"账号 {self.request.name} 批量下载{type_}作品结束")
        self.download._nickname, self.request.favorite, self.download.favorite = None, None, None  # 重置数据
        return True

    def single_acquisition(self):
        data_root = RecordManager.run(self._data["root"])
        save_file = self.DataLogger.get(self._data["save"], NoneLogger)
        with save_file(data_root) as data:
            self.download.data = data
            while True:
                url = input("请输入分享链接：")
                if not url:
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

    def initialize(
            self,
            root="./",
            folder="Log",
            name="%Y-%m-%d %H.%M.%S",
            filename=None):
        self.record = LoggerManager() if self._data["log"] else BaseLogger()
        self.record.root = root  # 日志根目录
        self.record.folder = folder  # 日志文件夹名称
        self.record.name = name  # 日志文件名称格式
        self.record.run(filename=filename)
        self.request = UserData(self.record)
        self.download = Download(self.record, None)
        self.download.clean.set_rule(self.CLEAN_PATCH, True)  # 设置文本过滤规则

    def set_parameters(self):
        self.download.root = self._data["root"]
        self.download.folder = self._data["folder"]
        self.download.name = self._data["name"]
        self.download.music = self._data["music"]
        self.request.time = self._data["time"]
        self.download.time = self.request.time
        self.download.split = self._data["split"]
        self.download.cookie = self._data["cookie"]
        self.request.cookie = self._data["cookie"]
        self.download.dynamic = self._data["dynamic"]
        self.download.original = self._data["original"]
        self.request.proxies = self._data["proxies"]
        self.download.proxies = self.request.proxies
        self.download.download = self._data["download"]

    def comment_acquisition(self):
        data_root = RecordManager.run(self._data["root"], "Comment")
        save_file = self.DataLogger.get(self._data["save"], NoneLogger)
        while True:
            url = input("请输入作品链接：")
            if not url:
                break
            id_ = self.request.run_alone(url)
            if not id_:
                self.record.error(f"{url} 获取 aweme_id 失败")
                continue
            with save_file(data_root, f"作品_{id_}", file="CommentData.db", title_line=self.Comment_Title,
                           title_type=self.Comment_Type) as data:
                self.request.run_comment(id_, data)

    def run(self):
        if not self.check_config():
            return False
        self.initialize()
        self.set_parameters()
        select = input(
            "请选择下载模式：\n1. 批量下载账号作品\n2. 单独下载链接作品\n3. 获取直播推流地址\n4. 抓取作品评论数据\n输入序号：")
        """兼容旧版本的Python，版本小于3.10不支持match语法"""
        # match select:
        #     case "1":
        #         self.record.info("已选择批量下载作品模式")
        #         self.batch_acquisition()
        #     case "2":
        #         self.record.info("已选择单独下载作品模式")
        #         self.single_acquisition()
        #     case "3":
        #         self.record.info("已选择直播下载模式")
        #         self.live_acquisition()
        if select == "1":
            self.record.info("已选择批量下载作品模式")
            self.batch_acquisition()
        elif select == "2":
            self.record.info("已选择单独下载作品模式")
            self.single_acquisition()
        elif select == "3":
            self.record.info("已选择直播下载模式")
            self.live_acquisition()
        elif select == "4":
            self.record.info("已选择评论抓取模式")
            self.comment_acquisition()
        self.record.info("程序运行结束")


def main():
    """单线程版本，支持所有功能"""
    example = TikTok()
    example.run()


if __name__ == '__main__':
    main()
