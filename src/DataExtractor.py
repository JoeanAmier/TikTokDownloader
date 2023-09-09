from src.DataAcquirer import Parameter

__all__ = ["Extractor"]


class Extractor:
    def __init__(self, params: Parameter):
        self.log = params.log
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
    def get_sec_uid(data: dict) -> str | False:
        try:
            return data["author"]["sec_uid"]
        except KeyError:
            return False

    def run(self, data: list[dict], type_="works", **kwargs) -> list[dict]:
        if type_ not in self.type.keys():
            raise ValueError
        return self.type[type_](data, **kwargs)

    def user(self, data: list[dict]) -> list[dict]:
        pass

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

    def hot(self, data: list[list[dict]]) -> list[list[dict]]:
        pass
