__all__ = ["Extractor"]


class Extractor:
    def __init__(self):
        self.type = {
            "user": self.user,
            "works": self.works,
            "comment": self.comment,
            "live": self.live,
            "search_general": self.search_general,
            "search_user": self.search_user,
            "hot": self.hot,
        }

    def run(self, data: list[dict], type_="Works") -> list[dict]:
        pass

    def user(self):
        pass

    def works(self):
        pass

    def comment(self):
        pass

    def live(self):
        pass

    def search_general(self):
        pass

    def search_user(self):
        pass

    def hot(self):
        pass
