from types import SimpleNamespace

__all__ = ["DownloadExtender"]


class DownloadExtender:
    MODIFY = False

    @staticmethod
    def deal(data: dict | SimpleNamespace, *args, **kwargs) -> str:
        return data["downloads"]
