import csv
import logging
import os
import time


class RunLogger:
    def __init__(self):
        self.log = None  # 记录器主体
        self._root = "./"  # 日志记录保存根路径
        self._folder = "Log"  # 日志记录保存文件夹名称
        self._name = "%Y-%m-%d %H.%M.%S"  # 日志文件名称

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        if os.path.exists(value) and os.path.isdir(value):
            self._root = value
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
                _ = time.strftime(value, time.localtime())
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
    def folder(self, value):
        """未生效"""
        pass

    def run(
            self,
            format_="%(asctime)s[%(levelname)s]%(filename)s-%(lineno)d: %(message)s"):
        if not os.path.exists(dir_ := os.path.join(self.root, self.folder)):
            os.mkdir(dir_)
        self.log = logging
        self.log.basicConfig(
            filename=os.path.join(
                dir_,
                f"{time.strftime(self.name, time.localtime())}.log"),
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S',
            format=format_,
            encoding="UTF-8")

    def info(self, text: str, output=True):
        if output:
            print(text)
        self.log.info(text)

    def warning(self, text: str, output=True):
        if output:
            print(text)
        self.log.warning(text)

    def error(self, text: str, output=True):
        if output:
            print(text)
        self.log.error(text)


class Writer:
    param = {
        "type_": "",
        "encoding": "UTF-8",
    }

    def __init__(self, *args, **kwargs):
        pass

    def save(self, *args, **kwargs):
        pass


class CSV(Writer):
    param = {
        "type_": "csv",
        "encoding": "UTF-8",
        "newline": ""
    }

    def __init__(self, file):
        self.main = csv.writer(file)

    def save(self, data):
        self.main.writerow(data)


class DataLogger:
    __root = "./"
    __folder = "Data"
    __name = "%Y-%m-%d %H.%M.%S"
    TYPE = {
        "csv": CSV,
    }

    def __init__(self, type_: str):
        self.writer = self.TYPE.get(type_, Writer)

    def start(self, dir_):
        self.file = open(os.path.join(
            dir_,
            f"{time.strftime(self.__name, time.localtime())}.csv"), "w")
        print("文件已打开")
        self.writer = csv.writer(self.file)

    def run(self):
        if not os.path.exists(dir_ := os.path.join(self.__root, self.__folder)):
            os.mkdir(dir_)
        self.start(dir_)
