from logging import FileHandler
from logging import Formatter
from logging import INFO as INFO_LEVEL
from logging import getLogger
from pathlib import Path
from platform import system
from time import localtime
from time import strftime
from typing import TYPE_CHECKING

from src.custom import (
    WARNING,
    ERROR,
    INFO,
)
from .base import BaseLogger

if TYPE_CHECKING:
    from src.tools import ColorfulConsole


class LoggerManager(BaseLogger):
    """日志记录"""
    encode = "UTF-8-SIG" if system() == "Windows" else "UTF-8"

    def __init__(
            self,
            main_path: Path,
            console: "ColorfulConsole",
            root="",
            folder="",
            name=""):
        super().__init__(main_path, console, root, folder, name)

    def run(
            self,
            format_="%(asctime)s[%(levelname)s]:  %(message)s", filename=None):
        if not (dir_ := self._root.joinpath(self._folder)).exists():
            dir_.mkdir()
        file_handler = FileHandler(
            dir_.joinpath(
                f"{filename}.log" if filename else f"{strftime(
                    self._name,
                    localtime())}.log"),
            encoding=self.encode)
        formatter = Formatter(format_, datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)
        self.log = getLogger(__name__)
        self.log.addHandler(file_handler)
        self.log.setLevel(INFO_LEVEL)

    def info(self, text: str, output=True, **kwargs):
        if output:
            self.console.print(text, style=INFO, **kwargs)
        self.log.info(text.strip())

    def warning(self, text: str, output=True, **kwargs):
        if output:
            self.console.print(text, style=WARNING, **kwargs)
        self.log.warning(text.strip())

    def error(self, text: str, output=True, **kwargs):
        if output:
            self.console.print(text, style=ERROR, **kwargs)
        self.log.error(text.strip())
