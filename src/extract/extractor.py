from datetime import datetime
from json import dumps
from time import localtime
from time import strftime
from time import time
from types import SimpleNamespace
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from src.custom import condition_filter
from src.tools import TikTokDownloaderError

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["Extractor"]


class Extractor:
    statistics_keys = (
        "digg_count",
        "comment_count",
        "collect_count",
        "share_count",
        "play_count",
    )
    detail_necessary_keys = "id"
    comment_necessary_keys = "cid"
    user_necessary_keys = "sec_uid"

    def __init__(self, params: "Parameter"):
        self.log = params.logger
        self.date_format = params.date_format
        self.cleaner = params.CLEANER
        self.type = {
            "batch": self.__batch,
            "detail": self.__detail,
            "comment": self.__comment,
            "live": self.__live,
            "user": self.__user,
            "search": self.__search,
            "hot": self.__hot,
            "music": self.__music,
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
    def get_user_info_tiktok(data: dict) -> dict:
        try:
            return {
                "nickname": data["user"]["nickname"],
                "sec_uid": data["user"]["secUid"],
                "uid": data["user"]["id"],
            }
        except (KeyError, TypeError):
            return {}

    @staticmethod
    def generate_data_object(
            data: dict | list) -> SimpleNamespace | list[SimpleNamespace]:
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

    async def run(
            self,
            data: list[dict],
            recorder,
            type_="detail",
            tiktok=False,
            **kwargs) -> list[dict]:
        if type_ not in self.type.keys():
            raise ValueError
        return await self.type[type_](data, recorder, tiktok, **kwargs)

    async def __batch(
            self,
            data: list[dict],
            recorder,
            tiktok: bool,
            name: str,
            mark: str,
            earliest,
            latest,
            same=True,
    ) -> list[dict]:
        """批量下载作品"""
        container = SimpleNamespace(
            all_data=[],
            template={
                "collection_time": datetime.now().strftime(self.date_format),
            },
            cache=None,
            name=name,
            mark=mark,
            same=same,  # 是否相同作者
            earliest=earliest,
            latest=latest,
        )
        self.__platform_classify_detail(data, container, tiktok, )
        container.all_data = self.__clean_extract_data(
            container.all_data, self.detail_necessary_keys)
        self.__extract_item_records(container.all_data)
        await self.__record_data(recorder, container.all_data)
        self.__date_filter(container)
        self.__condition_filter(container)
        self.__summary_detail(container.all_data)
        return container.all_data

    @staticmethod
    def __condition_filter(container: SimpleNamespace):
        """自定义筛选作品"""
        result = [i for i in container.all_data if condition_filter(i)]
        container.all_data = result

    def __summary_detail(self, data: list[dict]):
        """汇总作品数量"""
        self.log.info(f"当前账号筛选作品数量: {len(data)}")

    def __extract_batch(
            self,
            container: SimpleNamespace,
            data: SimpleNamespace,
    ) -> None:
        """批量提取作品信息"""
        container.cache = container.template.copy()
        self.__extract_detail_info(container.cache, data)
        self.__extract_account_info(container, data)
        self.__extract_music(container.cache, data)
        self.__extract_statistics(container.cache, data)
        self.__extract_tags(container.cache, data)
        self.__extract_extra_info(container.cache, data)
        self.__extract_additional_info(container.cache, data)
        container.all_data.append(container.cache)

    def __extract_batch_tiktok(
            self,
            container: SimpleNamespace,
            data: SimpleNamespace,
    ) -> None:
        """批量提取作品信息"""
        container.cache = container.template.copy()
        self.__extract_detail_info_tiktok(container.cache, data)
        self.__extract_account_info_tiktok(container, data)
        self.__extract_music(container.cache, data, True)
        self.__extract_statistics_tiktok(container.cache, data)
        self.__extract_tags_tiktok(container.cache, data)
        self.__extract_extra_info_tiktok(container.cache, data)
        self.__extract_additional_info(container.cache, data, True)
        container.all_data.append(container.cache)

    def __extract_extra_info(self, item: dict, data: SimpleNamespace):
        if e := self.safe_extract(data, "anchor_info"):
            extra = dumps(
                e,
                ensure_ascii=False,
                indent=2,
                default=lambda x: vars(x))
        else:
            extra = ""
        item["extra"] = extra

    def __extract_extra_info_tiktok(self, item: dict, data: SimpleNamespace):
        # if e := self.safe_extract(data, "anchor_info"):
        #     extra = dumps(
        #         e,
        #         ensure_ascii=False,
        #         indent=2,
        #         default=lambda x: vars(x))
        # else:
        #     extra = ""
        item["extra"] = ""

    def __extract_commodity_data(self, item: dict, data: SimpleNamespace):
        pass

    def __extract_game_data(self, item: dict, data: SimpleNamespace):
        pass

    def __extract_description(self, data: SimpleNamespace) -> str:
        # 2023/11/11: 抖音不再折叠过长的作品描述
        return self.safe_extract(data, "desc")
        # if len(desc := self.safe_extract(data, "desc")) < 107:
        #     return desc
        # long_desc = self.safe_extract(data, "share_info.share_link_desc")
        # return long_desc.split(
        #     "  ", 1)[-1].split("  %s", 1)[0].replace("# ", "#")

    def __clean_description(self, desc: str) -> str:
        return self.cleaner.clear_spaces(self.cleaner.filter(desc))

    def __format_date(self, data: int, ) -> str:
        return strftime(
            self.date_format,
            localtime(data or None),
        )

    def __extract_detail_info(self, item: dict, data: SimpleNamespace) -> None:
        item["id"] = self.safe_extract(data, "aweme_id")
        item["desc"] = self.__clean_description(
            self.__extract_description(data)) or item["id"]
        item["create_timestamp"] = self.safe_extract(data, "create_time")
        item["create_time"] = self.__format_date(item["create_timestamp"])
        self.__extract_text_extra(item, data)
        self.__classifying_detail(item, data)

    def __extract_detail_info_tiktok(
            self,
            item: dict,
            data: SimpleNamespace,
    ) -> None:
        item["id"] = self.safe_extract(data, "id")
        item["desc"] = self.__clean_description(
            self.__extract_description(data)) or item["id"]
        item["create_timestamp"] = self.safe_extract(data, "createTime", )
        item["create_time"] = self.__format_date(item["create_timestamp"])
        self.__extract_text_extra_tiktok(item, data)
        self.__classifying_detail_tiktok(item, data)

    def __classifying_detail(self, item: dict, data: SimpleNamespace) -> None:
        if images := self.safe_extract(data, "images"):
            self.__extract_image_info(item, data, images)
        else:
            self.__extract_video_info(item, data)

    def __classifying_detail_tiktok(
            self,
            item: dict,
            data: SimpleNamespace) -> None:
        if images := self.safe_extract(data, "imagePost.images"):
            self.__extract_image_info_tiktok(item, data, images)
        else:
            self.__extract_video_info_tiktok(item, data)

    def __extract_additional_info(
            self,
            item: dict,
            data: SimpleNamespace,
            tiktok=False,
    ):
        item["height"] = self.safe_extract(data, "video.height", "-1")
        item["width"] = self.safe_extract(data, "video.width", "-1")
        item["ratio"] = self.safe_extract(data, "video.ratio")
        item["share_url"] = self.__generate_link(
            item["type"], item["id"], item["unique_id"] if tiktok else None)

    @staticmethod
    def __generate_link(type_: str, id_: str, unique_id: str = None, ) -> str:
        match bool(unique_id), type_:
            case True, "视频":
                return f"https://www.tiktok.com/@{unique_id}/video/{id_}"
            case True, "图集":
                return f"https://www.tiktok.com/@{unique_id}/photo/{id_}"
            case False, "视频":
                return f"https://www.douyin.com/video/{id_}"
            case False, "图集":
                return f"https://www.douyin.com/note/{id_}"
            case _:
                return ""

    @staticmethod
    def __clean_share_url(url: str) -> str:
        if not url:
            return url
        parsed_url = urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

    def __extract_image_info(
            self,
            item: dict,
            data: SimpleNamespace,
            images: list) -> None:
        self.__set_blank_data(item, data)
        item["downloads"] = " ".join(
            self.safe_extract(
                i, 'url_list[-1]') for i in images)

    def __extract_image_info_tiktok(
            self,
            item: dict,
            data: SimpleNamespace,
            images: list) -> None:
        self.__set_blank_data(item, data)
        item["downloads"] = " ".join(self.safe_extract(
            i, "imageURL.urlList[0]") for i in images)

    def __set_blank_data(self, item: dict, data: SimpleNamespace, ):
        item["type"] = "图集"
        item["duration"] = "00:00:00"
        item["uri"] = ""
        self.__extract_cover(item, data)

    def __extract_video_info(self, item: dict, data: SimpleNamespace) -> None:
        item["type"] = "视频"
        item["downloads"] = self.safe_extract(
            data, "video.play_addr.url_list[0]")
        item["duration"] = self.time_conversion(
            self.safe_extract(data, "video.duration", 0))
        item["uri"] = self.safe_extract(
            data, "video.play_addr.uri")
        self.__extract_cover(item, data, True)

    def __extract_video_info_tiktok(
            self,
            item: dict,
            data: SimpleNamespace) -> None:
        item["type"] = "视频"
        item["downloads"] = self.safe_extract(
            data, "video.playAddr")
        item["duration"] = self.time_conversion_tiktok(
            self.safe_extract(data, "video.duration", 0))
        item["uri"] = self.safe_extract(
            data, "video.bitrateInfo[0].PlayAddr.Uri")
        self.__extract_cover_tiktok(item, data, True)

    @staticmethod
    def time_conversion(time_: int) -> str:
        second = time_ // 1000
        return f"{second // 3600:0>2d}:{second % 3600 // 60:0>2d}:{second % 3600 % 60:0>2d}"

    @staticmethod
    def time_conversion_tiktok(seconds: int) -> str:
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return '{:02d}:{:02d}:{:02d}'.format(
            int(hours), int(minutes), int(seconds))

    def __extract_text_extra(self, item: dict, data: SimpleNamespace):
        """作品标签"""
        text = [
            self.safe_extract(i, "hashtag_name")
            for i in self.safe_extract(
                data, "text_extra", []
            )
        ]
        item["text_extra"] = ", ".join(i for i in text if i)

    def __extract_text_extra_tiktok(self, item: dict, data: SimpleNamespace):
        """作品标签"""
        text = [
            self.safe_extract(i, "hashtagName")
            for i in self.safe_extract(
                data, "textExtra", []
            )
        ]
        item["text_extra"] = ", ".join(i for i in text if i)

    def __extract_cover(
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

    def __extract_cover_tiktok(
            self,
            item: dict,
            data: SimpleNamespace,
            has=False) -> None:
        if has:
            # 动态封面图链接
            item["dynamic_cover"] = self.safe_extract(
                data, "video.dynamicCover")
            # 静态封面图链接
            item["origin_cover"] = self.safe_extract(
                data, "video.originCover")
        else:
            item["dynamic_cover"], item["origin_cover"] = "", ""

    def __extract_music(
            self,
            item: dict,
            data: SimpleNamespace,
            tiktok=False,
    ) -> None:
        if music_data := self.safe_extract(data, "music"):
            if tiktok:
                author = self.safe_extract(music_data, "authorName")
                title = self.safe_extract(music_data, "title")
                url = self.safe_extract(
                    music_data, "playUrl")
            else:
                author = self.safe_extract(music_data, "author")
                title = self.safe_extract(music_data, "title")
                url = self.safe_extract(
                    music_data, "play_url.url_list[-1]")  # 部分作品的音乐无法下载

        else:
            author, title, url = "", "", ""
        item["music_author"] = author
        item["music_title"] = title
        item["music_url"] = url

    def __extract_statistics(self, item: dict, data: SimpleNamespace) -> None:
        data = self.safe_extract(data, "statistics")
        for i in self.statistics_keys:
            item[i] = str(self.safe_extract(data, i, "-1"))

    def __extract_statistics_tiktok(
            self,
            item: dict,
            data: SimpleNamespace) -> None:
        data = self.safe_extract(data, "stats")
        for i, j in enumerate((
                "diggCount",
                "commentCount",
                "collectCount",
                "shareCount",
                "playCount",
        )):
            item[self.statistics_keys[i]] = str(
                self.safe_extract(data, j, "-1"))

    def __extract_tags(self, item: dict, data: SimpleNamespace) -> None:
        if not (t := self.safe_extract(data, "video_tag")):
            tags = []
        else:
            tags = [self.safe_extract(i, "tag_name") for i in t]
        item["tag"] = ", ".join(tags)

    def __extract_tags_tiktok(self, item: dict, data: SimpleNamespace) -> None:
        if not (t := self.safe_extract(data, "textExtra")):
            tags = []
        else:
            tags = [self.safe_extract(i, "hashtagName") for i in t]
        item["tag"] = ", ".join(tags)

    def __extract_account_info(
            self,
            container: SimpleNamespace,
            data: SimpleNamespace,
            key="author",
    ) -> None:
        data = self.safe_extract(data, key)
        container.cache["uid"] = self.safe_extract(data, "uid")
        container.cache["sec_uid"] = self.safe_extract(data, "sec_uid")
        # container.cache["short_id"] = self.safe_extract(data, "short_id")
        container.cache["unique_id"] = self.safe_extract(data, "unique_id", )
        container.cache["signature"] = self.safe_extract(data, "signature")
        container.cache["user_age"] = self.safe_extract(data, "user_age", "-1")
        self.__extract_nickname_info(container, data)

    def __extract_account_info_tiktok(
            self,
            container: SimpleNamespace,
            data: SimpleNamespace,
            key="author",
    ) -> None:
        data = self.safe_extract(data, key)
        container.cache["uid"] = self.safe_extract(data, "id")
        container.cache["sec_uid"] = self.safe_extract(data, "secUid")
        container.cache["unique_id"] = self.safe_extract(data, "uniqueId")
        container.cache["signature"] = self.safe_extract(data, "signature")
        container.cache["user_age"] = "-1"
        self.__extract_nickname_info(container, data)

    def __extract_nickname_info(self,
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
                           id_: str,
                           mark="",
                           post=True,
                           mix=False,
                           tiktok=False,
                           title=None,
                           collect_id=None,
                           ) -> tuple:
        if tiktok:
            params = {
                "sec_uid": "author.secUid",
                "mix_id": "playlistId",
                "uid": "author.id",
                "nickname": "author.nickname",
                "mix_name": "playlistId",
                "title": title,
            }
        else:
            params = {
                "sec_uid": "author.sec_uid",
                "mix_id": "mix_info.mix_id",
                "uid": "author.uid",
                "nickname": "author.nickname",
                "mix_name": "mix_info.mix_name",
                "title": "",
            }
        return self.__preprocessing_data(
            data,
            id_,
            mark,
            post,
            mix,
            **params,
            collect_id=collect_id,
        )

    def __preprocessing_data(self,
                             data: list[dict],
                             id_: str,
                             mark="",
                             post=True,
                             mix=False,
                             sec_uid="",
                             mix_id="",
                             uid="",
                             nickname="",
                             mix_name="",
                             title="",
                             collect_id=None
                             ) -> tuple:
        for item in data:
            item = self.generate_data_object(item)
            if id_ in {
                self.safe_extract(item, sec_uid),
                mid := self.safe_extract(item, mix_id),
            }:
                break
        else:
            raise TikTokDownloaderError("提取账号信息或合集信息失败，请向作者反馈！")
        id_ = self.safe_extract(item, uid)
        name = self.cleaner.filter_name(self.safe_extract(
            item, nickname, f"账号_{str(time())[:10]}"),
            default="无效账号昵称")
        title = self.cleaner.filter_name(title or self.safe_extract(
            item, mix_name, f"合集_{str(time())[:10]}"),
                                         inquire=mix,
                                         default="无效合集标题")
        mark = self.cleaner.filter_name(
            mark, inquire=False, default=title if mix else name)
        return id_, name.strip(), collect_id or mid, title.strip(
        ), mark.strip(), data[:None if post else -1]

    def __platform_classify_detail(
            self,
            data: list[dict],
            container: SimpleNamespace,
            tiktok: bool) -> None:
        if tiktok:
            [self.__extract_batch_tiktok(
                container, self.generate_data_object(item)) for item in data]
        else:
            [self.__extract_batch(container, self.generate_data_object(item))
             for item in data]

    async def __detail(
            self,
            data: list[dict],
            recorder,
            tiktok: bool,
    ) -> list[dict]:
        container = SimpleNamespace(
            all_data=[],
            template={
                "collection_time": datetime.now().strftime(self.date_format),
            },
            cache=None,
            same=False,
        )
        self.__platform_classify_detail(data, container, tiktok, )
        container.all_data = self.__clean_extract_data(
            container.all_data, self.detail_necessary_keys)
        self.__extract_item_records(container.all_data)
        await self.__record_data(recorder, container.all_data)
        self.__condition_filter(container)
        return container.all_data

    async def __comment(self, data: list[dict], recorder, tiktok: bool,
                        source=False) -> list[dict]:
        if not any(data):
            return []
        container = SimpleNamespace(
            all_data=[],
            template={
                "collection_time": datetime.now().strftime(self.date_format),
            },
            cache=None,
            same=False,
        )
        if source:
            container.all_data = data
        else:
            [self.__extract_comments_data(
                container, self.generate_data_object(i)) for i in data]
            container.all_data = self.__clean_extract_data(
                container.all_data, self.comment_necessary_keys)
            await self.__record_data(recorder, container.all_data)
        return container.all_data

    def __extract_comments_data(
            self,
            container: SimpleNamespace,
            data: SimpleNamespace):
        container.cache = container.template.copy()
        container.cache["create_timestamp"] = self.safe_extract(
            data, "create_time")
        container.cache["create_time"] = self.__format_date(
            container.cache["create_timestamp"])
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
        self.__extract_account_info(container, data, "user")
        container.all_data.append(container.cache)

    @classmethod
    def extract_reply_ids(cls, data: list[dict]) -> list[str]:
        container = SimpleNamespace(
            reply_ids=[],
            cache=None,
        )
        for item in data:
            item = cls.generate_data_object(item)
            container.cache = {
                "reply_comment_total": str(
                    cls.safe_extract(
                        item, "reply_comment_total", "0")),
                "cid": cls.safe_extract(item, "cid")}
            cls.__filter_reply_ids(container)
        return container.reply_ids

    @staticmethod
    def __filter_reply_ids(container: SimpleNamespace):
        if container.cache["reply_comment_total"] != "0":
            container.reply_ids.append(container.cache["cid"])

    async def __live(
            self,
            data: list[dict],
            recorder,
            tiktok: bool,
            *args) -> list[dict]:
        container = SimpleNamespace(all_data=[])
        if tiktok:
            [self.__extract_live_data_tiktok(
                container, self.generate_data_object(i)) for i in data]
        else:
            [self.__extract_live_data(
                container, self.generate_data_object(i)) for i in data]
        return container.all_data

    def __extract_live_data(
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

    def __extract_live_data_tiktok(
            self,
            container: SimpleNamespace,
            data: SimpleNamespace):
        data = self.safe_extract(data, "data")
        live_data = {
            "create_time": datetime.fromtimestamp(t) if (
                t := self.safe_extract(data, "create_time")) else "未知",
            "id_str": self.safe_extract(data, "id_str"),
            "like_count": self.safe_extract(data, "like_count"),
            "nickname": self.safe_extract(data, "owner.nickname"),
            "display_id": self.safe_extract(data, "owner.display_id"),
            "title": self.safe_extract(data, "title"),
            "user_count": self.safe_extract(data, "user_count"),
            "flv_pull_url": vars(self.safe_extract(data, "stream_url.flv_pull_url")),
            "message": self.safe_extract(data, "message"),
            "prompts": self.safe_extract(data, "prompts"),
        }
        container.all_data.append(live_data)

    async def __user(
            self,
            data: list[dict],
            recorder,
            tiktok: bool,
    ) -> list[dict]:
        container = SimpleNamespace(
            all_data=[],
            cache=None,
            template={
                "collection_time": datetime.now().strftime(self.date_format),
            },
        )
        [self.__extract_user_data(container,
                                  self.generate_data_object(i)) for i in data]
        container.all_data = self.__clean_extract_data(
            container.all_data, self.user_necessary_keys)
        await self.__record_data(recorder, container.all_data)
        return container.all_data

    def __extract_user_data(
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
        container.cache["url"] = f"https: // www.douyin.com / user / {container.cache['sec_uid']}"
        container.all_data.append(container.cache)

    async def __search(
            self,
            data: list[dict],
            recorder,
            tiktok: bool,
            tab: int) -> list[dict]:
        if tab in {0, 1}:
            return await self.__search_general(data, recorder)
        elif tab == 2:
            return await self.__search_user(data, recorder)
        elif tab == 3:
            return await self.__search_live(data, recorder)

    async def __search_general(self, data: list[dict], recorder) -> list[dict]:
        container = SimpleNamespace(
            all_data=[],
            cache=None,
            template={
                "collection_time": datetime.now().strftime(self.date_format),
            },
            same=False,
        )
        [self.__search_result_classify(
            container, self.generate_data_object(i)) for i in data]
        await self.__record_data(recorder, container.all_data)
        return container.all_data

    def __search_result_classify(
            self,
            container: SimpleNamespace,
            data: SimpleNamespace):
        if d := self.safe_extract(data, "aweme_info"):
            self.__extract_batch(container, d)
        elif d := self.safe_extract(data, "aweme_mix_info.mix_items"):
            [self.__extract_batch(container, i) for i in d]
        elif d := self.safe_extract(data, "card_info.attached_info.aweme_list"):
            [self.__extract_batch(container, i) for i in d]
        elif d := self.safe_extract(data, "user_list[0].items"):
            [self.__extract_batch(container, i) for i in d]
        # elif d := self.safe_extract(data, "user_list.user_info"):
        #     pass
        # elif d := self.safe_extract(data, "music_list"):
        #     pass
        # elif d := self.safe_extract(data, "common_aladdin"):
        #     pass
        self.log.error(f"Unreported search results: {data}", False)

    async def __search_user(
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
        [self.__deal_search_user_live(container, self.generate_data_object(
            i["user_info"])) for i in data]
        await self.__record_data(recorder, container.all_data)
        return container.all_data

    def __deal_search_user_live(self,
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

    async def __search_live(
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
        [self.__deal_search_live(
            container, self.generate_data_object(i["lives"])) for i in data]
        await self.__record_data(recorder, container.all_data)
        return container.all_data

    def __deal_search_live(self,
                           container: SimpleNamespace,
                           data: SimpleNamespace):
        container.cache = container.template.copy()
        self.__deal_search_user_live(
            container, self.safe_extract(
                data, "author"), False)
        container.cache["room_id"] = self.safe_extract(data, "aweme_id")
        container.all_data.append(container.cache)

    async def __hot(
            self,
            data: list[dict],
            recorder,
            tiktok: bool,
    ) -> list[dict]:
        all_data = []
        [self.__deal_hot_data(all_data, self.generate_data_object(i))
         for i in data]
        await self.__record_data(recorder, all_data)
        return all_data

    def __deal_hot_data(self, container: list, data: SimpleNamespace):
        cache = {
            "position": str(self.safe_extract(data, "position", "-1")),
            "sentence_id": self.safe_extract(data, "sentence_id"),
            "word": self.safe_extract(data, "word"),
            "video_count": str(self.safe_extract(data, "video_count", "-1")),
            "event_time": self.__format_date(self.safe_extract(data, "event_time")),
            "view_count": str(self.safe_extract(data, "view_count", "-1")),
            "hot_value": str(self.safe_extract(data, "hot_value", "-1")),
            "cover": self.safe_extract(data, "word_cover.url_list[-1]"),
        }
        container.append(cache)

    async def __record_data(self, record, data: list[dict]):
        for i in data:
            await record.save(self.__extract_values(record, i))

    @staticmethod
    def __extract_values(record, data: dict) -> list:
        return [data[key] for key in record.field_keys]

    @staticmethod
    def __date_filter(container: SimpleNamespace):
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
        self.__summary_detail(result)
        return result

    @classmethod
    def extract_mix_id(cls, data: dict) -> str:
        data = cls.generate_data_object(data)
        return cls.safe_extract(data, "mix_info.mix_id")

    def __extract_item_records(self, data: list[dict]):
        for i in data:
            self.log.info(f"{i['type']} {i['id']} 数据提取成功", False)

    @classmethod
    def extract_mix_collect_info(cls, data: list[dict]) -> list[dict]:
        data = cls.generate_data_object(data)
        return [
            {
                "title": Extractor.safe_extract(i, "mix_name"),
                "id": Extractor.safe_extract(i, "mix_id"),
            }
            for i in data
        ]

    @classmethod
    def extract_collects_info(cls, data: list[dict]) -> list[dict]:
        data = cls.generate_data_object(data)
        return [
            {
                "name": Extractor.safe_extract(i, "collects_name"),
                "id": Extractor.safe_extract(i, "collects_id_str"),
            }
            for i in data
        ]

    @staticmethod
    def __clean_extract_data(data: list[dict], key: str) -> list[dict]:
        return [i for i in data if i.get(key)]

    async def __music(self,
                      data: list[dict],
                      recorder,
                      tiktok=False,
                      ) -> list[dict]:
        """暂不记录收藏音乐数据"""
        container = SimpleNamespace(
            all_data=[],
            template={
                "collection_time": datetime.now().strftime(self.date_format),
            },
            cache=None,
            same=False,
        )
        [self.__extract_collection_music(
            container, self.generate_data_object(item)) for item in data]
        return container.all_data

    def __extract_collection_music(self,
                                   container: SimpleNamespace,
                                   data: SimpleNamespace, ):
        container.cache = container.template.copy()
        container.cache["id"] = self.safe_extract(data, "id_str")
        container.cache["title"] = self.safe_extract(data, "title")
        container.cache["author"] = self.safe_extract(data, "author")
        container.cache["album"] = self.safe_extract(data, "album")
        container.cache["cover"] = self.safe_extract(
            data, "cover_hd.url_list[0]")
        container.cache["download"] = self.safe_extract(
            data, "play_url.url_list[0]")
        container.cache["duration"] = self.time_conversion(
            self.safe_extract(data, "duration", 0))
        container.all_data.append(container.cache)
