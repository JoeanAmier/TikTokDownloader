from datetime import datetime
from time import localtime
from time import strftime
from types import SimpleNamespace

from src.Customizer import conditional_filtering

__all__ = ["Extractor"]


class Extractor:
    def __init__(self, params):
        self.log = params.logger
        self.date_format = params.date_format
        self.clean = params.clean
        self.type = {
            "user": self.user,
            "works": self.works,
            "comment": self.comment,
            "live": self.live,
            "search_general": self.search_general,
            "search_user": self.search_user,
            "hot": self.hot,
        }

    @staticmethod
    def get_sec_uid(data: dict) -> str:
        try:
            return data["author"]["sec_uid"]
        except KeyError:
            return ""

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
    def safe_extract(data: SimpleNamespace, attribute_chain: str, default=""):
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

    def user(
            self,
            data: list[dict],
            recorder,
            earliest,
            latest,
            post=True,
            mark="",
    ) -> tuple[str, str, list[dict]]:
        container = SimpleNamespace(
            all_data=[],
            template={
                "collection_time": datetime.now().strftime(self.date_format),
            },
            cache=None,
            nickname="",
            mark=self.clean.clean_name(mark),
            post=post,
            earliest=earliest,
            latest=latest,
        )
        data = conditional_filtering(data)
        if post:
            [self.extract_user(container, self.generate_data_object(item))
             for item in data]
        else:
            [self.extract_user(container, self.generate_data_object(
                item)) for item in data[:-1]]
            self.extract_not_post(container,
                                  self.generate_data_object(data[-1]))
        self.date_filter(container)
        self.summary_works(container.all_data[:None if post else -1])
        self.record_data(recorder, container.all_data[:None if post else -1])
        return container.nickname, container.mark, container.all_data

    def summary_works(self, data: list[dict]):
        self.log.info(f"当前账号筛选作品数量: {len(data)}")

    def extract_user(
            self,
            container: SimpleNamespace,
            data: SimpleNamespace) -> None:
        container.cache = container.template.copy()
        self.extract_works_info(container.cache, data)
        self.extract_account_info(container, data)
        self.extract_music(container.cache, data)
        self.extract_statistics(container.cache, data)
        self.extract_tags(container.cache, data)
        self.extract_additional_info(container.cache, data)
        container.all_data.append(container.cache)

    def extract_description(self, data: SimpleNamespace) -> str:
        return self.safe_extract(data, "desc")
        # try:
        #     desc = self.safe_extract(data, "share_info.share_link_desc")
        #     return desc.split(
        #         "  ", 1)[-1].rstrip("  %s 复制此链接，打开Dou音搜索，直接观看视频！")
        # except (KeyError, IndexError):
        #     return ""

    def clean_description(self, desc: str) -> str:
        return self.clean.clear_spaces(self.clean.filter(desc))

    def format_date(self, data: SimpleNamespace) -> str:
        return strftime(
            self.date_format,
            localtime(
                self.safe_extract(data, "create_time") or None))

    def extract_works_info(self, item: dict, data: SimpleNamespace) -> None:
        item["id"] = self.safe_extract(data, "aweme_id")
        item["desc"] = self.clean_description(
            self.extract_description(data)) or item["id"]
        item["create_time"] = self.format_date(data)
        item["create_timestamp"] = self.safe_extract(data, "create_time")
        self.classifying_works(item, data)

    def classifying_works(self, item: dict, data: SimpleNamespace) -> None:
        if images := self.safe_extract(data, "images"):
            self.extract_image_info(item, data, images)
        elif images := self.safe_extract(data, "image_post_info"):
            self.extract_image_info_tiktok(item, data, images)
        else:
            self.extract_video_info(item, data)

    def extract_additional_info(self, item: dict, data: SimpleNamespace):
        item["height"] = self.safe_extract(data, "video.height")
        item["width"] = self.safe_extract(data, "video.width")
        item["ratio"] = self.safe_extract(data, "video.ratio")

    def extract_image_info(
            self,
            item: dict,
            data: SimpleNamespace,
            images: list) -> None:
        item["type"] = "图集"
        item["downloads"] = " ".join(
            self.safe_extract(
                i, 'url_list[-1]') for i in images)
        self.extract_cover(item, data)

    def extract_image_info_tiktok(
            self,
            item: dict,
            data: SimpleNamespace,
            images: dict) -> None:
        item["type"] = "图集"
        item["downloads"] = " ".join(self.safe_extract(
            i, "display_image.url_list[-1]") for i in images["images"])
        self.extract_cover(item, data)

    def extract_video_info(self, item: dict, data: SimpleNamespace) -> None:
        item["type"] = "视频"
        item["downloads"] = self.safe_extract(
            data, "video.play_addr.url_list[-1]")
        self.extract_cover(item, data, True)

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
            item[i] = str(self.safe_extract(data, i))

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
    ) -> None:
        data = self.safe_extract(data, "author")
        container.cache["uid"] = self.safe_extract(data, "uid")
        container.cache["sec_uid"] = self.safe_extract(data, "sec_uid")
        container.cache["short_id"] = self.safe_extract(data, "short_id")
        container.cache["unique_id"] = self.safe_extract(data, "unique_id")
        container.cache["signature"] = self.safe_extract(data, "signature")
        self.check_account_info(container, data)

    def check_account_info(self,
                           container: SimpleNamespace,
                           data: SimpleNamespace, ) -> None:
        if container.post:
            if not container.nickname:
                container.nickname = self.clean.clean_name(self.safe_extract(
                    data, "nickname", "已注销账号"), default="无效账号昵称")
            container.cache["nickname"] = container.nickname
            container.cache["mark"] = container.mark or container.nickname
        else:
            nickname = self.clean.clean_name(self.safe_extract(
                data, "nickname", "已注销账号"), inquire=False, default="无效账号昵称")
            container.cache["nickname"] = nickname
            container.cache["mark"] = nickname

    def extract_not_post(self, container: SimpleNamespace,
                         data: SimpleNamespace) -> None:
        data_dict = {
            "nickname": self.safe_extract(data, "author.nickname"),
            "uid": self.safe_extract(data, "author.uid"),
        }
        container.all_data.append(data_dict)

    def works(self, data: list[dict], recorder) -> list[dict]:
        pass

    def comment(self, data: list[dict], recorder) -> list[dict]:
        pass

    def live(self, data: list[dict], recorder) -> list[dict]:
        pass

    def search_general(self, data: list[dict], recorder) -> list[dict]:
        pass

    def search_user(self, data: list[dict], recorder) -> list[dict]:
        pass

    def hot(self, data: list[list[dict]], recorder) -> list[dict]:
        pass

    def record_data(self, record, data: list[dict]):
        for i in data:
            record.save(self.extract_values(record, i))

    @staticmethod
    def extract_values(record, data: dict) -> list:
        return [data[key] for key in record.field_keys]

    @staticmethod
    def date_filter(container: SimpleNamespace, ):
        result = []
        for item in container.all_data:
            create_time = datetime.fromtimestamp(
                item["create_timestamp"]).date()
            if container.earliest <= create_time <= container.latest:
                result.append(item)
        container.all_data = result
