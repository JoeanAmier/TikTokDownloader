from ..translation import _


class DownloaderError(Exception):
    def __init__(
        self,
        message: str = "",
    ):
        self.message = message or _("项目代码错误")
        super().__init__(self.message)

    def __str__(self):
        return f"DownloaderError: {self.message}"


class CacheError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message
