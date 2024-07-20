from datetime import date
from datetime import datetime
from pathlib import Path
from platform import system
from time import time
from types import SimpleNamespace
from typing import TYPE_CHECKING

from src.custom import (
    WARNING,
)
from src.custom import failure_handling
from src.custom import suspend
from src.downloader import Downloader
from src.extract import Extractor
from src.interface import (
    Account,
    AccountTikTok,
    Comment,
    Detail,
    Live,
    Collection,
    Mix,
    Hot,
    Search,
    User,
    HashTag,
    DetailTikTok,
    CollectsMix,
    LiveTikTok,
    MixTikTok,
    # CommentTikTok,
    Collects,
    # CollectsSeries,
    CollectsMusic,
    CollectsDetail,
)
from src.link import Extractor as LinkExtractor
from src.link import ExtractorTikTok
from src.manager import Cache
from src.storage import RecordManager
from src.tools import choose
from src.tools import safe_pop

if TYPE_CHECKING:
    from src.config import Parameter
    from src.manager import Database

__all__ = [
    "TikTok",
]


def check_storage_format(function):
    async def inner(self, *args, **kwargs):
        if self.parameter.storage_format:
            return await function(self, *args, **kwargs)
        self.console.print(
            "未设置 storage_format 参数，无法正常使用该功能，详细说明请查阅项目文档！",
            style=WARNING)

    return inner


def check_cookie_state(tiktok=False):
    def check_cookie(function):
        async def inner(self, *args, **kwargs):
            if tiktok:
                params = self.parameter.cookie_tiktok_state
                tip = "TikTok Cookie"
            else:
                params = self.parameter.cookie_state
                tip = "抖音 Cookie"
            if params:
                return await function(self, *args, **kwargs)
            self.console.print(
                f"{tip} 未登录，无法使用该功能，详细说明请查阅项目文档！",
                style=WARNING)

        return inner

    return check_cookie


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
    ENCODE = "UTF-8-SIG" if system() == "Windows" else "UTF-8"

    def __init__(self, parameter: "Parameter", database: "Database", ):
        self.default_mode = None
        self.parameter = parameter
        self.database = database
        self.console = parameter.console
        self.logger = parameter.logger
        self.links = LinkExtractor(parameter)
        self.links_tiktok = ExtractorTikTok(parameter)
        self.downloader = Downloader(parameter)
        self.extractor = Extractor(parameter)
        self.storage = bool(parameter.storage_format)
        self.record = RecordManager()
        self.settings = parameter.settings
        self.accounts = parameter.accounts_urls
        self.accounts_tiktok = parameter.accounts_urls_tiktok
        self.mix = parameter.mix_urls
        self.mix_tiktok = parameter.mix_urls_tiktok
        self.owner = parameter.owner_url
        self.owner_tiktok = parameter.owner_url_tiktok
        self.running = True
        self.cache = Cache(
            parameter,
            self.database,
            "mark" in parameter.name_format,
            "nickname" in parameter.name_format
        )
        self.__function = (
            ("批量下载账号作品(抖音)", self.account_acquisition_interactive,),
            ("批量下载链接作品(抖音)", self.detail_interactive,),
            ("获取直播推流地址(抖音)", self.live_interactive,),
            # ("采集作品评论数据(抖音)", self.comment_interactive,),
            ("批量下载合集作品(抖音)", self.mix_interactive,),
            # ("采集账号详细数据(抖音)", self.disable_function,),
            # ("采集搜索结果数据(抖音)", self.disable_function,),
            ("采集抖音热榜数据(抖音)", self.hot_interactive,),
            # ("批量下载话题作品(抖音)", self.disable_function,),
            ("批量下载收藏作品(抖音)", self.collection_interactive,),
            ("批量下载收藏音乐(抖音)", self.collection_music_interactive,),
            # ("批量下载收藏短剧(抖音)", self.disable_function,),
            ("批量下载收藏夹作品(抖音)", self.collects_interactive,),
            ("批量下载账号作品(TikTok)", self.account_acquisition_interactive_tiktok,),
            ("批量下载链接作品(TikTok)", self.detail_interactive_tiktok,),
            ("批量下载合集作品(TikTok)", self.mix_interactive_tiktok,),
            ("获取直播推流地址(TikTok)", self.live_interactive_tiktok,),
            # ("采集作品评论数据(TikTok)", self.comment_interactive_tiktok,),
        )
        self.__function_account = (
            ("使用 accounts_urls 参数的账号链接(推荐)", self.account_detail_batch),
            ("手动输入待采集的账号链接", self.account_detail_inquire),
            ("从文本文档读取待采集的账号链接", self.account_detail_txt),
        )
        self.__function_account_tiktok = (
            ("使用 accounts_urls_tiktok 参数的账号链接(推荐)", self.account_detail_batch_tiktok),
            ("手动输入待采集的账号链接", self.account_detail_inquire_tiktok),
            ("从文本文档读取待采集的账号链接", self.account_detail_txt_tiktok),
        )
        self.__function_mix = (
            ("使用 mix_urls 参数的合集链接(推荐)", self.mix_batch),
            ("获取当前账号收藏合集列表", self.mix_collection),
            ("手动输入待采集的合集/作品链接", self.mix_inquire),
            ("从文本文档读取待采集的合集/作品链接", self.mix_txt),
        )
        self.__function_mix_tiktok = (
            ("使用 mix_urls_tiktok 参数的合集链接(推荐)", self.mix_batch_tiktok),
            ("手动输入待采集的合集/作品链接", self.mix_inquire_tiktok),
            ("从文本文档读取待采集的合集/作品链接", self.mix_txt_tiktok),
        )
        self.__function_user = (
            ("使用 accounts_urls 参数的账号链接", self.user_batch),
            ("手动输入待采集的账号链接", self.user_inquire),
            ("从文本文档读取待采集的账号链接", self.user_txt),
        )
        self.__function_detail = (
            ("手动输入待采集的作品链接", self.__detail_inquire),
            ("从文本文档读取待采集的作品链接", self.__detail_txt),
        )
        self.__function_detail_tiktok = (
            ("手动输入待采集的作品链接", self.__detail_inquire_tiktok),
            ("从文本文档读取待采集的作品链接", self.__detail_txt_tiktok),
        )
        self.__function_comment = (
            ("手动输入待采集的作品链接", self.__comment_inquire),
            ("从文本文档读取待采集的作品链接", self.__comment_txt),
        )
        self.__function_comment_tiktok = (
            ("手动输入待采集的作品链接", self.__comment_inquire_tiktok),
            # ("从文本文档读取待采集的作品链接", self.__comment_txt_tiktok),
        )

    async def disable_function(self, *args, **kwargs, ):
        self.console.print("该功能暂不开放！", style=WARNING)

    def _inquire_input(self, url: str = None, tip: str = None) -> str:
        text = self.console.input(tip or f"请输入{url}链接: ")
        if not text:
            return ""
        elif text in ("Q", "q",):
            self.running = False
            return ""
        return text

    async def account_acquisition_interactive_tiktok(
            self, select="", *args, **kwargs):
        root, params, logger = self.record.run(self.parameter)
        await self.__account_secondary_menu(
            root,
            params,
            logger,
            self.__function_account_tiktok,
            select)
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

    async def account_acquisition_interactive(
            self, select="", *args, **kwargs):
        root, params, logger = self.record.run(self.parameter)
        await self.__account_secondary_menu(
            root,
            params,
            logger,
            self.__function_account,
            select)
        self.logger.info("已退出批量下载账号作品(抖音)模式")

    async def __account_secondary_menu(
            self,
            root,
            params,
            logger,
            function,
            select):
        if not select:
            select = choose("请选择账号链接来源",
                            [i[0] for i in function], self.console)
        await self.__multiple_choice(select, function, root, params, logger, )

    async def account_detail_batch(self, root, params, logger):
        count = SimpleNamespace(time=time(), success=0, failed=0)
        self.logger.info(f"共有 {len(self.accounts)} 个账号的作品等待下载")
        for index, data in enumerate(self.accounts, start=1):
            if hasattr(data, "enable") and not data.enable:
                continue
            if not (sec_user_id := await self.check_sec_user_id(data.url)):
                self.logger.warning(
                    f"配置文件 accounts_urls 参数"
                    f"第 {index} 条数据的 url {data.url} 错误，提取 sec_user_id 失败")
                count.failed += 1
                continue
            if not await self.deal_account_detail(
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
                await suspend(index, self.console)
        self.__summarize_results(count)

    async def account_detail_batch_tiktok(self, root, params, logger):
        count = SimpleNamespace(time=time(), success=0, failed=0)
        self.logger.info(f"共有 {len(self.accounts_tiktok)} 个账号的作品等待下载")
        for index, data in enumerate(self.accounts_tiktok, start=1):
            if hasattr(data, "enable") and not data.enable:
                continue
            if not (sec_user_id := await self.links_tiktok.run(data.url, "user")):
                self.logger.warning(
                    f"配置文件 accounts_urls_tiktok 参数"
                    f"第 {index} 条数据的 url {data.url} 错误，提取 sec_user_id 失败")
                count.failed += 1
                continue
            if not await self.deal_account_detail(
                    index,
                    **vars(data) | {"sec_user_id": sec_user_id[0]},
                    root=root,
                    params=params,
                    logger=logger,
                    tiktok=True,
            ):
                count.failed += 1
                if index != len(self.accounts_tiktok) and failure_handling():
                    continue
                break
            # break  # 调试代码
            count.success += 1
            if index != len(self.accounts_tiktok):
                await suspend(index, self.console)
        self.__summarize_results(count)

    async def check_sec_user_id(self, sec_user_id: str) -> str:
        sec_user_id = await self.links.run(sec_user_id, "user")
        return sec_user_id[0] if len(sec_user_id) > 0 else ""

    async def account_detail_inquire(self, root, params, logger):
        while url := self._inquire_input("账号主页"):
            links = await self.links.run(url, "user")
            if not links:
                self.logger.warning(f"{url} 提取账号 sec_user_id 失败")
                continue
            await self.__account_detail_handle(root, params, logger, links)

    async def account_detail_inquire_tiktok(self, root, params, logger):
        while url := self._inquire_input("账号主页"):
            links = await self.links_tiktok.run(url, "user")
            if not links:
                self.logger.warning(f"{url} 提取账号 sec_user_id 失败")
                continue
            await self.__account_detail_handle(root, params, logger, links, True, )

    async def account_detail_txt(self, root, params, logger):
        if not (url := self.txt_inquire()):
            return
        links = await self.links.run(url, "user", )
        if not links:
            self.logger.warning("从文本文档提取账号 sec_user_id 失败")
            return
        await self.__account_detail_handle(root, params, logger, links)

    async def account_detail_txt_tiktok(self, root, params, logger):
        if not (url := self.txt_inquire()):
            return
        links = await self.links_tiktok.run(url, "user")
        if not links:
            self.logger.warning("从文本文档提取账号 sec_user_id 失败")
            return
        await self.__account_detail_handle(root, params, logger, links, True, )

    async def __account_detail_handle(
            self,
            root,
            params,
            logger,
            links,
            tiktok=False,
    ):
        count = SimpleNamespace(time=time(), success=0, failed=0)
        for index, sec in enumerate(links, start=1):
            if not await self.deal_account_detail(
                    index,
                    sec_user_id=sec,
                    root=root,
                    params=params,
                    logger=logger,
                    tiktok=tiktok,
            ):
                count.failed += 1
                if index != len(links) and failure_handling():
                    continue
                break
            count.success += 1
            if index != len(links):
                await suspend(index, self.console)
        self.__summarize_results(count)

    async def deal_account_detail(
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
            proxy: str = None,
            tiktok=False,
            *args,
            **kwargs,
    ):
        self.logger.info(f"开始处理第 {num} 个账号" if num else "开始处理账号")
        if tiktok:
            acquirer = AccountTikTok(
                self.parameter,
                cookie,
                proxy,
                sec_user_id,
                tab,
                earliest,
                latest,
                pages,
            )
        else:
            acquirer = Account(
                self.parameter,
                cookie,
                proxy,
                sec_user_id,
                tab,
                earliest,
                latest,
                pages,
            )
        account_data, earliest, latest = await acquirer.run()
        if not any(account_data):
            # self.logger.warning("获取账号主页数据失败")
            return None
        if source:
            # TODO: 未适配 TikTok 平台
            return self.extractor.source_date_filter(
                account_data[:None if tab == "post" else -1],
                earliest,
                latest
            )
        return await self._batch_process_detail(
            root,
            params,
            logger,
            account_data,
            sec_user_id,
            mark,
            tab == "post",
            api=api,
            earliest=earliest,
            latest=latest,
            tiktok=tiktok,
        )

    async def _batch_process_detail(self,
                                    root,
                                    params: dict,
                                    logger,
                                    data,
                                    id_,
                                    mark,
                                    post=True,
                                    mix=False,
                                    api=False,
                                    earliest: date = None,
                                    latest: date = None,
                                    addition: str = None,
                                    tiktok=False,
                                    title: str = None,
                                    collect_id: str = None,
                                    ):
        self.logger.info("开始提取作品数据")
        id_, name, mid, title, mark, data = self.extractor.preprocessing_data(
            data, id_, mark, post, mix, tiktok, title, collect_id=collect_id, )
        self.__display_extracted_information(
            mix, id_, name, mid, title, mark, )
        addition = addition or ("合集作品" if mix else "发布作品" if post else "喜欢作品")
        old_mark = f"{m["MARK"]}_{addition}" if (
            m := await self.cache.has_cache(
                mid if mix else id_)) else None
        async with logger(root,
                          name=f"{self._generate_prefix(mix=mix, collect=bool(collect_id))}{self._generate_id(id_, mid, mix=mix, collect=bool(collect_id))}_{mark}_{addition}",
                          old=old_mark,
                          console=self.console, **params) as recorder:
            data = await self.extractor.run(
                data,
                recorder,
                type_="batch",
                tiktok=tiktok,
                name=name,
                mark=mark,
                earliest=earliest or date(2016, 9, 20),
                latest=latest or date.today(),
                same=any((post, mix)))
        if api:
            return data
        await self.cache.update_cache(
            self.parameter.folder_mode,
            self._generate_prefix(mix=mix, collect=bool(collect_id)),
            self._generate_id(id_, mid, mix=mix, collect=bool(collect_id)),
            mark,
            title if mix else name,
            addition,
        )
        await self.download_account_detail(
            data, id_, name, mark, self._generate_id(id_, mid, mix=mix, collect=bool(collect_id)), title, addition,
            tiktok, collect=bool(collect_id), )
        return True

    @staticmethod
    def _generate_prefix(user=True, mix=False, collect=False):
        if collect:
            return "CID"
        if mix:
            return "MID"
        if user:
            return "UID"

    @staticmethod
    def _generate_id(id_, mid, user=True, mix=False, collect=False):
        if collect:
            return mid
        if mix:
            return mid
        if user:
            return id_

    def __display_extracted_information(
            self,
            mix: bool,
            id_: str,
            name: str,
            mid: str,
            title: str,
            mark: str,
    ) -> None:
        self.logger.info(f"合集标题：{title}；合集标识：{mark}；合集 ID：{mid}", mix, )
        self.logger.info(f"账号昵称：{name}；账号标识：{mark}；账号 ID：{id_}", not mix, )

    async def download_account_detail(
            self,
            data: list[dict],
            id_: str,
            name: str,
            mark: str,
            mid: str = None,
            title: str = None,
            addition: str = None,
            tiktok: bool = False,
            collect=False,
    ):
        await self.downloader.run(
            data,
            "batch",
            tiktok,
            id_=id_,
            name=name,
            mark=mark,
            addition=addition,
            mid=mid,
            title=title,
            collect=collect,
        )

    async def detail_interactive(self, select="", *args, **kwargs):
        await self.__detail_secondary_menu(self.__function_detail, select)
        self.logger.info("已退出批量下载链接作品(抖音)模式")

    async def detail_interactive_tiktok(self, select="", *args, **kwargs):
        await self.__detail_secondary_menu(self.__function_detail_tiktok, select)
        self.logger.info("已退出批量下载链接作品(TikTok)模式")

    async def __detail_secondary_menu(self, menu, select="", *args, **kwargs):
        root, params, logger = self.record.run(self.parameter)
        async with logger(root, console=self.console, **params) as record:
            if not select:
                select = choose(
                    "请选择作品链接来源", [
                        i[0] for i in menu], self.console)
            if select.upper() == "Q":
                self.running = False
            try:
                n = int(select) - 1
            except ValueError:
                return
            if n in range(len(menu)):
                await menu[n][1](record)

    async def __detail_inquire(self, record, tiktok=False, ):
        while url := self._inquire_input("作品"):
            ids = await self.links_tiktok.run(url) if tiktok else await self.links.run(url)
            if not any(ids):
                self.logger.warning(f"{url} 提取作品 ID 失败")
                continue
            self.console.print(f"共提取到 {len(ids)} 个作品，开始处理！")
            await self.input_links_acquisition(tiktok, ids, record)

    async def __detail_inquire_tiktok(self, record, tiktok=True, ):
        await self.__detail_inquire(record, tiktok)

    async def __detail_txt(self, record, tiktok=False, ):
        if ids := await self.__read_detail_txt():
            await self.input_links_acquisition(tiktok, ids, record)

    async def __detail_txt_tiktok(self, record, tiktok=True, ):
        await self.__detail_txt(record, tiktok)

    async def __read_detail_txt(self):
        if not (url := self.txt_inquire()):
            return
        ids = await self.links.run(url)
        if not any(ids):
            self.logger.warning("从文本文档提取作品 ID 失败")
            return
        self.console.print(f"共提取到 {len(ids)} 个作品，开始处理！")
        return ids

    async def input_links_acquisition(
            self,
            tiktok: bool,
            ids: list[str],
            record,
            api=False,
            source=False,
            cookie: str = None,
            proxy: str = None, ):
        if tiktok:
            detail_data = [
                await DetailTikTok(
                    self.parameter,
                    cookie,
                    proxy,
                    i,
                ).run() for i in ids]
        else:
            detail_data = [
                await Detail(
                    self.parameter,
                    cookie,
                    proxy,
                    i,
                ).run() for i in ids]
        if not any(detail_data):
            # self.logger.warning("获取作品数据失败")
            return None
        if source:
            return detail_data
        detail_data = await self.extractor.run(detail_data, record, tiktok=tiktok, )
        if api:
            return detail_data
        await self.downloader.run(detail_data, "detail", tiktok=tiktok)
        return self._get_preview_image(detail_data[0])

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

    async def live_interactive(
            self,
            cookie: str = None,
            proxy: str = None,
            *args,
            **kwargs):
        while url := self._inquire_input("直播"):
            params = self._generate_live_params(*await self.links.run(url, type_="live"))
            if not params:
                self.logger.warning(f"{url} 提取直播 ID 失败")
                continue
            live_data = [await Live(self.parameter, cookie, proxy, **i).run() for i in params]
            if not [i for i in live_data if i]:
                self.logger.warning("获取直播数据失败")
                continue
            live_data = await self.extractor.run(live_data, None, "live")
            download_tasks = self.show_live_info(live_data)
            await self.downloader.run_live(download_tasks)
        self.logger.info("已退出获取直播推流地址(抖音)模式")

    async def live_interactive_tiktok(
            self,
            cookie: str = None,
            proxy: str = None,
            *args,
            **kwargs):
        while url := self._inquire_input("直播"):
            _, ids = await self.links_tiktok.run(url, type_="live")
            if not ids:
                self.logger.warning(f"{url} 提取直播 ID 失败")
                continue
            live_data = [await LiveTikTok(self.parameter, cookie, proxy, i).run() for i in ids]
            if not [i for i in live_data if i]:
                self.logger.warning("获取直播数据失败")
                continue
            live_data = await self.extractor.run(live_data, None, "live", tiktok=True, )
            download_tasks = self.show_live_info_tiktok(live_data)
            await self.downloader.run_live(download_tasks, tiktok=True)
        self.logger.info("已退出获取直播推流地址(TikTok)模式")

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

    def show_live_info_tiktok(self, data: list[dict]) -> list[tuple]:
        download_tasks = []
        for item in data:
            if item["message"]:
                self.console.print(item["message"])
                self.console.print(item["prompts"])
                continue
            self.console.print("直播标题:", item["title"])
            self.console.print("主播昵称:", item["nickname"])
            self.console.print("开播时间:", item["create_time"])
            self.console.print("在线观众:", item["user_count"])
            self.console.print("点赞次数:", item["like_count"])
            # TODO: TikTok 直播下载功能异常，代理错误
            # self.show_live_stream_url_tiktok(item, download_tasks)
        self.console.print("TikTok 直播下载功能尚未完成！")  # 完成后移除
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

    def show_live_stream_url_tiktok(self, item: dict, tasks: list):
        self.console.print("FLV 推流地址: ")
        for i, (k, v) in enumerate(item["flv_pull_url"].items(), start=1):
            self.console.print(i, k, v)
        if self.parameter.download:
            tasks.append(
                (item,
                 *
                 u) if (  # TikTok 平台 暂无 m3u8 地址
                    u := self._choice_live_quality(
                        item["flv_pull_url"],
                        item["flv_pull_url"])) else u)

    @check_storage_format
    async def comment_interactive_tiktok(self, select="", *args, **kwargs):
        await self.__comment_interactive(self.__function_comment_tiktok, select, *args, **kwargs, )
        self.logger.info("已退出采集作品评论数据(TikTok)模式")

    @check_storage_format
    async def comment_interactive(self, select="", *args, **kwargs):
        await self.__comment_interactive(self.__function_comment, select, *args, **kwargs, )
        self.logger.info("已退出采集作品评论数据(抖音)模式")

    async def __comment_interactive(self, function: tuple | list = ..., select="", *args, **kwargs):
        root, params, logger = self.record.run(self.parameter, type_="comment")
        if not select:
            select = choose(
                "请选择作品链接来源", [
                    i[0] for i in function], self.console)
        if select.upper() == "Q":
            self.running = False
        try:
            n = int(select) - 1
        except ValueError:
            return
        if n in range(len(function)):
            await function[n][1](root, params, logger)

    async def __comment_inquire(self, root, params, logger, tiktok=False, ):
        link = self.links_tiktok if tiktok else self.links
        while url := self._inquire_input("作品"):
            ids = await link.run(url, )
            if not any(ids):
                self.logger.warning(f"{url} 提取作品 ID 失败")
                continue
            self.console.print(f"共提取到 {len(ids)} 个作品，开始处理！")
            await self.__comment_handle(ids, root, params, logger, tiktok=tiktok, )

    async def __comment_inquire_tiktok(self, root, params, logger):
        await self.__comment_inquire(root, params, logger, True, )

    async def __comment_txt(self, root, params, logger):
        if ids := await self.__read_detail_txt():
            await self.__comment_handle(ids, root, params, logger)

    async def __comment_handle(
            self,
            ids: list,
            root,
            params,
            logger,
            cookie: str = None,
            proxy: str = None,
            tiktok=False,
    ):
        if tiktok:  # TODO: 代码未完成
            pass
            # for i in ids:
            #     name = f"作品{i}_评论数据"
            #     async with logger(root, name=name, console=self.console, **params) as record:
            #         if d := await CommentTikTok(self.parameter, cookie, proxy, item_id=i, ).run():
            #             await self.extractor.run(d, record, type_="comment")
            #             self.logger.info(f"作品评论数据已储存至 {name}")
            #         else:
            #             self.logger.warning("采集评论数据失败")
        else:
            for i in ids:
                name = f"作品{i}_评论数据"
                async with logger(root, name=name, console=self.console, **params) as record:
                    if d := await Comment(self.parameter, cookie, proxy, item_id=i, ).run():
                        await self.extractor.run(d, record, type_="comment")
                        self.logger.info(f"作品评论数据已储存至 {name}")
                    else:
                        self.logger.warning("采集评论数据失败")

    async def mix_interactive(self, select="", *args, **kwargs):
        await self.__mix_interactive(self.__function_mix, select, False, *args, **kwargs)

    async def mix_interactive_tiktok(self, select="", *args, **kwargs):
        await self.__mix_interactive(self.__function_mix_tiktok, select, True, *args, **kwargs)

    async def __mix_interactive(self, function, select="", tiktok=False, *args, **kwargs):
        root, params, logger = self.record.run(self.parameter, type_="mix")
        if not select:
            select = choose("请选择合集链接来源",
                            [i[0] for i in function], self.console)
        await self.__multiple_choice(select, function, root, params, logger, )
        self.logger.info(f"已退出批量下载合集作品{"(TikTok)" if tiktok else "(抖音)"}模式")

    async def __multiple_choice(self, select: str, function, *args, **kwargs, ):
        if select.upper() == "Q":
            self.running = False
        try:
            n = int(select) - 1
        except ValueError:
            return
        if n in range(len(function)):
            await function[n][1](*args, **kwargs, )

    @staticmethod
    def _generate_mix_params(mix: bool, id_: str) -> dict:
        return {"mix_id": id_, } if mix else {"detail_id": id_, }

    async def mix_inquire(self, root, params, logger):
        while url := self._inquire_input("合集或作品"):
            mix_id, ids = await self.links.run(url, type_="mix")
            if not ids:
                self.logger.warning(f"{url} 获取作品 ID 或合集 ID 失败")
                continue
            await self.__mix_handle(root, params, logger, mix_id, ids)

    async def mix_inquire_tiktok(self, root, params, logger):
        while url := self._inquire_input("合集或作品"):
            _, ids, title = await self.links_tiktok.run(url, type_="mix")
            if not ids:
                self.logger.warning(f"{url} 获取合集 ID 失败")
                continue
            await self.__mix_handle(root, params, logger, True, ids, True, title, )

    @check_cookie_state(tiktok=False)
    async def mix_collection(self, root, params, logger):
        if id_ := await self.mix_inquire_collection():
            await self.__mix_handle(root, params, logger, True, id_)

    async def mix_inquire_collection(self) -> list[str]:
        data = await CollectsMix(self.parameter).run()
        if not data:
            return []
        data = self.extractor.extract_mix_collect_info(data)
        return self.input_download_index(data)

    def input_download_index(self, data: list[dict]) -> list[str]:
        _, id_ = self.__input_download_index(data)
        return id_

    def __input_download_index(self,
                               data: list[dict],
                               text="合集",
                               key="title",
                               ) -> [list[str],
                                     list[str]]:
        self.console.print(f"{text}列表：")
        for i, j in enumerate(data, start=1):
            self.console.print(f"{i}. {j[key]}")
        index = self.console.input(f"请输入需要下载的{text}序号(多个序号使用空格分隔，输入 ALL 下载全部{text})：")
        try:
            if index.upper() == "ALL":
                return zip(*[(d[key], d["id"]) for d in data])
            index = {int(i) for i in index.split()}
            return zip(*[(d[key], d["id"]) for i, d in enumerate(data, start=1) if i in index])
        except ValueError:
            self.console.print(f"{text}序号输入错误！", style=WARNING)
            return []

    async def mix_txt(self, root, params, logger):
        if not (url := self.txt_inquire()):
            return
        mix_id, ids = await self.links.run(url, type_="mix")
        if not ids:
            self.logger.warning("从文本文档提取作品 ID 或合集 ID 失败")
            return
        await self.__mix_handle(root, params, logger, mix_id, ids)

    async def mix_txt_tiktok(self, root, params, logger):
        if not (url := self.txt_inquire()):
            return
        _, ids, title = await self.links_tiktok.run(url, type_="mix")
        if not ids:
            self.logger.warning("从文本文档提取合集 ID 失败")
            return
        await self.__mix_handle(root, params, logger, True, ids, True, title, )

    async def __mix_handle(
            self,
            root,
            params,
            logger,
            mix_id: bool,
            ids: list[str],
            tiktok=False,
            mix_title_map: list[str] = None,
    ):
        count = SimpleNamespace(time=time(), success=0, failed=0)
        for index, i in enumerate(ids, start=1):
            if not await self._deal_mix_detail(
                    root,
                    params,
                    logger,
                    mix_id,
                    i,
                    num=index,
                    tiktok=tiktok,
                    mix_title=mix_title_map[index - 1] if mix_title_map else None,
            ):
                count.failed += 1
                if index != len(ids) and failure_handling():
                    continue
                break
            count.success += 1
            if index != len(ids):
                await suspend(index, self.console)
        self.__summarize_results(count, "合集")

    async def mix_batch(self, root, params, logger):
        count = SimpleNamespace(time=time(), success=0, failed=0)
        for index, data in enumerate(self.mix, start=1):
            if hasattr(data, "enable") and not data.enable:
                continue
            mix_id, id_ = await self._check_mix_id(data.url)
            if not id_:
                self.logger.warning(
                    f"配置文件 mix_urls 参数" f"第 {index} 条数据的 url {
                    data.url} 错误，获取作品 ID 或合集 ID 失败")
                count.failed += 1
                continue
            if not await self._deal_mix_detail(
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
                await suspend(index, self.console)
        self.__summarize_results(count, "合集")

    async def mix_batch_tiktok(self, root, params, logger):
        count = SimpleNamespace(time=time(), success=0, failed=0)
        for index, data in enumerate(self.mix_tiktok, start=1):
            if hasattr(data, "enable") and not data.enable:
                continue
            _, ids, title = await self.links_tiktok.run(data.url, type_="mix")
            if not ids:
                self.logger.warning(
                    f"配置文件 mix_urls_tiktok 参数" f"第 {index} 条数据的 url {
                    data.url} 错误，获取合集 ID 失败")
                count.failed += 1
                continue
            id_, title = ids[0], title[0]
            if not await self._deal_mix_detail(
                    root,
                    params,
                    logger,
                    True,
                    id_,
                    data.mark,
                    index,
                    tiktok=True,
                    mix_title=title,
            ):
                count.failed += 1
                if index != len(self.mix_tiktok) and failure_handling():
                    continue
                break
            count.success += 1
            if index != len(self.mix_tiktok):
                await suspend(index, self.console)
        self.__summarize_results(count, "合集")

    async def _deal_mix_detail(self,
                               root,
                               params,
                               logger,
                               mix_id: bool = None,
                               id_: str = None,
                               mark="",
                               num: int = 0,
                               api=False,
                               source=False,
                               cookie: str = None,
                               proxy: str = None,
                               tiktok=False,
                               mix_title: str = "",
                               ):
        self.logger.info(f"开始处理第 {num} 个合集" if num else "开始处理合集")
        mix_params = self._generate_mix_params(mix_id, id_)
        if tiktok:
            mix_obj = MixTikTok(
                self.parameter,
                cookie,
                proxy,
                mix_title=mix_title,
                **mix_params,
            )
        else:
            mix_obj = Mix(
                self.parameter,
                cookie,
                proxy,
                **mix_params,
            )
        if any(
                mix_data := await mix_obj.run()):
            return (
                mix_data
                if source
                else await self._batch_process_detail(
                    root,
                    params,
                    logger,
                    mix_data,
                    mix_obj.mix_id,
                    mark,
                    mix=True,
                    api=api,
                    tiktok=tiktok,
                    title=mix_obj.mix_title,
                )
            )
        self.logger.warning("采集合集作品数据失败")
        return None

    async def _check_mix_id(self, url: str) -> tuple[bool, str]:
        mix_id, ids = await self.links.run(url, type_="mix")
        return (mix_id, ids[0]) if len(ids) > 0 else (mix_id, "")

    async def user_batch(self, root, params, logger):
        users = []
        for index, data in enumerate(self.accounts, start=1):
            if not (sec_user_id := await self.check_sec_user_id(data.url)):
                self.logger.warning(
                    f"配置文件 accounts_urls 参数"
                    f"第 {index} 条数据的 url 无效")
                continue
            users.append(await self._get_user_data(sec_user_id))
        await self._deal_user_data(root, params, logger, [i for i in users if i])

    async def user_inquire(self, root, params, logger):
        while url := self._inquire_input("账号主页"):
            sec_user_ids = await self.links.run(url, type_="user")
            if not sec_user_ids:
                self.logger.warning(f"{url} 提取账号 sec_user_id 失败")
                continue
            users = [await self._get_user_data(i) for i in sec_user_ids]
            await self._deal_user_data(root, params, logger, [i for i in users if i])

    def txt_inquire(self) -> str:
        path = self.console.input("请输入文本文档路径：")
        if not (t := Path(path.replace("\"", ""))).is_file():
            self.console.print(f"{path} 文件不存在！")
            return ""
        with t.open("r", encoding=self.ENCODE) as f:
            return f.read()

    async def user_txt(self, root, params, logger):
        if not (url := self.txt_inquire()):
            return
        sec_user_ids = await self.links.run(url, type_="user")
        if not sec_user_ids:
            self.logger.warning("从文本文档提取账号 sec_user_id 失败")
            return
        users = [await self._get_user_data(i) for i in sec_user_ids]
        await self._deal_user_data(root, params, logger, [i for i in users if i])

    async def _get_user_data(
            self,
            sec_user_id: str,
            cookie: str = None,
            proxy: str = None,
    ):
        self.logger.info(f"正在获取账号 {sec_user_id} 的数据")
        data = await User(self.parameter, cookie, proxy, sec_user_id, ).run()
        return data or {}

    async def _deal_user_data(
            self,
            root,
            params,
            logger,
            data: list[dict],
            source=False):
        if not any(data):
            # self.logger.warning("采集账号数据失败")
            return None
        if source:
            return data
        async with logger(root, name="UserData", console=self.console, **params) as recorder:
            data = self.extractor.run(data, recorder, type_="user")
        self.logger.info("账号数据已保存至文件")
        return data

    @check_storage_format
    async def user_interactive(self, select="", *args, **kwargs):
        root, params, logger = self.record.run(self.parameter, type_="user")
        await self.__account_secondary_menu(
            root,
            params,
            logger,
            self.__function_user,
            select)
        self.logger.info("已退出采集账号详细数据模式")

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
    async def search_interactive(self, *args, **kwargs):
        while True:
            if isinstance(c := self._enter_search_criteria(), tuple):
                await self._deal_search_data(*c)
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

    async def _deal_search_data(
            self,
            keyword: str,
            type_: tuple,
            pages: int,
            sort: tuple,
            publish: tuple,
            source=False,
            cookie: str = None,
            proxy: str = None,
    ):
        search_data = await Search(
            self.parameter,
            cookie,
            proxy,
            keyword,
            type_[0],
            pages,
            sort[0],
            publish[0],
        ).run()
        if not any(search_data):
            # self.logger.warning("采集搜索数据失败")
            return None
        # print(search_data)  # 调试代码
        if source:
            return search_data
        name = self._generate_search_name(
            keyword, type_[1], sort[1], publish[1])
        root, params, logger = self.record.run(self.parameter,
                                               type_=self.DATA_TYPE[type_[0]])
        async with logger(root, name=name, console=self.console, **params) as logger:
            search_data = await self.extractor.run(
                search_data,
                logger,
                type_="search",
                tab=type_[0])
            self.logger.info(f"搜索数据已保存至 {name}")
        # print(search_data)  # 调试代码
        return search_data

    @check_storage_format
    async def hot_interactive(self, *args, **kwargs):
        await self._deal_hot_data()
        self.logger.info("已退出采集抖音热榜数据(抖音)模式")

    async def _deal_hot_data(
            self,
            source=False,
            cookie: str = None,
            proxy: str = None,
    ):
        time_, board = await Hot(self.parameter, cookie, proxy, ).run()
        if not any(board):
            return None, None
        if source:
            return time_, [{Hot.board_params[i].name: j} for i, j in board]
        root, params, logger = self.record.run(self.parameter, type_="hot")
        data = []
        for i, j in board:
            name = f"热榜数据_{time_}_{Hot.board_params[i].name}"
            async with logger(root, name=name, console=self.console, **params) as record:
                data.append(
                    {Hot.board_params[i].name: await self.extractor.run(j, record, type_="hot")})
        self.logger.info(f"热榜数据已储存至: 实时热榜数据_{time_} + 榜单类型")
        # print(time_, data, source)  # 调试代码
        return time_, data

    @check_cookie_state(tiktok=False)
    async def collection_interactive(self, *args, **kwargs):
        if isinstance(sec_user_id := await self.__check_owner_url(), str):
            root, params, logger = self.record.run(self.parameter)
            start = time()
            await self._deal_collection_data(root, params, logger, sec_user_id)
            time_ = time() - start
            self.logger.info(
                f"程序运行耗时 {
                int(time_ //
                    60)} 分钟 {
                int(time_ %
                    60)} 秒")
        self.logger.info("已退出批量下载收藏作品(抖音)模式")

    @check_cookie_state(tiktok=False)
    async def collects_interactive(self, *args, **kwargs):
        if sec_user_id := await self.__check_owner_url():
            try:
                names, ids = await self.__get_collects_list()
            except ValueError:
                names, ids = [], []
            root, params, logger = self.record.run(self.parameter)
            start = time()
            for i, j in zip(names, ids):
                await self._deal_collects_data(root, params, logger, sec_user_id, i, j)
            time_ = time() - start
            self.logger.info(
                f"程序运行耗时 {
                int(time_ //
                    60)} 分钟 {
                int(time_ %
                    60)} 秒")
        else:
            self.console.print("该模式必须设置 owner_url 参数才能使用", style=WARNING)
        self.logger.info("已退出批量下载收藏夹作品(抖音)模式")

    async def __get_collects_list(self,
                                  cookie: str = None,
                                  proxy: str | dict = None,
                                  # api=False,
                                  source=False,
                                  *args,
                                  **kwargs,
                                  ):
        collects = await Collects(self.parameter, cookie, proxy, ).run()
        if not any(collects):
            return None
        if source:
            return collects
        data = self.extractor.extract_collects_info(collects)
        return self.__input_download_index(data, "收藏夹", "name", )

    async def __check_owner_url(self, tiktok=False, ):
        if not (sec_user_id := await self.check_sec_user_id(self.owner.url)):
            self.logger.warning(
                f"配置文件 owner_url 的 url 参数 {self.owner.url} 无效")
            if self.console.input(
                    "程序无法获取账号信息，建议修改配置文件后重新运行，是否返回上一级菜单(YES/NO)").upper != "NO":
                return None
            return ""
        return sec_user_id

    @check_cookie_state(tiktok=False)
    async def collection_music_interactive(self, *args, **kwargs, ):
        start = time()
        if data := await self.__handle_collection_music(*args, **kwargs):
            data = await self.extractor.run(data, None, "music", )
            await self.downloader.run_music(data, )
        time_ = time() - start
        self.logger.info(
            f"程序运行耗时 {
            int(time_ //
                60)} 分钟 {
            int(time_ %
                60)} 秒")
        self.logger.info("已退出批量下载收藏音乐(抖音)模式")

    async def __handle_collection_music(self,
                                        # api=False,
                                        # source=False,
                                        cookie: str = None,
                                        proxy: str = None,
                                        *args,
                                        **kwargs,
                                        ):
        data = await CollectsMusic(self.parameter, cookie, proxy, *args, **kwargs).run()
        if not any(data):
            return None
        return data

    async def _deal_collection_data(
            self,
            root,
            params,
            logger,
            sec_user_id: str,
            api=False,
            source=False,
            cookie: str = None,
            proxy: str = None,
            tiktok=False,
    ):
        self.logger.info("开始获取收藏数据")
        collection = await Collection(self.parameter, cookie, proxy, sec_user_id, ).run()
        if not any(collection):
            # self.logger.warning("获取账号收藏数据失败")
            return None
        if source:
            return collection
        return await self._batch_process_detail(
            root,
            params,
            logger,
            collection,
            sec_user_id,
            self.owner.mark,
            False,
            api=api,
            addition="收藏作品",
            tiktok=tiktok,
        )

    async def _deal_collects_data(
            self,
            root,
            params,
            logger,
            sec_user_id: str,
            name: str,
            id_: str,
            api=False,
            source=False,
            cookie: str = None,
            proxy: str = None,
            tiktok=False,
    ):
        self.logger.info("开始获取收藏夹数据")
        data = await CollectsDetail(self.parameter, cookie, proxy, id_, sec_user_id, ).run()
        if not any(data):
            return None
        if source:
            return data
        return await self._batch_process_detail(
            root,
            params,
            logger,
            data,
            sec_user_id,
            name,
            post=False,
            api=api,
            addition="收藏夹作品",
            tiktok=tiktok,
            title=name,
            collect_id=id_,
        )

    async def hashtag_interactive(
            self,
            cookie: str = None,
            proxy: str = None,
            *args,
            **kwargs,
    ):
        await HashTag(self.parameter, cookie, proxy, ).run()

    async def run(self, default_mode: list):
        self.default_mode = default_mode
        while self.running:
            if not (select := safe_pop(self.default_mode)):
                select = choose(
                    "请选择采集功能",
                    [i for i, _ in self.__function],
                    self.console)
            if select in {"Q", "q", }:
                self.running = False
            try:
                n = int(select) - 1
            except ValueError:
                break
            if n in range(len(self.__function)):
                await self.__function[n][1](safe_pop(self.default_mode))
