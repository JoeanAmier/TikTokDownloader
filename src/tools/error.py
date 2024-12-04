class TikTokDownloaderError(Exception):
    def __init__(self, message="项目代码错误"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"TikTokDownloaderError: {self.message}"


class CacheError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message
