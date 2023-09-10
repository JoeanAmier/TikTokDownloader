from csv import writer
from logging import FileHandler
from logging import Formatter
from logging import INFO as INFO_LEVEL
from logging import getLogger
from os import path
from pathlib import Path
from platform import system
from sqlite3 import connect
from time import localtime
from time import strftime

from openpyxl import Workbook
from openpyxl import load_workbook

from src.StringCleaner import Cleaner

__all__ = [
    'BaseLogger',
    'LoggerManager',
    'NoneLogger',
    'CSVLogger',
    'XLSXLogger',
    'SQLLogger',
    'RecordManager']

INFO = 94
WARNING = 93
ERROR = 91


class BaseLogger:
    """不记录日志，空白日志记录器"""

    def __init__(self, colour):
        self.colour = colour
        self.log = None  # 记录器主体
        self._root = "./"  # 日志记录保存根路径
        self._folder = "Log"  # 日志记录保存文件夹名称
        self._name = "%Y-%m-%d %H.%M.%S"  # 日志文件名称

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        pass

    @property
    def folder(self):
        return self._folder

    @folder.setter
    def folder(self, value: str):
        pass

    def run(self, *args, **kwargs):
        pass

    def info(self, text: str, output=True):
        if output:
            print(self.colour.colorize(text, INFO))

    def warning(self, text: str, output=True):
        if output:
            print(self.colour.colorize(text, WARNING))

    def error(self, text: str, output=True):
        if output:
            print(self.colour.colorize(text, ERROR))


class LoggerManager(BaseLogger):
    """日志记录"""

    def __init__(self, colour):
        super().__init__(colour)

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        if (r := Path(value)).exists():
            self._root = r
        else:
            print("日志保存路径错误！将使用当前路径作为日志保存路径！")
            self._root = "./"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value:
            try:
                _ = strftime(value, localtime())
                self._name = value
            except ValueError:
                print("日志名称格式错误，将使用默认时间格式（年-月-日 时.分.秒）")
                self._name = "%Y-%m-%d %H.%M.%S"
        else:
            print("日志名称格式错误，将使用默认时间格式（年-月-日 时.分.秒）")
            self._name = "%Y-%m-%d %H.%M.%S"

    @property
    def folder(self):
        return self._folder

    @folder.setter
    def folder(self, value: str):
        self._folder = s if (s := Cleaner().filter(value)) else "Log"

    def run(
            self,
            format_="%(asctime)s[%(levelname)s]:  %(message)s", filename=None):
        if not (dir_ := self.root.joinpath(self.folder)).exists():
            dir_.mkdir()
        file_handler = FileHandler(
            dir_.joinpath(
                filename or f"{strftime(self.name, localtime())}.log"),
            encoding="UTF-8")
        formatter = Formatter(format_, datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)
        self.log = getLogger(__name__)
        self.log.addHandler(file_handler)
        self.log.setLevel(INFO_LEVEL)

    def info(self, text: str, output=True):
        if output:
            print(self.colour.colorize(text, INFO))
        self.log.info(text)

    def warning(self, text: str, output=True):
        if output:
            print(self.colour.colorize(text, WARNING))
        self.log.warning(text)

    def error(self, text: str, output=True):
        if output:
            print(self.colour.colorize(text, ERROR))
        self.log.error(text)


class NoneLogger:
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def save(self, *args, **kwargs):
        pass

    @staticmethod
    def rename(*args, **kwargs):
        pass


class CSVLogger:
    """CSV格式记录"""
    __type = "csv"

    def __init__(
            self,
            root: str,
            title_line,
            solo_key: bool,
            old=None,
            name="Solo_Download",
            *args,
            **kwargs):
        self.file = None  # 文件对象
        self.writer = None  # CSV对象
        self.root = Path(root)  # 文件路径
        self.name = self.rename(self.root, self.__type, old, name)  # 文件名称
        self.title_line = title_line  # 标题行
        self.index = 1 if solo_key else 0

    def __enter__(self):
        if not self.root.exists():
            self.root.mkdir()
        self.root = self.root.joinpath(f"{self.name}.{self.__type}")
        self.file = self.root.open(
            "a",
            encoding="UTF-8-SIG" if system() == "Windows" else "UTF-8",
            newline="")
        self.writer = writer(self.file)
        self.title()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def title(self):
        if path.getsize(self.root) == 0:
            # 如果文件没有任何数据，则写入标题行
            self.save(self.title_line[self.index:])

    def save(self, data, *args, **kwargs):
        self.writer.writerow(data)

    @staticmethod
    def rename(root, type_, old, new_):
        mark = new_.split("_", 1)
        if not old or mark[-1] == old:
            return new_
        mark[-1] = old
        old_file = root.joinpath(f'{"_".join(mark)}.{type_}')
        if old_file.exists():
            new_file = root.joinpath(f"{new_}.{type_}")
            old_file.rename(new_file)
        return new_


class XLSXLogger:
    """XLSX格式"""
    __type = "xlsx"

    def __init__(
            self,
            root: str,
            title_line,
            solo_key: bool,
            old=None,
            name="Solo_Download",
            *args,
            **kwargs):
        self.book = None  # XLSX数据簿
        self.sheet = None  # XLSX数据表
        self.root = Path(root)  # 文件路径
        self.name = CSVLogger.rename(self.root, self.__type, old, name)  # 文件名称
        self.title_line = title_line  # 标题行
        self.index = 1 if solo_key else 0

    def __enter__(self):
        if not self.root.exists():
            self.root.exists()
        self.root = self.root.joinpath(f"{self.name}.{self.__type}")
        self.book = load_workbook(
            self.root) if self.root.exists() else Workbook()
        self.sheet = self.book.active
        self.title()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.book.save(self.root)
        self.book.close()

    def title(self):
        if not self.sheet["A1"].value:
            # 如果文件没有任何数据，则写入标题行
            for col, value in enumerate(self.title_line[self.index:], start=1):
                self.sheet.cell(row=1, column=col, value=value)

    def save(self, data, *args, **kwargs):
        self.sheet.append(data)


class SQLLogger:
    """SQLite保存数据"""

    def __init__(
            self,
            root: str,
            file,
            title_line,
            title_type,
            solo_key: bool,
            old=None,
            name="Solo_Download", ):
        self.db = None  # 数据库
        self.cursor = None  # 游标对象
        self.root = Path(root)  # 文件路径
        self.name = (old, name)  # 数据表名称
        self.file = file  # 数据库文件名称
        self.title_line = title_line  # 数据表列名
        self.title_type = title_type  # 数据表数据类型
        self.index = 1 if solo_key else 0

    def __enter__(self):
        if not self.root.exists():
            self.root.mkdir()
        self.db = connect(self.root.joinpath(self.file))
        self.cursor = self.db.cursor()
        self.update_sheet()
        self.create()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def create(self):
        create_sql = f"""CREATE TABLE IF NOT EXISTS {self.name} ({", ".join([f"{i} {j}" for i, j in zip(self.title_line, self.title_type)])});"""
        self.cursor.execute(create_sql)
        self.db.commit()

    def save(self, data, *args, **kwargs):
        column = self.title_line[self.index:]
        insert_sql = f"""REPLACE INTO {self.name} ({", ".join(column)}) VALUES ({", ".join(["?" for _ in column])});"""
        self.cursor.execute(insert_sql, data)
        self.db.commit()

    def update_sheet(self):
        old_sheet, new_sheet = self.name
        mark = new_sheet.split("_", 1)
        if not old_sheet or mark[-1] == old_sheet:
            self.name = new_sheet
            return
        mark[-1] = old_sheet
        old_sheet = "_".join(mark)
        update_sql = f"ALTER TABLE {old_sheet} RENAME TO {new_sheet};"
        self.cursor.execute(update_sql)
        self.db.commit()
        self.name = Cleaner.clean_name(new_sheet)


class RecordManager:
    """检查数据储存路径和文件夹"""
    clean = Cleaner()
    Title = (
        "作品类型",
        "采集时间",
        "账号UID",
        "SEC_UID",
        "抖音号",
        "SHORT_ID",
        "作品ID",
        "作品描述",
        "发布时间",
        "账号昵称",
        "账号签名",
        "作品地址",
        "音乐标题",
        "音乐链接",
        "静态封面",
        "动态封面",
        "TAG_1",
        "TAG_2",
        "TAG_3",
        "点赞数量",
        "评论数量",
        "收藏数量",
        "分享数量")
    Type_ = (
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT PRIMARY KEY",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "INTEGER",
        "INTEGER",
        "INTEGER",
        "INTEGER",
    )
    Comment_Title = (
        "采集时间",
        "评论ID",
        "评论时间",
        "账号UID",
        "SEC_UID",
        "SHORT_ID",
        "抖音号",
        "账号昵称",
        "账号签名",
        "年龄",
        "IP归属地",
        "评论内容",
        "评论表情",
        "评论图片",
        "点赞数量",
        "回复数量",
        "回复ID",
    )
    Comment_Type = (
        "TEXT",
        "TEXT PRIMARY KEY",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "INTEGER",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "INTEGER",
        "INTEGER",
        "TEXT",
    )
    User_Title = (
        "ID",
        "采集时间",
        "昵称昵称",
        "账号签名",
        "抖音号",
        "年龄",
        "性别",
        "国家",
        "城市",
        # "地区",
        # "IP归属地",
        "标签",
        "企业",
        "SEC_UID",
        "账号UID",
        "SHORT_ID",
        "头像链接",
        "背景图链接",
        "作品数量",
        "获赞数量",
        "喜欢作品数量",
        "粉丝数量",
        "关注数量",
        "粉丝最多数量",
    )
    User_Type = (
        "INTEGER PRIMARY KEY",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "INTEGER",
        "TEXT",
        "TEXT",
        "TEXT",
        # "TEXT",
        # "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "INTEGER",
        "INTEGER",
        "INTEGER",
        "INTEGER",
        "INTEGER",
        "INTEGER",
    )
    Search_User_Title = (
        "采集时间",
        "账号UID",
        "SEC_UID",
        "账号昵称",
        "抖音号",
        "SHORT_ID",
        "头像缩略图",
        "账号签名",
        "标签",
        "企业",
        "粉丝数量",
        "获赞数量",
    )
    Search_User_Type = (
        "TEXT",
        "TEXT PRIMARY KEY",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "INTEGER",
        "INTEGER",
    )
    Hot_Title = (
        "排名",
        "内容",
        "热度",
        # "浏览数量",
        "时间",
        "作品数量",
        "sentence_tag",
        "sentence_id",
    )
    Hot_Type = (
        "INTEGER PRIMARY KEY",
        "TEXT",
        "INTEGER",
        # "INTEGER",
        "TEXT",
        "INTEGER",
        "INTEGER",
        "TEXT",
    )
    DataSheet = {
        "": {
            "file": "TikTokDownloader.db",
            "title_line": Title,
            "title_type": Type_,
            "solo_key": False,
        },
        "comment": {
            "file": "CommentData.db",
            "title_line": Comment_Title,
            "title_type": Comment_Type,
            "solo_key": False,
        },
        "user": {
            "file": "UserData.db",
            "title_line": User_Title,
            "title_type": User_Type,
            "solo_key": True,
        },
        "mix": {
            "file": "MixData.db",
            "title_line": Title,
            "title_type": Type_,
            "solo_key": False,
        },
        "search_user": {
            "file": "SearchResult.db",
            "title_line": Search_User_Title,
            "title_type": Search_User_Type,
            "solo_key": False,
        },
        "hot": {
            "file": "HotBoardData.db",
            "title_line": Hot_Title,
            "title_type": Hot_Type,
            "solo_key": False,
        },
    }
    DataLogger = {
        "csv": CSVLogger,
        "xlsx": XLSXLogger,
        "sql": SQLLogger,
    }

    def run(self, root="./", folder="Data", type_="", format_=""):
        root = r if (r := Path(root)).exists() else Path("./")
        name = root.joinpath(self.clean.filter(folder) or "Data")
        type_ = self.DataSheet.get(type_)
        format_ = self.DataLogger.get(format_, NoneLogger)
        return format_, name, type_
