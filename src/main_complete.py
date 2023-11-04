from datetime import date
from time import time

from src.Customizer import (
    WARNING,
)
from src.Customizer import failed
from src.Customizer import rest
from src.DataAcquirer import (
    Link,
    Account,
    Works,
    Live,
    Comment,
    Mix,
)
from src.DataDownloader import Downloader
from src.DataExtractor import Extractor
from src.FileManager import Cache
from src.Recorder import RecordManager


def prompt(
        title: str,
        choose: tuple | list,
        console,
        separate=None) -> str:
    screen = f"{title}:\n"
    row = 0
    for i, j in enumerate(choose):
        screen += f"{i + 1}. {j}\n"
        if separate and row in separate:
            screen += f"{'=' * 25}\n"
        row += 1
    return console.input(screen)


def check_storage_format(function):
    def inner(self, *args, **kwargs):
        if self.parameter.storage_format:
            return function(self, *args, **kwargs)
        self.console.print(
            "未设置 storage_format 参数，无法正常使用该功能，详细说明请查阅项目文档！",
            style=WARNING)

    return inner


class TikTok:
    SEARCH = {
        "type": {
            "综合": 0,
            "视频": 1,
            "用户": 2,
            # "直播": 3,
            "0": 0,
            "1": 1,
            "2": 2,
            # "3": 3,
        },
        "type_text": {
            0: "综合搜索",
            1: "视频搜索",
            2: "用户搜索",
            # 3: "直播搜索",
        },
        "sort": {
            "综合排序": 0,
            "最新发布": 1,
            "最多点赞": 2,
            "0": 0,
            "1": 1,
            "2": 2,
        },
        "sort_text": {
            0: "综合排序",
            1: "最新发布",
            2: "最多点赞",
        },
        "publish_text": {
            "0": "不限",
            "1": "一天内",
            "7": "一周内",
            "182": "半年内",
        },
    }
    DATA_TYPE = {
        0: "",
        1: "",
        2: "search_user",
    }

    def __init__(self, parameter, settings):
        self.parameter = parameter
        self.console = parameter.console
        self.logger = parameter.logger
        self.links = Link(parameter)
        self.downloader = Downloader(parameter)
        self.extractor = Extractor(parameter)
        self.storage = bool(parameter.storage_format)
        self.record = RecordManager()
        self.settings = settings
        self.accounts = parameter.accounts_urls
        self.mix = parameter.mix_urls
        self.running = True
        self.cache = Cache(
            parameter,
            "mark" in parameter.name_format,
            "nickname" in parameter.name_format
        )

    def _inquire_input(self, tip: str) -> str:
        url = self.console.input(f"请输入{tip}链接: ")
        if not url:
            return ""
        elif url in ("Q", "q",):
            self.running = False
            return ""
        return url

    def account_acquisition_interactive(self):
        root, params, logger = self.record.run(self.parameter)
        select = prompt("请选择账号链接来源", ("使用 accounts_urls 参数内的账号链接(推荐)",
                                               "手动输入待采集的账号链接"), self.console)
        if select == "1":
            self.account_works_batch(root, params, logger)
        elif select == "2":
            self.account_works_inquire(root, params, logger)
        elif select.upper() == "Q":
            self.running = False
        self.logger.info("已退出批量下载账号作品模式")

    def account_works_batch(self, root, params, logger):
        self.logger.info(f"共有 {len(self.accounts)} 个账号的作品等待下载")
        for index, data in enumerate(self.accounts, start=1):
            if not (sec_user_id := self.check_sec_user_id(data.url)):
                self.logger.warning(
                    f"配置文件 accounts_urls 参数"
                    f"第 {index} 条数据的 url 无效")
                continue
            if not self.deal_account_works(
                    index,
                    **vars(data) | {"sec_user_id": sec_user_id},
                    root=root,
                    params=params,
                    logger=logger):
                if failed():
                    continue
                break
            # break  # 调试使用
            rest(index, self.console.print)

    def check_sec_user_id(self, sec_user_id: str) -> str:
        sec_user_id = self.links.user(sec_user_id)
        return sec_user_id[0] if len(sec_user_id) > 0 else ""

    def account_works_inquire(self, root, params, logger):
        while url := self._inquire_input("账号主页"):
            links = self.links.user(url)
            if not links:
                self.logger.warning(f"{url} 提取账号 sec_user_id 失败")
            for index, sec in enumerate(links, start=1):
                if not self.deal_account_works(
                        index,
                        sec_user_id=sec,
                        root=root,
                        params=params,
                        logger=logger):
                    if failed():
                        continue
                    break
                rest(index, self.console.print)

    def deal_account_works(
            self,
            num: int,
            root,
            params: dict,
            logger,
            sec_user_id: str,
            mark="",
            tab="post",
            earliest="",
            latest="",
            api=False,
            source=False,
            *args,
            **kwargs,
    ):
        self.logger.info(f"开始处理第 {num} 个账号" if num else "开始处理账号")
        acquirer = Account(self.parameter, sec_user_id, tab, earliest, latest)
        account_data, earliest, latest = acquirer.run()
        if not account_data:
            return False
        if source:
            return account_data
        return self._batch_process_works(
            root,
            params,
            logger,
            account_data,
            mark,
            tab == "post",
            api=api,
            earliest=earliest,
            latest=latest)

    def _batch_process_works(self,
                             root,
                             params: dict,
                             logger,
                             data,
                             mark,
                             post=True,
                             mix=False,
                             api=False,
                             earliest: date = None,
                             latest: date = None,
                             ):
        id_, name, mid, title, mark, data = self.extractor.preprocessing_data(
            data, mark, post, mix)
        old_mark = m["mark"] if (
            m := self.cache.data.get(
                mid if mix else id_)) else None
        with logger(root, name=f"{'MID' if mix else 'UID'}{mid if mix else id_}_{mark}", old=old_mark,
                    **params) as recorder:
            data = self.extractor.run(
                data,
                recorder,
                type_="batch",
                post=post,
                name=name,
                mark=mark,
                earliest=earliest or date(2016, 9, 20),
                latest=latest or date.today(),
                same=any((post, mix)))
        if not data:
            return False
        if api:
            return data
        self.cache.update_cache(
            self.parameter.folder_mode,
            "MID" if mix else "UID",
            mid if mix else id_,
            mark,
            title if mix else name,
        )
        self.download_account_works(
            data, id_, name, mark, post, mix, mid, title)
        return True

    def download_account_works(
            self,
            data: list[dict],
            id_: str,
            name: str,
            mark: str,
            post: bool,
            mix: bool,
            mid: str = None,
            title: str = None,
    ):
        self.downloader.run(
            data,
            "batch",
            id_=id_,
            name=name,
            mark=mark,
            addition="合集作品" if mix else "发布作品" if post else "喜欢作品",
            mid=mid,
            title=title, )

    def works_interactive(self):
        root, params, logger = self.record.run(self.parameter)
        with logger(root, **params) as record:
            while url := self._inquire_input("作品"):
                tiktok, ids = self.links.works(url)
                if not ids:
                    self.logger.warning(f"{url} 提取作品 ID 失败")
                    continue
                self.input_links_acquisition(tiktok, ids, record)
        self.logger.info("已退出批量下载链接作品模式")

    def input_links_acquisition(
            self,
            tiktok: bool,
            ids: list[str],
            record,
            api=False,
            source=False):
        works_data = [Works(self.parameter, i, tiktok).run() for i in ids]
        if not works_data:
            return False
        if source:
            return works_data
        works_data = self.extractor.run(works_data, record)
        if api:
            return works_data
        self.downloader.run(works_data, "works", tiktok=tiktok)

    def _choice_live_quality(self, items: dict) -> str:
        try:
            choice = self.console.input(
                "请选择下载清晰度(输入清晰度或者对应序号，直接回车代表不下载): ")
            if u := items.get(choice):
                return u
            if not 0 <= (i := int(choice) - 1) < len(items):
                raise ValueError
        except ValueError:
            return ""
        return list(items.values())[i]

    def live_interactive(self):
        self.console.print(
            "如果设置了已登录的 Cookie，获取直播数据时将会导致正在观看的直播中断，刷新即可恢复！", style=WARNING)
        while url := self._inquire_input("直播"):
            params = self._generate_live_params(*self.links.live(url))
            if not params:
                self.console.print(f"{url} 提取直播 ID 失败")
                continue
            live_data = [Live(self.parameter, **i).run() for i in params]
            if not live_data:
                self.console.print("获取直播数据失败")
                continue
            live_data = self.extractor.run(live_data, None, "live")
            download_tasks = self.show_live_info(live_data)
            self.downloader.run_live(download_tasks)
        self.logger.info("已退出获取直播推流地址模式")

    def _generate_live_params(self, rid: bool, ids: list[list]) -> list[dict]:
        if not ids:
            self.console.print("提取 web_rid 或者 room_id 失败！", style=WARNING)
            return []
        if rid:
            return [{"web_rid": id_} for id_ in ids]
        else:
            return [{"room_id": id_[0], "sec_user_id": id_[1]} for id_ in ids]

    def show_live_info(self, data: list[dict]) -> list[tuple]:
        download_tasks = []
        for item in data:
            self.console.print("直播标题:", item["title"])
            self.console.print("主播昵称:", item["nickname"])
            self.console.print("在线观众:", item["user_count_str"])
            self.console.print("观看次数:", item["total_user_str"])
            if item["status"] == 4:
                self.console.print("当前直播已结束！")
                continue
            self.show_live_stream_url(item, download_tasks)
        return [i for i in download_tasks if isinstance(i, tuple)]

    def show_live_stream_url(self, item: dict, tasks: list):
        for i, (k, v) in enumerate(item["stream_url"].items(), start=1):
            self.console.print(i, k, v)
        tasks.append(
            (item, u) if (
                u := self._choice_live_quality(
                    item["stream_url"])) else u)

    @check_storage_format
    def comment_interactive(self):
        root, params, logger = self.record.run(self.parameter, type_="comment")
        while url := self._inquire_input("作品"):
            tiktok, ids = self.links.works(url)
            if not ids:
                self.logger.warning(f"{url} 提取作品 ID 失败")
                continue
            elif tiktok:
                self.console.print("目前项目暂不支持采集 TikTok 作品评论数据！", style=WARNING)
                continue
            for i in ids:
                name = f"作品{i}_评论数据"
                with logger(root, name=name, **params) as record:
                    Comment(self.parameter, i).run(self.extractor, record)
                self.logger.info(f"作品评论数据已储存至 {name}")
        self.logger.info("已退出采集作品评论数据模式")

    def mix_interactive(self):
        root, params, logger = self.record.run(self.parameter, type_="mix")
        select = prompt("请选择合集链接来源", ("使用 mix_urls 参数内的合集链接(推荐)",
                                               "手动输入待采集的合集/作品链接"), self.console)
        if select == "1":
            self.mix_batch(root, params, logger)
        elif select == "2":
            self.mix_inquire(root, params, logger)
        elif select.upper() == "Q":
            self.running = False
        self.logger.info("已退出批量下载合集作品模式")

    def get_mix_info(self, id_: str, collection=False):
        data = id_ if collection else self.download.get_data(id_)
        if not data:
            self.logger.info(f"{id_} 获取合集信息失败")
            return False
        mix_info = self.request.run_mix(data)
        if not isinstance(mix_info, list):
            self.logger.info(f"{id_} 获取合集信息失败")
            return False
        return mix_info

    @staticmethod
    def _generate_mix_params(mix: bool, id_: str) -> dict:
        return {"mix_id": id_, } if mix else {"works_id": id_, }

    def download_mix(self, mix_info, save, root, params, mark=None, api=False):
        if isinstance(mark, str):
            mix_info[1] = mark or mix_info[1]
        else:
            mix_info[1] = input(
                "请输入合集标识(直接回车使用合集标题作为合集标识): ") or mix_info[1]
        self.download.nickname = mix_info[2]
        self.download.mark = mix_info[1]
        old_mark = m["mark"] if (
            m := self.manager.data.get(
                mix_info[0])) else None
        self.manager.update_cache(*mix_info)
        with save(root, name=f"MIX{mix_info[0]}_{mix_info[1]}", old=old_mark, **params) as data:
            self.download.data = data
            self.download.run_mix(
                f"MIX{mix_info[0]}_{mix_info[1]}",
                self.request.mix_total, api)

    def mix_inquire(self, root, params, logger):
        while url := self._inquire_input("合集或作品"):
            mix_id, id_ = self.links.mix(url)
            if not id_:
                self.logger.warning(f"{url} 获取作品 ID 或合集 ID 失败")
            for index, i in enumerate(id_, start=1):
                if not self._deal_mix_works(root, params, logger, mix_id, i):
                    if failed():
                        continue
                    break
                rest(index, self.console.print)

    def mix_batch(self, root, params, logger):
        for index, data in enumerate(self.mix, start=1):
            mix_id, id_ = self._check_mix_id(data.url)
            if not id_:
                self.logger.warning(f"{data.url} 获取作品 ID 或合集 ID 失败")
                continue
            if not self._deal_mix_works(
                    root,
                    params,
                    logger,
                    mix_id,
                    id_,
                    data.mark,
                    index):
                if failed():
                    continue
                break
            rest(index, self.console.print)

    def _deal_mix_works(self,
                        root,
                        params,
                        logger,
                        mix_id: bool = None,
                        id_: str = None,
                        mark: str = None,
                        num: int = 0,
                        api=False,
                        source=False, ):
        self.logger.info(f"开始处理第 {num} 个合集" if num else "开始处理合集")
        mix_params = self._generate_mix_params(mix_id, id_)
        if mix_data := Mix(self.parameter, **mix_params).run():
            return (
                mix_data
                if source
                else self._batch_process_works(
                    root, params, logger, mix_data, mark, mix=True, api=api
                )
            )
        return False

    def _check_mix_id(self, url: str) -> tuple[bool, str]:
        mix_id, id_ = self.links.mix(url)
        return (mix_id, id_[0]) if len(id_) > 0 else (mix_id, "")

    def accounts_user(self):
        save, root, params = self.record.run(
            self._data["root"], type_="user", format_=self._data["save"])
        for i in self.accounts:
            self.request.url = i[1]
            self.logger.info(f"{i[1]} 开始获取账号数据")
            data = self.request.run_batch()
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
            elif url in ("Q", "q",):
                self.quit = True
                break
            ids = self.request.run_alone(url, user=True)
            if not ids:
                continue
            for i in ids:
                self.request.url = i
                self.logger.info(f"{i} 开始获取账号数据")
                data = self.request.run_batch()
                if not data:
                    self.logger.warning(f"{i} 获取账号数据失败")
                    continue
                with save(root, name="UserData", **params) as file:
                    self.request.save_user(file, data)

    @check_storage_format
    def user_interactive(self):
        def choose_mode() -> str:
            return prompt(
                "请选择账号链接来源",
                ("使用 accounts 参数内的账号链接",
                 "手动输入待采集的账号链接"), self.colour.colorize)

        if (m := choose_mode()) == "1":
            self.accounts_user()
        elif m == "2":
            self.alone_user()
        elif m.upper() == "Q":
            self.quit = True
        self.logger.info("已退出批量采集账号数据模式")

    def get_condition(self, condition=None) -> None | tuple[list, str]:
        def extract_integer_and_compare(input_string: str) -> int:
            try:
                # 尝试将字符串转换为整数，如果转换成功，则返回比较大的数
                return max(int(input_string), 1)
            except ValueError:
                # 如果转换失败，则返回1
                return 1

        while not condition:
            condition = input("请输入搜索条件:\n(关键词 类型 页数 排序规则 时间筛选)\n")
            if not condition:
                return None
            elif condition.upper() == "Q":
                self.quit = True
                return None

        # 分割字符串
        words = condition.split()

        # 如果列表长度小于指定长度，使用空字符串补齐
        while len(words) < 5:
            words.append("")

        words[1] = self.SEARCH["type"].get(words[1], 0)
        words[2] = extract_integer_and_compare(words[2])
        words[3] = self.SEARCH["sort"].get(words[3], 0)
        words[4] = words[4] if words[4] in ("0", "1", "7", "182") else "0"

        if words[1] == 2:
            text = "_".join([self.SEARCH["type_text"][words[1]],
                             words[0]])
        else:
            text = "_".join([self.SEARCH["type_text"][words[1]],
                             self.SEARCH["sort_text"][words[3]],
                             self.SEARCH["publish_text"][words[4]],
                             words[0]])

        return words, text

    @check_storage_format
    def search_interactive(self):
        self.download.favorite = True
        self.download.download = False
        while c := self.get_condition():
            self.get_search_results(*c)
        self.download.favorite = False
        self.download.download = self._data['download']
        self.logger.info("已退出采集搜索结果数据模式")

    def get_search_results(self, works, text, api=False):
        tag = works[1]
        self.request.run_search(*works[:5])
        if not self.request.search_data:
            self.logger.info("采集搜索结果失败")
            return
        save, root, params = self.record.run(
            self._data["root"], type_=self.DATA_TYPE.get(
                tag), format_=self._data["save"])
        params["file"] = "SearchResult.db"
        name = f"{text}_{str(time())[:10]}"
        with save(root, name=name, **params) as data:
            if tag in (0, 1):
                self.deal_search_items(data, api)
            elif tag == 2:
                self.deal_search_user(data, api)
            else:
                raise ValueError
        self.logger.info(f"搜索结果数据已储存至 {name}")

    def deal_search_items(self, file, api=False):
        self.logger.info("开始提取搜索结果")
        self.download.data = file
        self.download.api_data = []
        self.download.get_info(self.request.search_data, api)
        self.logger.info("搜索结果提取结束")

    def deal_search_user(self, file, api=False):
        self.logger.info("开始提取搜索结果")
        item = self.request.deal_search_user()
        if api:
            self.download.api_data = item
        self.request.save_user(file, item, True)

    @check_storage_format
    def hot_interactive(self, api=None):
        collection_time = str(time())[:10]
        save, root, params = self.record.run(
            self._data["root"], type_="hot", format_=self._data["save"])
        for i, j in enumerate(("热榜", "娱乐榜", "社会榜", "挑战榜")):
            with save(root, name=f"HOT_{collection_time}_{j}", **params) as data:
                self.request.run_hot(i, j, data, api)
        self.logger.info(f"抖音热榜数据已储存至 HOT + {collection_time} + 榜单类型")
        self.logger.info("已退出采集抖音热榜数据模式")

    def collection_interactive(self):
        save, root, params = self.record.run(
            self._data["root"], format_=self._data["save"])
        self.request.earliest = ""
        self.request.latest = ""
        if self.request.run_collection():
            self.download_account_works(0, save, root, params, None)
        self.logger.info("已退出批量下载收藏作品模式")

    def run(self):
        while self.running:
            select = prompt(
                "请选择采集功能",
                ("批量下载账号作品",
                 "批量下载链接作品",
                 "获取直播推流地址",
                 "采集作品评论数据",
                 "批量下载合集作品",
                 "批量采集账号数据",
                 "采集搜索结果数据",
                 "采集抖音热榜数据",
                 "批量下载收藏作品"),
                self.console)
            if select in {"Q", "q"}:
                self.running = False
            elif not select:
                break
            elif select == "1":
                self.logger.info("已选择批量下载账号作品模式")
                self.account_acquisition_interactive()
            elif select == "2":
                self.logger.info("已选择批量下载链接作品模式")
                self.works_interactive()
            elif select == "3":
                self.logger.info("已选择获取直播推流地址模式")
                self.live_interactive()
            elif select == "4":
                self.logger.info("已选择采集作品评论数据模式")
                self.comment_interactive()
            elif select == "5":
                self.logger.info("已选择批量下载合集作品模式")
                self.mix_interactive()
            elif select == "6":
                self.logger.info("已选择批量采集账号数据模式")
                self.user_interactive()
            elif select == "7":
                self.logger.info("已选择采集搜索结果数据模式")
                self.search_interactive()
            elif select == "8":
                self.logger.info("已选择采集抖音热榜数据模式")
                self.hot_interactive()
            elif select == "9":
                self.logger.info("已选择批量下载收藏作品模式")
                self.collection_interactive()
