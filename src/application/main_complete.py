from datetime import date
from datetime import datetime
from random import choice
from time import time
from types import SimpleNamespace

from src.DataAcquirer import (
    Link,
    Account,
    Works,
    Live,
    Comment,
    Mix,
    User,
    Search,
    Hot,
    Collection,
)
from src.DataDownloader import Downloader
from src.custom import (
    WARNING,
)
from src.custom import failure_handling
from src.custom import suspend
from src.extract import Extractor
from src.manager import Cache
from src.storage import RecordManager
from src.tools import TikTokAccount
from src.tools import choose

__all__ = [
    "TikTok",
]


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
            "直播": 3,
            "综合搜索": 0,
            "视频搜索": 1,
            "用户搜索": 2,
            "直播搜索": 3,
            "0": 0,
            "1": 1,
            "2": 2,
            "3": 3,
        },
        "type_text": {
            0: "综合搜索",
            1: "视频搜索",
            2: "用户搜索",
            3: "直播搜索",
        },
        "sort": {
            "综合排序": 0,
            "最新发布": 2,
            "最多点赞": 1,
            "0": 0,
            "1": 1,
            "2": 2,
        },
        "sort_text": {
            0: "综合排序",
            2: "最新发布",
            1: "最多点赞",
        },
        "publish_text": {
            0: "不限",
            1: "一天内",
            7: "一周内",
            182: "半年内",
        },
    }
    DATA_TYPE = {
        0: "search_general",
        1: "search_general",
        2: "search_user",
        3: "search_live"
    }

    def __init__(self, parameter):
        self.parameter = parameter
        self.console = parameter.console
        self.logger = parameter.logger
        self.links = Link(parameter)
        self.downloader = Downloader(parameter)
        self.extractor = Extractor(parameter)
        self.storage = bool(parameter.storage_format)
        self.record = RecordManager()
        self.settings = parameter.settings
        self.accounts = parameter.accounts_urls
        self.mix = parameter.mix_urls
        self.owner = parameter.owner_url
        self.running = True
        self.cache = Cache(
            parameter,
            "mark" in parameter.name_format,
            "nickname" in parameter.name_format
        )

    def _inquire_input(self, url: str = None, tip: str = None) -> str:
        text = self.console.input(tip or f"请输入{url}链接: ")
        if not text:
            return ""
        elif text in ("Q", "q",):
            self.running = False
            return ""
        return text

    def account_acquisition_interactive_tiktok(self):
        root, params, logger = self.record.run(self.parameter)
        while path := self._inquire_input(tip="请输入 TikTok 主页 HTML 文件(夹)路径: "):
            items = TikTokAccount(path).run()
            if not items:
                self.logger.warning(f"{path} 读取 HTML 文件失败")
                continue
            count = SimpleNamespace(time=time(), success=0, failed=0)
            for index, (uid, nickname, item) in enumerate(items, start=1):
                if not self._deal_account_works_tiktok(
                        index, uid, nickname, item, root, params, logger):
                    count.failed += 1
                    if index != len(items) and failure_handling():
                        continue
                    break
                count.success += 1
                # if index != len(items):
                #     rest(index, self.console.print)
            self.__summarize_results(count)
        self.logger.info("已退出批量下载账号作品(TikTok)模式")

    def __summarize_results(self, count: SimpleNamespace, name="账号"):
        time_ = time() - count.time
        self.logger.info(
            f"程序共处理 {
            count.success +
            count.failed} 个{name}，成功 {
            count.success} 个，失败 {
            count.failed} 个，耗时 {
            int(time_ //
                60)} 分钟 {
            int(time_ %
                60)} 秒")

    def _deal_account_works_tiktok(
            self,
            num: int,
            uid: str,
            nickname: str,
            item: list[str],
            root,
            params: dict,
            logger,
    ):
        self.logger.info(f"开始处理第 {num} 个账号")
        account_data = [Works(self.parameter, i, True).run() for i in item]
        if not any(account_data):
            self.logger.warning("获取 TikTok 作品数据失败")
            return False
        tab = self.__check_post_tiktok(uid, nickname, account_data)
        return self._batch_process_works(
            root,
            params,
            logger,
            account_data,
            "",
            tab,
            addition="发布作品" if tab else "喜欢作品", )

    def __check_post_tiktok(self, uid: str, nickname: str, item: list[dict]):
        cache = self.extractor.generate_data_object(choice(item))
        uid_ = self.extractor.safe_extract(cache, "author.uid")
        nickname_ = self.extractor.safe_extract(cache, "author.nickname")
        match (uid == uid_, nickname == nickname_):
            case True, True:
                return True
            case False, False:
                item.append({
                    "author": {
                        "nickname": nickname,
                        "uid": uid,
                    }
                })
                return False
            case _:
                self.logger.error(f"发生异常: {uid, uid_, nickname, nickname_}")
                return False

    def account_acquisition_interactive(self):
        root, params, logger = self.record.run(self.parameter)
        select = choose("请选择账号链接来源",
                        ("使用 accounts_urls 参数的账号链接(推荐)",
                         "手动输入待采集的账号链接"), self.console)
        if select == "1":
            self.account_works_batch(root, params, logger)
        elif select == "2":
            self.account_works_inquire(root, params, logger)
        elif select.upper() == "Q":
            self.running = False
        self.logger.info("已退出批量下载账号作品(抖音)模式")

    def account_works_batch(self, root, params, logger):
        count = SimpleNamespace(time=time(), success=0, failed=0)
        self.logger.info(f"共有 {len(self.accounts)} 个账号的作品等待下载")
        for index, data in enumerate(self.accounts, start=1):
            if not (sec_user_id := self.check_sec_user_id(data.url)):
                self.logger.warning(
                    f"配置文件 accounts_urls 参数"
                    f"第 {index} 条数据的 url {data.url} 错误，提取 sec_user_id 失败")
                count.failed += 1
                continue
            if not self.deal_account_works(
                    index,
                    **vars(data) | {"sec_user_id": sec_user_id},
                    root=root,
                    params=params,
                    logger=logger):
                count.failed += 1
                if index != len(self.accounts) and failure_handling():
                    continue
                break
            # break  # 调试代码
            count.success += 1
            if index != len(self.accounts):
                suspend(index, self.console.print)
        self.__summarize_results(count)

    def check_sec_user_id(self, sec_user_id: str) -> str:
        sec_user_id = self.links.user(sec_user_id)
        return sec_user_id[0] if len(sec_user_id) > 0 else ""

    def account_works_inquire(self, root, params, logger):
        while url := self._inquire_input("账号主页"):
            links = self.links.user(url)
            if not links:
                self.logger.warning(f"{url} 提取账号 sec_user_id 失败")
                continue
            count = SimpleNamespace(time=time(), success=0, failed=0)
            for index, sec in enumerate(links, start=1):
                if not self.deal_account_works(
                        index,
                        sec_user_id=sec,
                        root=root,
                        params=params,
                        logger=logger):
                    count.failed += 1
                    if index != len(links) and failure_handling():
                        continue
                    break
                count.success += 1
                if index != len(links):
                    suspend(index, self.console.print)
            self.__summarize_results(count)

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
            pages: int = None,
            api=False,
            source=False,
            cookie: str = None,
            *args,
            **kwargs,
    ):
        self.logger.info(f"开始处理第 {num} 个账号" if num else "开始处理账号")
        acquirer = Account(
            self.parameter,
            sec_user_id,
            tab,
            earliest,
            latest,
            pages,
            cookie)
        account_data, earliest, latest = acquirer.run()
        if not any(account_data):
            self.logger.warning("获取账号主页数据失败")
            return None
        if source:
            return self.extractor.source_date_filter(
                account_data[:None if tab == "post" else -1],
                earliest,
                latest
            )
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
                             addition: str = None,
                             ):
        self.logger.info("开始提取作品数据")
        id_, name, mid, title, mark, data = self.extractor.preprocessing_data(
            data, mark, post, mix)
        addition = addition or ("合集作品" if mix else "发布作品" if post else "喜欢作品")
        old_mark = f"{m["mark"]}_{addition}" if (
            m := self.cache.data.get(
                mid if mix else id_)) else None
        with logger(root, name=f"{'MID' if mix else 'UID'}{mid if mix else id_}_{mark}_{addition}", old=old_mark,
                    console=self.console, **params) as recorder:
            data = self.extractor.run(
                data,
                recorder,
                type_="batch",
                name=name,
                mark=mark,
                earliest=earliest or date(2016, 9, 20),
                latest=latest or date.today(),
                same=any((post, mix)))
        if api:
            return data
        self.cache.update_cache(
            self.parameter.folder_mode,
            "MID" if mix else "UID",
            mid if mix else id_,
            mark,
            title if mix else name,
            addition,
        )
        self.download_account_works(
            data, id_, name, mark, mid, title, addition)
        return True

    def download_account_works(
            self,
            data: list[dict],
            id_: str,
            name: str,
            mark: str,
            mid: str = None,
            title: str = None,
            addition: str = None,
    ):
        self.downloader.run(
            data,
            "batch",
            id_=id_,
            name=name,
            mark=mark,
            addition=addition,
            mid=mid,
            title=title,
        )

    def works_interactive(self):
        root, params, logger = self.record.run(self.parameter)
        with logger(root, console=self.console, **params) as record:
            while url := self._inquire_input("作品"):
                tiktok, ids = self.links.works(url)
                if not any(ids):
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
            source=False,
            cookie: str = None):
        works_data = [
            Works(
                self.parameter,
                i,
                tiktok,
                cookie).run() for i in ids]
        if not any(works_data):
            self.logger.warning("获取作品数据失败")
            return None
        if source:
            return works_data
        works_data = self.extractor.run(works_data, record)
        if api:
            return works_data
        self.downloader.run(works_data, "works", tiktok=tiktok)
        return self._get_preview_image(works_data[0])

    @staticmethod
    def _get_preview_image(data: dict) -> str:
        if data["type"] == "图集":
            return data["downloads"][0]
        elif data["type"] == "视频":
            return data["origin_cover"]
        raise ValueError

    def _choice_live_quality(
            self,
            flv_items: dict,
            m3u8_items: dict) -> tuple | None:
        try:
            choice_ = self.console.input(
                "请选择下载清晰度(输入清晰度或者对应序号，直接回车代表不下载): ")
            if u := flv_items.get(choice_):
                return u, m3u8_items.get(choice_)
            if not 0 <= (i := int(choice_) - 1) < len(flv_items):
                raise ValueError
        except ValueError:
            return None
        return list(flv_items.values())[i], list(m3u8_items.values())[i]

    def live_interactive(self):
        while url := self._inquire_input("直播"):
            params = self._generate_live_params(*self.links.live(url))
            if not params:
                self.logger.warning(f"{url} 提取直播 ID 失败")
                continue
            live_data = [Live(self.parameter, **i).run() for i in params]
            if not [i for i in live_data if i]:
                self.logger.warning("获取直播数据失败")
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
        self.console.print("FLV 推流地址: ")
        for i, (k, v) in enumerate(item["flv_pull_url"].items(), start=1):
            self.console.print(i, k, v)
        self.console.print("M3U8 推流地址: ")
        for i, (k, v) in enumerate(item["hls_pull_url_map"].items(), start=1):
            self.console.print(i, k, v)
        if self.parameter.download:
            tasks.append(
                (item,
                 *
                 u) if (
                    u := self._choice_live_quality(
                        item["flv_pull_url"],
                        item["hls_pull_url_map"])) else u)

    @check_storage_format
    def comment_interactive(self):
        root, params, logger = self.record.run(self.parameter, type_="comment")
        while url := self._inquire_input("作品"):
            tiktok, ids = self.links.works(url)
            if not any(ids):
                self.logger.warning(f"{url} 提取作品 ID 失败")
                continue
            elif tiktok:
                self.console.print("目前项目暂不支持采集 TikTok 作品评论数据！", style=WARNING)
                continue
            for i in ids:
                name = f"作品{i}_评论数据"
                with logger(root, name=name, console=self.console, **params) as record:
                    if Comment(self.parameter, i).run(self.extractor, record):
                        self.logger.info(f"作品评论数据已储存至 {name}")
                    else:
                        self.logger.warning("采集评论数据失败")
        self.logger.info("已退出采集作品评论数据模式")

    def mix_interactive(self):
        root, params, logger = self.record.run(self.parameter, type_="mix")
        select = choose("请选择合集链接来源",
                        ("使用 mix_urls 参数的合集链接(推荐)",
                         "手动输入待采集的合集/作品链接"), self.console)
        if select == "1":
            self.mix_batch(root, params, logger)
        elif select == "2":
            self.mix_inquire(root, params, logger)
        elif select.upper() == "Q":
            self.running = False
        self.logger.info("已退出批量下载合集作品模式")

    @staticmethod
    def _generate_mix_params(mix: bool, id_: str) -> dict:
        return {"mix_id": id_, } if mix else {"works_id": id_, }

    def mix_inquire(self, root, params, logger):
        while url := self._inquire_input("合集或作品"):
            mix_id, ids = self.links.mix(url)
            if not ids:
                self.logger.warning(f"{url} 获取作品 ID 或合集 ID 失败")
                continue
            count = SimpleNamespace(time=time(), success=0, failed=0)
            for index, i in enumerate(ids, start=1):
                if not self._deal_mix_works(root, params, logger, mix_id, i):
                    count.failed += 1
                    if index != len(ids) and failure_handling():
                        continue
                    break
                count.success += 1
                if index != len(ids):
                    suspend(index, self.console.print)
            self.__summarize_results(count)

    def mix_batch(self, root, params, logger):
        count = SimpleNamespace(time=time(), success=0, failed=0)
        for index, data in enumerate(self.mix, start=1):
            mix_id, id_ = self._check_mix_id(data.url)
            if not id_:
                self.logger.warning(
                    f"配置文件 mix_urls 参数" f"第 {index} 条数据的 url {
                    data.url} 错误，获取作品 ID 或合集 ID 失败")
                count.failed += 1
                continue
            if not self._deal_mix_works(
                    root,
                    params,
                    logger,
                    mix_id,
                    id_,
                    data.mark,
                    index):
                count.failed += 1
                if index != len(self.mix) and failure_handling():
                    continue
                break
            count.success += 1
            if index != len(self.mix):
                suspend(index, self.console.print)
        self.__summarize_results(count, "合集")

    def _deal_mix_works(self,
                        root,
                        params,
                        logger,
                        mix_id: bool = None,
                        id_: str = None,
                        mark="",
                        num: int = 0,
                        api=False,
                        source=False,
                        cookie: str = None):
        self.logger.info(f"开始处理第 {num} 个合集" if num else "开始处理合集")
        mix_params = self._generate_mix_params(mix_id, id_)
        if any(
                mix_data := Mix(
                    self.parameter,
                    **mix_params,
                    cookie=cookie).run()):
            return (
                mix_data
                if source
                else self._batch_process_works(
                    root, params, logger, mix_data, mark, mix=True, api=api
                )
            )
        self.logger.warning("采集合集作品数据失败")
        return None

    def _check_mix_id(self, url: str) -> tuple[bool, str]:
        mix_id, id_ = self.links.mix(url)
        return (mix_id, id_[0]) if len(id_) > 0 else (mix_id, "")

    def user_batch(self):
        root, params, logger = self.record.run(self.parameter, type_="user")
        users = []
        for index, data in enumerate(self.accounts, start=1):
            if not (sec_user_id := self.check_sec_user_id(data.url)):
                self.logger.warning(
                    f"配置文件 accounts_urls 参数"
                    f"第 {index} 条数据的 url 无效")
                continue
            users.append(self._get_user_data(sec_user_id))
        self._deal_user_data(root, params, logger, [i for i in users if i])

    def user_inquire(self):
        root, params, logger = self.record.run(self.parameter, type_="user")
        while url := self._inquire_input("账号主页"):
            sec_user_ids = self.links.user(url)
            if not sec_user_ids:
                self.logger.warning(f"{url} 提取账号 sec_user_id 失败")
                continue
            users = [self._get_user_data(i) for i in sec_user_ids]
            self._deal_user_data(root, params, logger, [i for i in users if i])

    def _get_user_data(self, sec_user_id: str, cookie: str = None):
        self.logger.info(f"正在获取账号 {sec_user_id} 的数据")
        data = User(self.parameter, sec_user_id, cookie=cookie).run()
        return data or {}

    def _deal_user_data(
            self,
            root,
            params,
            logger,
            data: list[dict],
            source=False):
        if not any(data):
            self.logger.warning("采集账号数据失败")
            return None
        if source:
            return data
        with logger(root, name="UserData", console=self.console, **params) as recorder:
            data = self.extractor.run(data, recorder, type_="user")
        self.logger.info("账号数据已保存至文件")
        return data

    @check_storage_format
    def user_interactive(self):
        select = choose(
            "请选择账号链接来源",
            ("使用 accounts_urls 参数的账号链接",
             "手动输入待采集的账号链接"), self.console)
        if select == "1":
            self.user_batch()
        elif select == "2":
            self.user_inquire()
        elif select.upper() == "Q":
            self.running = False
        self.logger.info("已退出批量采集账号数据模式")

    def _enter_search_criteria(
            self, text: str = None) -> None | tuple | bool:
        if not text:
            text = self._inquire_input(
                tip="请输入搜索条件:\n(关键词 搜索类型 页数 排序规则 时间筛选)\n")
        # 分割字符串
        text = text.split()
        # 如果列表长度小于指定长度，使用空字符串补齐
        while 0 < len(text) < 5:
            text.append("0")
        return self._verify_search_criteria(*text)

    def _verify_search_criteria(
            self,
            keyword: str = None,
            type_: str = None,
            pages: str = None,
            sort: str = None,
            publish: str = None, *args) -> tuple | bool:
        if not keyword:
            return False
        if args:
            return True
        type_ = self.SEARCH["type"].get(type_, 0)
        type_text = self.SEARCH["type_text"][type_]
        pages = self._extract_integer(pages)
        sort = self.SEARCH["sort"].get(sort, 0)
        sort_text = self.SEARCH["sort_text"][sort]
        publish = int(publish) if publish in {"0", "1", "7", "182"} else 0
        publish_text = self.SEARCH["publish_text"][publish]
        return keyword, (type_, type_text), pages, (sort,
                                                    sort_text), (publish, publish_text)

    @staticmethod
    def _extract_integer(page: str) -> int:
        try:
            # 尝试将字符串转换为整数，如果转换成功，则返回比较大的数
            return max(int(page), 1)
        except ValueError:
            # 如果转换失败，则返回1
            return 1

    @check_storage_format
    def search_interactive(self):
        while True:
            if isinstance(c := self._enter_search_criteria(), tuple):
                self._deal_search_data(*c)
            elif c:
                self.console.print("搜索条件输入格式错误，详细说明请查阅文档！", style=WARNING)
                continue
            else:
                break
        self.logger.info("已退出采集搜索结果数据模式")

    @staticmethod
    def _generate_search_name(
            keyword: str,
            type_: str,
            sort: str = None,
            publish: str = None) -> str:
        format_ = (
            "搜索数据",
            f"{datetime.now():%Y_%m_%d_%H_%M_%S}",
            type_,
            keyword.strip(),
            sort,
            publish)
        if all(format_):
            return "_".join(format_)
        elif all(format_[:3]):
            return "_".join(format_[:3])
        raise ValueError

    def _deal_search_data(
            self,
            keyword: str,
            type_: tuple,
            pages: int,
            sort: tuple,
            publish: tuple,
            source=False,
            cookie: str = None, ):
        search_data = Search(
            self.parameter,
            keyword,
            type_[0],
            pages,
            sort[0],
            publish[0], cookie).run()
        if not any(search_data):
            self.logger.warning("采集搜索数据失败")
            return None
        # print(search_data)  # 调试代码
        if source:
            return search_data
        name = self._generate_search_name(
            keyword, type_[1], sort[1], publish[1])
        root, params, logger = self.record.run(self.parameter,
                                               type_=self.DATA_TYPE[type_[0]])
        with logger(root, name=name, console=self.console, **params) as logger:
            search_data = self.extractor.run(
                search_data,
                logger,
                type_="search",
                tab=type_[0])
            self.logger.info(f"搜索数据已保存至 {name}")
        # print(search_data)  # 调试代码
        return search_data

    @check_storage_format
    def hot_interactive(self):
        self._deal_hot_data()
        self.logger.info("已退出采集抖音热榜数据模式")

    def _deal_hot_data(self, source=False):
        time_, board = Hot(self.parameter).run()
        if not any(board):
            return None, None
        if source:
            return time_, [{Hot.board_params[i].name: j} for i, j in board]
        root, params, logger = self.record.run(self.parameter, type_="hot")
        data = []
        for i, j in board:
            name = f"实时热榜数据_{time_}_{Hot.board_params[i].name}"
            with logger(root, name=name, console=self.console, **params) as record:
                data.append(
                    {Hot.board_params[i].name: self.extractor.run(j, record, type_="hot")})
        self.logger.info(f"热榜数据已储存至: 实时热榜数据_{time_} + 榜单类型")
        # print(time_, data, source)  # 调试代码
        return time_, data

    def collection_interactive(self):
        root, params, logger = self.record.run(self.parameter)
        if not (sec_user_id := self.check_sec_user_id(self.owner.url)):
            self.logger.warning(
                f"配置文件 owner_url 的 url 参数 {self.owner.url} 无效")
        start = time()
        self._deal_collection_data(root, params, logger, sec_user_id)
        time_ = time() - start
        self.logger.info(
            f"程序运行耗时 {
            int(time_ //
                60)} 分钟 {
            int(time_ %
                60)} 秒")
        self.logger.info("已退出批量下载收藏作品模式")

    def _deal_collection_data(
            self,
            root,
            params,
            logger,
            sec_user_id: str,
            api=False,
            source=False):
        self.logger.info("开始获取收藏数据")
        collection = Collection(self.parameter, sec_user_id).run()
        if not any(collection):
            self.logger.warning("获取账号收藏数据失败")
            return None
        if source:
            return collection
        return self._batch_process_works(
            root,
            params,
            logger,
            collection,
            self.owner.mark,
            False,
            api=api,
            addition="收藏作品", )

    def run(self):
        while self.running:
            select = choose(
                "请选择采集功能",
                (
                    "批量下载账号作品(TikTok)",
                    "批量下载账号作品(抖音)",
                    "批量下载链接作品(通用)",
                    "获取直播推流地址(抖音)",
                    "采集作品评论数据(抖音)",
                    "批量下载合集作品(抖音)",
                    "批量采集账号数据(抖音)",
                    "采集搜索结果数据(抖音)",
                    "采集抖音热榜数据(抖音)",
                    "批量下载收藏作品(抖音)",
                ),
                self.console)
            if select in {"Q", "q"}:
                self.running = False
            elif not select:
                break
            elif select == "1":
                self.logger.info("已选择批量下载账号作品(TikTok)模式")
                self.account_acquisition_interactive_tiktok()
            elif select == "2":
                self.logger.info("已选择批量下载账号作品(抖音)模式")
                self.account_acquisition_interactive()
            elif select == "3":
                self.logger.info("已选择批量下载链接作品模式")
                self.works_interactive()
            elif select == "4":
                self.logger.info("已选择获取直播推流地址模式")
                self.live_interactive()
            elif select == "5":
                self.logger.info("已选择采集作品评论数据模式")
                self.comment_interactive()
            elif select == "6":
                self.logger.info("已选择批量下载合集作品模式")
                self.mix_interactive()
            elif select == "7":
                self.logger.info("已选择批量采集账号数据模式")
                self.user_interactive()
            elif select == "8":
                self.logger.info("已选择采集搜索结果数据模式")
                self.search_interactive()
            elif select == "9":
                self.logger.info("已选择采集抖音热榜数据模式")
                self.hot_interactive()
            elif select == "10":
                self.logger.info("已选择批量下载收藏作品模式")
                self.collection_interactive()
