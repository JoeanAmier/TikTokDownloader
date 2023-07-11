from time import time

from src.Configuration import Settings
from src.DataAcquirer import UserData
from src.DataDownloader import Download
from src.FileManager import Cache
from src.Recorder import BaseLogger
from src.Recorder import LoggerManager
from src.Recorder import RecordManager


def prompt(tip: str, choose: tuple | list, start=1) -> str:
    screen = f"{tip}:\n"
    for i, j in enumerate(choose):
        screen += f"{i + start}. {j}\n"
    return input(screen)


class TikTok:
    CLEAN_PATCH = {
        " ": " ",
    }  # 过滤字符

    def __init__(self):
        self.logger = None
        self.request = None
        self.download = None
        self.manager = None
        self.record = RecordManager()
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
             "log",
             "retry",))
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
        mark = "mark" in self._data["name"]
        self.manager = Cache(
            self.logger,
            self._data["root"],
            type_="UID",
            mark=mark)
        self.logger.info(f"共有 {self._number} 个账号的作品等待下载")
        save, root, params = self.record.run(
            self._data["root"], format_=self._data["save"])
        for index in range(self._number):
            if not self.account_download(
                    index + 1,
                    *self.accounts[index],
                    save,
                    root,
                    params):
                break

    def account_download(
            self,
            num: int,
            mark: str,
            url: str,
            mode: str,
            earliest: str,
            latest: str, save, root: str, params: dict):
        self.request.mark = mark
        self.request.url = url
        self.request.api = mode
        self.request.earliest = earliest
        self.request.latest = latest
        if not self.request.run(f"第 {num} 个"):
            return False
        old_mark = m["mark"] if (
            m := self.manager.cache.get(
                self.request.uid.lstrip("UID"))) else None
        self.manager.update_cache(
            self.request.uid.lstrip("UID"),
            self.request.mark,
            self.request.name)
        self.download.nickname = self.request.name
        self.download.uid = self.request.uid
        self.download.mark = self.request.mark
        self.download.favorite = self.request.favorite
        with save(root, name=f"{self.download.uid}_{self.download.mark}", old=old_mark, **params) as data:
            self.download.data = data
            self.download.run(f"第 {num} 个",
                              self.request.video_data,
                              self.request.image_data)
        return True

    def single_acquisition(self):
        save, root, params = self.record.run(
            self._data["root"], format_=self._data["save"])
        with save(root, **params) as data:
            self.download.data = data
            while True:
                url = input("请输入分享链接：")
                if not url:
                    break
                ids = self.request.run_alone(url)
                if not ids:
                    self.logger.error(f"{url} 获取作品ID失败")
                    continue
                self.download.tiktok = self.request.tiktok
                for i in ids:
                    self.download.run_alone(i)

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

        self.request.headers['referer'] = "https://live.douyin.com"
        while True:
            link = input("请输入直播链接：")
            if not link:
                break
            ids = self.request.return_live_ids(link)
            if not ids:
                continue
            for i in ids:
                if not (data := self.request.get_live_data(i)):
                    self.logger.warning("获取直播数据失败")
                    continue
                if not (data := self.request.deal_live_data(data)):
                    continue
                self.logger.info(f"主播昵称: {data[0]}")
                self.logger.info(f"直播标题: {data[1]}")
                self.logger.info(
                    "推流地址: \n" + "\n".join([f"清晰度{i}: {j}" for i, j in data[2].items()]))
                if len(ids) == 1 and (l := choice_quality(data[2])):
                    self.download.download_live(l, f"{data[0]}-{data[1]}")
                    break

    def initialize(
            self,
            root="./",
            folder="Log",
            name="%Y-%m-%d %H.%M.%S",
            filename=None,
    ):
        self.logger = LoggerManager() if self._data["log"] else BaseLogger()
        self.logger.root = root  # 日志根目录
        self.logger.folder = folder  # 日志文件夹名称
        self.logger.name = name  # 日志文件名称格式
        self.logger.run(filename=filename)
        self.request = UserData(self.logger)
        self.download = Download(self.logger, None)
        self.request.clean.set_rule(self.CLEAN_PATCH, True)  # 设置文本过滤规则
        self.download.clean.set_rule(self.CLEAN_PATCH, True)  # 设置文本过滤规则
        self.request.set_web_id()
        self.download.set_web_id()

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
        self.request.retry = self._data["retry"]
        self.download.retry = self._data["retry"]

    def comment_acquisition(self):
        save, root, params = self.record.run(
            self._data["root"], type_="comment", format_=self._data["save"])
        while True:
            url = input("请输入作品链接：")
            if not url:
                break
            ids = self.request.run_alone(url)
            if not ids:
                self.logger.error(f"{url} 获取作品ID失败")
                continue
            for i in ids:
                with save(root, name=f"作品评论_{i}", **params) as data:
                    self.request.run_comment(i, data)

    def mix_acquisition(self):
        mark = "mark" in self._data["name"]
        self.manager = Cache(
            self.logger,
            self._data["root"],
            type_="MIX",
            mark=mark)
        save, root, params = self.record.run(
            self._data["root"], type_="mix", format_=self._data["save"])
        while True:
            url = input("请输入合集作品链接：")
            if not url:
                break
            ids = self.request.run_alone(url)
            if not ids:
                self.logger.error(f"{url} 获取作品ID失败")
                continue
            for i in ids:
                mix_data = self.download.get_data(i)
                mix_info = self.request.run_mix(mix_data)
                if not isinstance(mix_info, list):
                    self.logger.info(f"作品 {i} 不属于任何合集")
                    continue
                mix_info[1] = input(
                    "请输入合集标识(直接回车使用合集标题作为合集标识): ") or mix_info[1]
                self.download.nickname = mix_info[2]
                self.download.mark = mix_info[1]
                old_mark = m["mark"] if (
                    m := self.manager.cache.get(
                        mix_info[0])) else None
                self.manager.update_cache(*mix_info)
                with save(root, name=f"MIX{mix_info[0]}_{mix_info[1]}", old=old_mark, **params) as data:
                    self.download.data = data
                    self.download.run_mix(
                        f"MIX{mix_info[0]}_{mix_info[1]}",
                        self.request.mix_total)

    def accounts_user(self):
        save, root, params = self.record.run(
            self._data["root"], type_="user", format_=self._data["save"])
        for i in self.accounts:
            self.request.url = i[1]
            self.logger.info(f"{i[1]} 开始获取账号数据")
            data = self.request.run_user()
            if not data:
                self.logger.warning(f"{i[1]} 获取账号数据失败")
                continue
            with save(root, name="UserData", **params) as file:
                self.request.save_user(file, data)

    def alone_user(self):
        save, root, params = self.record.run(
            self._data["root"], type_="user", format_=self._data["save"])
        while True:
            url = input("请输入账号链接: ")
            if not url:
                break
            ids = self.request.run_alone(url, user=True)
            if not ids:
                continue
            for i in ids:
                self.request.url = i
                self.logger.info(f"{i} 开始获取账号数据")
                data = self.request.run_user()
                if not data:
                    self.logger.warning(f"{i} 获取账号数据失败")
                    continue
                with save(root, name="UserData", **params) as file:
                    self.request.save_user(file, data)

    def user_acquisition(self):
        def choose_mode() -> str:
            return prompt(
                "请选择账号链接来源",
                ("使用 accounts 参数内的账号链接",
                 "手动输入待采集的账号链接"))

        if (m := choose_mode()) == "1":
            self.accounts_user()
        elif m == "2":
            self.alone_user()

    @staticmethod
    def get_condition() -> None | list:
        condition = input("请输入搜索条件:\n(关键词 类型 页数 排序规则 时间筛选)\n")
        if not condition:
            return None
        length = 5
        type_ = {
            "综合": 0,
            "视频": 1,
            "用户": 2,
            # "直播": 3,
            "0": 0,
            "1": 1,
            "2": 2,
            # "3": 3,
        }
        sort = {
            "综合排序": 0,
            "最新发布": 1,
            "最多点赞": 2,
            "0": 0,
            "1": 1,
            "2": 2,
        }

        # 分割字符串
        words = condition.split()

        # 如果列表长度小于指定长度，使用空字符串补齐
        if len(words) < length:
            words.extend([""] * (length - len(words)))
        # 如果列表长度超出指定长度，截取指定长度
        elif len(words) > length:
            words = words[:length]

        words[1] = type_.get(words[1], 0)
        words[2] = max(int(words[2] or 1), 1)
        words[3] = sort.get(words[3], 0)
        words[4] = words[4] if words[4] in ("0", "1", "7", "182") else "0"

        return words

    def search_acquisition(self):
        type_ = {
            0: "",
            1: "",
            2: "user",
        }
        self.download.download = False
        while c := self.get_condition():
            self.request.run_search(*c)
            if not self.request.search_data:
                self.logger.info("采集搜索结果失败")
                continue
            save, root, params = self.record.run(
                self._data["root"], type_=type_.get(c[1]), format_=self._data["save"])
            params["file"] = "SearchResult.db"
            with save(root, name=f"关键词_{c[0]}_{str(time())[:10]}", **params) as data:
                self.download.data = data
                print(self.request.search_data)

    def run(self):
        if not self.check_config():
            return False
        self.initialize()
        self.set_parameters()
        select = prompt("请选择下载模式", (
            "批量下载账号作品", "单独下载链接作品", "获取直播推流地址", "抓取作品评论数据", "批量下载合集作品",
            "批量提取账号数据", "采集搜索结果数据"))
        if select == "1":
            self.logger.info("已选择批量下载作品模式")
            self.batch_acquisition()
        elif select == "2":
            self.logger.info("已选择单独下载作品模式")
            self.single_acquisition()
        elif select == "3":
            self.logger.info("已选择直播下载模式")
            self.live_acquisition()
        elif select == "4":
            self.logger.info("已选择评论抓取模式")
            self.comment_acquisition()
        elif select == "5":
            self.logger.info("已选择合集下载模式")
            self.mix_acquisition()
        elif select == "6":
            self.logger.info("已选择提取账号数据模式")
            self.user_acquisition()
        elif select == "7":
            self.logger.info("已选择搜索结果采集模式")
            self.search_acquisition()
        self.logger.info("程序运行结束")
