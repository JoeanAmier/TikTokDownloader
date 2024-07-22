__all__ = ["TikTokDownloaderError"]


class TikTokDownloaderError(Exception):
    def __init__(self, message="项目代码出现异常！"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"TikTokDownloaderError: {self.message}"
