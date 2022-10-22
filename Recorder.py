import logging


class Logger:
    def __init__(self):
        self.log = logging
        self.log.basicConfig(
            filename="./TikTokDownloader.log",
            level=logging.INFO,
            datefmt='[%Y-%m-%d %H:%M:%S]',
            format="%(asctime)s:%(levelname)s:[%(lineno)d]:%(message)s"
        )
