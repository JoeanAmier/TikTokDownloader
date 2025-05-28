from ..custom import PROJECT_ROOT
from shutil import copy2


class RenameCompatible:
    OLD_DB_FILE = PROJECT_ROOT.joinpath("TikTokDownloader.db")
    NEW_DB_FILE = PROJECT_ROOT.joinpath("DouK-Downloader.db")

    @classmethod
    def migration_file(
        cls,
    ):
        if cls.OLD_DB_FILE.exists() and not cls.NEW_DB_FILE.exists():
            copy2(cls.OLD_DB_FILE.resolve(), cls.NEW_DB_FILE.resolve())
