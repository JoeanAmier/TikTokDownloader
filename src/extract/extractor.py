from datetime import datetime
from json import dumps
from time import localtime
from time import strftime
from time import time
from types import SimpleNamespace
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from src.custom import condition_filter

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["Extractor"]


class Extractor:
    def __init__(self, params: "Parameter"):
        self.log = params.logger
        self.date_format = params.date_format
        self.cleaner = params.cleaner
        self.type = {
            "batch": self.batch,
            "works": self.works,
            "comment": self.comment,
            "live": self.live,
            "user": self.user,
            "search": self.search,
            "hot": self.hot,
        }

    @staticmethod
    def get_user_info(data: dict) -> dict:
        try:
            return {
                "nickname": data["nickname"],
                "sec_uid": data["sec_uid"],
                "uid": data["uid"],
            }
        except (KeyError, TypeError):
            return {}

    @staticmethod
    def generate_data_object(data: dict) -> SimpleNamespace:
        def depth_conversion(element):
            if isinstance(element, dict):
                return SimpleNamespace(
                    **{k: depth_conversion(v) for k, v in element.items()})
            elif isinstance(element, list):
                return [depth_conversion(item) for item in element]
            else:
                return element

        return depth_conversion(data)

    @staticmethod
    def safe_extract(
            data: SimpleNamespace,
            attribute_chain: str,
            default: str | int | list | dict | SimpleNamespace = ""):
        attributes = attribute_chain.split(".")
        for attribute in attributes:
            if "[" in attribute:
                parts = attribute.split("[", 1)
                attribute = parts[0]
                index = parts[1].split("]", 1)[0]
                try:
                    index = int(index)
                    data = getattr(data, attribute, None)[index]
                except (IndexError, TypeError, ValueError):
                    return default
            else:
                data = getattr(data, attribute, None)
                if not data:
                    return default
        return data or default

    def run(
            self,
            data: list[dict],
            recorder,
            type_="works",
            **kwargs) -> list[dict]:
        if type_ not in self.type.keys():
            raise ValueError
        return self.type[type_](data, recorder, **kwargs)

    def batch(
            self,
            data: list[dict],
            recorder,
            name: str,
            mark: str,
            earliest,
            latest,
            same=True,
    ) -> list[dict]:
        container = SimpleNamespace(
            all_data=[],
            template={
                "collection_time": datetime.now().strftime(self.date_format),
            },
            cache=None,
            name=name,
            mark=mark,
            same=same,
            earliest=earliest,
            latest=latest,
        )
        [self.extract_batch(container, self.generate_data_object(item))
         for item in data]
        self._extract_item_records(container.all_data)
        self.record_data(recorder, container.all_data)
        self.date_filter(container)
        self.__condition_filter(container)
        self.summary_works(container.all_data)
        return container.all_data

    @staticmethod
    def __condition_filter(container: SimpleNamespace):
        result = [i for i in container.all_data if condition_filter(i)]
        container.all_data = result

    def summary_works(self, data: list[dict]):
        self.log.info(f"当前账号筛选作品数量: {len(data)}")

    def extract_batch(
            self,
            container: SimpleNamespace,
            data: SimpleNamespace) -> None:
        container.cache = container.template.copy()
        self.extract_works_info(container.cache, data)
        self.extract_account_info(container, data)
        self.extract_music(container.cache, data)
        self.extract_statistics(container.cache, data)
        self.extract_tags(container.cache, data)
        self._extract_extra_info(container.cache, data)
        self.extract_additional_info(container.cache, data)
        container.all_data.append(container.cache)

    def _extract_extra_info(self, item: dict, data: SimpleNamespace):
        if e := self.safe_extract(data, "anchor_info"):
            extra = dumps(
                e,
                ensure_ascii=False,
                indent=2,
                default=lambda x: vars(x))
        else:
            extra = ""
        item["extra"] = extra

    def _extract_commodity_data(self, item: dict, data: SimpleNamespace):
        pass

    def _extract_game_data(self, item: dict, data: SimpleNamespace):
        pass

    def extract_description(self, data: SimpleNamespace) -> str:
        # 2023/11/11: 抖音不再折叠过长的作品描述
        return self.safe_extract(data, "desc")
        # if len(desc := self.safe_extract(data, "desc")) < 107:
        #     return desc
        # long_desc = self.safe_extract(data, "share_info.share_link_desc")
        # return long_desc.split(
        #     "  ", 1)[-1].split("  %s", 1)[0].replace("# ", "#")

    def clean_description(self, desc: str) -> str:
        return self.cleaner.clear_spaces(self.cleaner.filter(desc))

    def format_date(self, data: SimpleNamespace, key: str = None) -> str:
        return strftime(
            self.date_format,
            localtime(
                self.safe_extract(data, key or "create_time") or None))

    def extract_works_info(self, item: dict, data: SimpleNamespace) -> None:
        item["id"] = self.safe_extract(data, "aweme_id")
        item["desc"] = self.clean_description(
            self.extract_description(data)) or item["id"]
        item["create_time"] = self.format_date(data)
        item["create_timestamp"] = self.safe_extract(data, "create_time")
        self._extract_text_extra(item, data)
        self.classifying_works(item, data)

    def classifying_works(self, item: dict, data: SimpleNamespace) -> None:
        if images := self.safe_extract(data, "images"):
            self.extract_image_info(item, data, images)
        elif images := self.safe_extract(data, "image_post_info"):
            self.extract_image_info_tiktok(item, data, images)
        else:
            self.extract_video_info(item, data)

    def extract_additional_info(self, item: dict, data: SimpleNamespace):
        item["height"] = self.safe_extract(data, "video.height", "-1")
        item["width"] = self.safe_extract(data, "video.width", "-1")
        item["ratio"] = self.safe_extract(data, "video.ratio")
        item["share_url"] = self.__generate_link(item["type"], item["id"])

    @staticmethod
    def __generate_link(type_: str, id_: str) -> str:
        match type_:
            case "视频":
                return f"https://www.douyin.com/video/{id_}"
            case "图集":
                return f"https://www.douyin.com/note/{id_}"
            case _:
                return ""

    @staticmethod
    def __clean_share_url(url: str) -> str:
        if not url:
            return url
        parsed_url = urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

    def extract_image_info(
            self,
            item: dict,
            data: SimpleNamespace,
            images: list) -> None:
        self.__set_blank_data(item, data)
        item["downloads"] = " ".join(
            self.safe_extract(
                i, 'url_list[-1]') for i in images)

    def extract_image_info_tiktok(
            self,
            item: dict,
            data: SimpleNamespace,
            images: SimpleNamespace) -> None:
        self.__set_blank_data(item, data)
        item["downloads"] = " ".join(self.safe_extract(
            i, "display_image.url_list[-1]") for i in images.images)

    def __set_blank_data(self, item: dict, data: SimpleNamespace, ):
        item["type"] = "图集"
        item["duration"] = "00:00:00"
        item["uri"] = ""
        self.extract_cover(item, data)

    def extract_video_info(self, item: dict, data: SimpleNamespace) -> None:
        item["type"] = "视频"
        item["downloads"] = self.safe_extract(
            data, "video.play_addr.url_list[-1]")
        item["duration"] = self._time_conversion(
            self.safe_extract(data, "video.duration", 0))
        item["uri"] = self.safe_extract(
            data, "video.play_addr.uri")
        self.extract_cover(item, data, True)

    @staticmethod
    def _time_conversion(time_: int) -> str:
        return f"{
        time_ //
        1000 //
        3600:0>2d}:{
        time_ //
        1000 %
        3600 //
        60:0>2d}:{
        time_ //
        1000 %
        3600 %
        60:0>2d}"

    def _extract_text_extra(self, item: dict, data: SimpleNamespace):
        text = [
            self.safe_extract(i, "hashtag_name")
            for i in self.safe_extract(
                data, "text_extra", []
            )
        ]
        item["text_extra"] = ", ".join(i for i in text if i)

    def extract_cover(
            self,
            item: dict,
            data: SimpleNamespace,
            has=False) -> None:
        if has:
            # 动态封面图链接
            item["dynamic_cover"] = self.safe_extract(
                data, "video.dynamic_cover.url_list[-1]")
            # 静态封面图链接
            item["origin_cover"] = self.safe_extract(
                data, "video.origin_cover.url_list[-1]")
        else:
            item["dynamic_cover"], item["origin_cover"] = "", ""

    def extract_music(self, item: dict, data: SimpleNamespace) -> None:
        if music_data := self.safe_extract(data, "music"):
            author = self.safe_extract(music_data, "author")
            title = self.safe_extract(music_data, "title")
            url = self.safe_extract(
                music_data, "play_url.url_list[-1]")  # 部分作品的音乐无法下载
        else:
            author, title, url = "", "", ""
        item["music_author"] = author
        item["music_title"] = title
        item["music_url"] = url

    def extract_statistics(self, item: dict, data: SimpleNamespace) -> None:
        data = self.safe_extract(data, "statistics")
        for i in (
                "digg_count",
                "comment_count",
                "collect_count",
                "share_count",
        ):
            item[i] = str(self.safe_extract(data, i, "-1"))

    def extract_tags(self, item: dict, data: SimpleNamespace) -> None:
        if not (t := self.safe_extract(data, "video_tag")):
            tags = ["", "", ""]
        else:
            tags = [self.safe_extract(i, "tag_name") for i in t]
        for tag, value in zip(("tag_1", "tag_2", "tag_3"), tags):
            item[tag] = value

    def extract_account_info(
            self,
            container: SimpleNamespace,
            data: SimpleNamespace,
            key="author",
    ) -> None:
        data = self.safe_extract(data, key)
        container.cache["uid"] = self.safe_extract(data, "uid")
        container.cache["sec_uid"] = self.safe_extract(data, "sec_uid")
        container.cache["short_id"] = self.safe_extract(data, "short_id")
        container.cache["unique_id"] = self.safe_extract(data, "unique_id")
        container.cache["signature"] = self.safe_extract(data, "signature")
        container.cache["user_age"] = self.safe_extract(data, "user_age", "-1")
        self.extract_nickname_info(container, data)

    def extract_nickname_info(self,
                              container: SimpleNamespace,
                              data: SimpleNamespace) -> None:
        if container.same:
            container.cache["nickname"] = container.name
            container.cache["mark"] = container.mark or container.name
        else:
            name = self.cleaner.filter_name(
                self.safe_extract(
                    data,
                    "nickname",
                    "已注销账号"),
                inquire=False,
                default="无效账号昵称", )
            container.cache["nickname"] = name
            container.cache["mark"] = name

    def preprocessing_data(self,
                           data: list[dict],
                           mark="",
                           post=True,
                           mix=False) -> tuple:
        item = self.generate_data_object(data[-1])
        mid = self.safe_extract(item, "mix_info.mix_id")
        id_ = self.safe_extract(item, "author.uid")
        name = self.cleaner.filter_name(self.safe_extract(
            item, "author.nickname", f"账号_{str(time())[:10]}"),
            default="无效账号昵称")
        title = self.cleaner.filter_name(self.safe_extract(
            item, "mix_info.mix_name", f"合集_{str(time())[:10]}"),
            inquire=mix,
            default="无效合集标题")
        mark = self.cleaner.filter_name(
            mark, inquire=False, default=title if mix else name)
        return id_, name.strip(), mid, title.strip(
        ), mark.strip(), data[:None if post else -1]

    def works(self, data: list[dict], recorder) -> list[dict]:
        container = SimpleNamespace(
            all_data=[],
            template={
                "collection_time": datetime.now().strftime(self.date_format),
            },
            cache=None,
            same=False,
        )
        [self.extract_batch(container, self.generate_data_object(item))
         for item in data]
        self._extract_item_records(container.all_data)
        self.record_data(recorder, container.all_data)
        self.__condition_filter(container)
        return container.all_data

    def comment(self, data: list[dict], recorder,
                source=False) -> tuple[list[dict], list]:
        if not any(data):
            return [{}], []
        container = SimpleNamespace(
            all_data=[],
            reply_ids=[],
            template={
                "collection_time": datetime.now().strftime(self.date_format),
            },
            cache=None,
            same=False,
        )
        if source:
            [self._extract_reply_ids(container, i) for i in data]
        else:
            [self._extract_comments_data(
                container, self.generate_data_object(i)) for i in data]
            self.record_data(recorder, container.all_data)
        return container.all_data, container.reply_ids

    def _extract_comments_data(
            self,
            container: SimpleNamespace,
            data: SimpleNamespace):
        container.cache = container.template.copy()
        container.cache["create_time"] = self.format_date(data)
        container.cache["ip_label"] = self.safe_extract(data, "ip_label", "未知")
        container.cache["text"] = self.safe_extract(data, "text")
        container.cache["image"] = self.safe_extract(
            data, "image_list[0].origin_url.url_list[-1]")
        container.cache["sticker"] = self.safe_extract(
            data, "sticker.static_url.url_list[-1]")
        container.cache["digg_count"] = str(
            self.safe_extract(data, "digg_count", "-1"))
        container.cache["reply_to_reply_id"] = self.safe_extract(
            data, "reply_to_reply_id")
        container.cache["reply_comment_total"] = str(
            self.safe_extract(data, "reply_comment_total", "0"))
        container.cache["reply_id"] = self.safe_extract(data, "reply_id")
        container.cache["cid"] = self.safe_extract(data, "cid")
        self.extract_account_info(container, data, "user")
        self._filter_reply_ids(container)
        container.all_data.append(container.cache)

    def _extract_reply_ids(self, container: SimpleNamespace, data: dict):
        cache = self.generate_data_object(data)
        container.cache = {
            "reply_comment_total": str(
                self.safe_extract(
                    cache, "reply_comment_total", "0")), "cid": self.safe_extract(
                cache, "cid")}
        self._filter_reply_ids(container)
        container.all_data.append(data)

    @staticmethod
    def _filter_reply_ids(container: SimpleNamespace):
        if container.cache["reply_comment_total"] != "0":
            container.reply_ids.append(container.cache["cid"])

    def live(self, data: list[dict], *args) -> list[dict]:
        container = SimpleNamespace(all_data=[])
        [self.extract_live_data(container,
                                self.generate_data_object(i)) for i in data]
        return container.all_data

    def extract_live_data(
            self,
            container: SimpleNamespace,
            data: SimpleNamespace):
        data = self.safe_extract(
            data, "data.data[0]") or self.safe_extract(
            data, "data.room")
        live_data = {"status": self.safe_extract(data, "status"),
                     "nickname": self.safe_extract(data, "owner.nickname"),
                     "title": self.safe_extract(data, "title"),
                     "flv_pull_url": vars(self.safe_extract(data, "stream_url.flv_pull_url", SimpleNamespace())),
                     "hls_pull_url_map": vars(
                         self.safe_extract(data, "stream_url.hls_pull_url_map", SimpleNamespace())),
                     "cover": self.safe_extract(data, "cover.url_list[-1]"),
                     "total_user_str": self.safe_extract(data, "stats.total_user_str"),
                     "user_count_str": self.safe_extract(data, "stats.user_count_str"), }
        container.all_data.append(live_data)

    def user(self, data: list[dict], recorder) -> list[dict]:
        container = SimpleNamespace(
            all_data=[],
            cache=None,
            template={
                "collection_time": datetime.now().strftime(self.date_format),
            },
        )
        [self._extract_user_data(container,
                                 self.generate_data_object(i)) for i in data]
        self.record_data(recorder, container.all_data)
        return container.all_data

    def _extract_user_data(
            self,
            container: SimpleNamespace,
            data: SimpleNamespace):
        container.cache = container.template.copy()
        container.cache["avatar"] = self.safe_extract(
            data, "avatar_larger.url_list[0]")
        container.cache["city"] = self.safe_extract(data, "city")
        container.cache["country"] = self.safe_extract(data, "country")
        container.cache["district"] = self.safe_extract(data, "district")
        container.cache["favoriting_count"] = str(
            self.safe_extract(data, "favoriting_count", "-1"))
        container.cache["follower_count"] = str(
            self.safe_extract(data, "follower_count", "-1"))
        container.cache["max_follower_count"] = str(
            self.safe_extract(data, "max_follower_count", "-1"))
        container.cache["following_count"] = str(
            self.safe_extract(data, "following_count", "-1"))
        container.cache["total_favorited"] = str(
            self.safe_extract(data, "total_favorited", "-1"))
        container.cache["gender"] = {1: "男", 2: "女"}.get(
            self.safe_extract(data, "gender"), "未知")
        container.cache["ip_location"] = self.safe_extract(data, "ip_location")
        container.cache["nickname"] = self.safe_extract(data, "nickname")
        container.cache["province"] = self.safe_extract(data, "province")
        container.cache["school_name"] = self.safe_extract(data, "school_name")
        container.cache["sec_uid"] = self.safe_extract(data, "sec_uid")
        container.cache["signature"] = self.safe_extract(data, "signature")
        container.cache["uid"] = self.safe_extract(data, "uid")
        container.cache["unique_id"] = self.safe_extract(data, "unique_id")
        container.cache["user_age"] = str(
            self.safe_extract(data, "user_age", "-1"))
        container.cache["cover"] = self.safe_extract(
            data, "cover_url[0].url_list[-1]")
        container.cache["short_id"] = self.safe_extract(data, "short_id")
        container.cache["aweme_count"] = str(
            self.safe_extract(data, "aweme_count", "-1"))
        container.cache["verify"] = self.safe_extract(
            data, "custom_verify", "无")
        container.cache["enterprise"] = self.safe_extract(
            data, "enterprise_verify_reason", "无")
        container.cache["url"] = f"https://www.douyin.com/user/{
        container.cache["sec_uid"]}"
        container.all_data.append(container.cache)

    def search(self, data: list[dict], recorder, tab: int) -> list[dict]:
        if tab in {0, 1}:
            return self.search_general(data, recorder)
        elif tab == 2:
            return self.search_user(data, recorder)
        elif tab == 3:
            return self.search_live(data, recorder)

    def search_general(self, data: list[dict], recorder) -> list[dict]:
        container = SimpleNamespace(
            all_data=[],
            cache=None,
            template={
                "collection_time": datetime.now().strftime(self.date_format),
            },
            same=False,
        )
        [self._search_result_classify(
            container, self.generate_data_object(i)) for i in data]
        self.record_data(recorder, container.all_data)
        return container.all_data

    def _search_result_classify(
            self,
            container: SimpleNamespace,
            data: SimpleNamespace):
        if d := self.safe_extract(data, "aweme_info"):
            self.extract_batch(container, d)
        elif d := self.safe_extract(data, "aweme_mix_info.mix_items"):
            [self.extract_batch(container, i) for i in d]
        elif d := self.safe_extract(data, "card_info.attached_info.aweme_list"):
            [self.extract_batch(container, i) for i in d]
        elif d := self.safe_extract(data, "user_list[0].items"):
            [self.extract_batch(container, i) for i in d]
        # elif d := self.safe_extract(data, "user_list.user_info"):
        #     pass
        # elif d := self.safe_extract(data, "music_list"):
        #     pass
        # elif d := self.safe_extract(data, "common_aladdin"):
        #     pass
        self.log.error(f"Unreported search results: {data}", False)

    def search_user(
            self,
            data: list[dict],
            recorder) -> list[dict]:
        container = SimpleNamespace(
            all_data=[],
            cache=None,
            template={
                "collection_time": datetime.now().strftime(self.date_format),
            },
        )
        [self._deal_search_user_live(container, self.generate_data_object(
            i["user_info"])) for i in data]
        self.record_data(recorder, container.all_data)
        return container.all_data

    def _deal_search_user_live(self,
                               container: SimpleNamespace,
                               data: SimpleNamespace,
                               user=True):
        if user:
            container.cache = container.template.copy()
        container.cache["avatar"] = self.safe_extract(
            data, f"{'avatar_thumb' if user else 'avatar_larger'}.url_list[0]")
        container.cache["nickname"] = self.safe_extract(data, "nickname")
        container.cache["sec_uid"] = self.safe_extract(data, "sec_uid")
        container.cache["signature"] = self.safe_extract(data, "signature")
        container.cache["uid"] = self.safe_extract(data, "uid")
        container.cache["short_id"] = self.safe_extract(data, "short_id")
        container.cache["verify"] = self.safe_extract(
            data, "custom_verify", "无")
        container.cache["enterprise"] = self.safe_extract(
            data, "enterprise_verify_reason", "无")
        if user:
            container.cache["follower_count"] = str(
                self.safe_extract(data, "follower_count", "-1"))
            container.cache["total_favorited"] = str(
                self.safe_extract(data, "total_favorited", "-1"))
            container.cache["unique_id"] = self.safe_extract(data, "unique_id")
            container.all_data.append(container.cache)
        # else:
        #     pass

    def search_live(
            self,
            data: list[dict],
            recorder) -> list[dict]:
        container = SimpleNamespace(
            all_data=[],
            cache=None,
            template={
                "collection_time": datetime.now().strftime(self.date_format),
            },
        )
        [self._deal_search_live(
            container, self.generate_data_object(i["lives"])) for i in data]
        self.record_data(recorder, container.all_data)
        return container.all_data

    def _deal_search_live(self,
                          container: SimpleNamespace,
                          data: SimpleNamespace):
        container.cache = container.template.copy()
        self._deal_search_user_live(
            container, self.safe_extract(
                data, "author"), False)
        container.cache["room_id"] = self.safe_extract(data, "aweme_id")
        container.all_data.append(container.cache)

    def hot(self, data: list[dict], recorder) -> list[dict]:
        all_data = []
        [self._deal_hot_data(all_data, self.generate_data_object(i))
         for i in data]
        self.record_data(recorder, all_data)
        return all_data

    def _deal_hot_data(self, container: list, data: SimpleNamespace):
        cache = {
            "position": str(self.safe_extract(data, "position", "-1")),
            "sentence_id": self.safe_extract(data, "sentence_id"),
            "word": self.safe_extract(data, "word"),
            "video_count": str(self.safe_extract(data, "video_count", "-1")),
            "event_time": self.format_date(data, "event_time"),
            "view_count": str(self.safe_extract(data, "view_count", "-1")),
            "hot_value": str(self.safe_extract(data, "hot_value", "-1")),
            "cover": self.safe_extract(data, "word_cover.url_list[-1]"),
        }
        container.append(cache)

    def record_data(self, record, data: list[dict]):
        for i in data:
            record.save(self.extract_values(record, i))

    @staticmethod
    def extract_values(record, data: dict) -> list:
        return [data[key] for key in record.field_keys]

    @staticmethod
    def date_filter(container: SimpleNamespace):
        # print("前", len(container.all_data))  # 调试代码
        result = []
        for item in container.all_data:
            create_time = datetime.fromtimestamp(
                item["create_timestamp"]).date()
            if container.earliest <= create_time <= container.latest:
                result.append(item)
            # else:
            #     print("丢弃", item)  # 调试代码
        # print("后", len(result))  # 调试代码
        container.all_data = result

    def source_date_filter(
            self,
            data: list[dict],
            earliest,
            latest) -> list[dict]:
        result = []
        for item in data:
            create_time = datetime.fromtimestamp(
                item.get("create_time", 0)).date()
            if earliest <= create_time <= latest:
                result.append(item)
        self.summary_works(result)
        return result

    @staticmethod
    def extract_mix_id(data: dict) -> str:
        data = Extractor.generate_data_object(data)
        return Extractor.safe_extract(data, "mix_info.mix_id")

    def _extract_item_records(self, data: list[dict]):
        for i in data:
            self.log.info(f"{i['type']} {i['id']} 数据提取成功", False)
