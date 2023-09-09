from datetime import datetime
from time import localtime
from time import strftime

from src.DataAcquirer import Parameter

__all__ = ["Extractor"]


class Extractor:
    def __init__(self, params: Parameter):
        self.log = params.log
        self.date = params.date
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

    def run(self, data: list[dict], type_="works", **kwargs) -> dict:
        if type_ not in self.type.keys():
            raise ValueError
        return self.type[type_](data, **kwargs)

    def user(self, data: list[dict], post=True) -> list[dict]:
        result = []
        template = {
            "collection_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        if post:
            [self.extract_user(result, template, item) for item in data]
        else:
            [self.extract_user(result, template, item) for item in data[:-1]]
            self.extract_not_post(result, data[-1])
        return result

    def extract_user(
            self,
            container: list,
            template: dict,
            data: dict) -> None:
        data_dict = template.copy()
        self.extract_works_info(data_dict, data)
        self.extract_account_info(data_dict, data)
        container.append(data_dict)

    @staticmethod
    def extract_description(data: dict) -> str:
        try:
            desc = data["share_info"]["share_link_desc"]
            return desc.split(
                ":/ ", 1)[-1].rstrip("  %s 复制此链接，打开Dou音搜索，直接观看视频！")
        except (KeyError, IndexError):
            return ""

    def format_date(self, data: dict) -> str:
        return strftime(
            self.date,
            localtime(
                data["create_time"]))

    def extract_works_info(self, item: dict, data: dict) -> None:
        item["id"] = data["aweme_id"]
        item["desc"] = self.extract_description(data)
        item["create_time"] = self.format_date(data)

    def extract_account_info(self, item: dict, data: dict) -> None:
        pass

    @staticmethod
    def extract_not_post(container: list, data: dict) -> None:
        data_dict = {
            "nickname": data["author"]["nickname"],
            "uid": data["author"]["uid"],
        }
        container.append(data_dict)

    def works(self, data: list[dict]) -> list[dict]:
        pass

    def comment(self, data: list[dict]) -> list[dict]:
        pass

    def live(self, data: list[dict]) -> list[dict]:
        pass

    def search_general(self, data: list[dict]) -> list[dict]:
        pass

    def search_user(self, data: list[dict]) -> list[dict]:
        pass

    def hot(self, data: list[list[dict]]) -> list[dict]:
        pass
