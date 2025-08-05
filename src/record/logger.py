from logging import INFO as INFO_LEVEL
from logging import FileHandler, Formatter, getLogger
from pathlib import Path
from platform import system
from shutil import move
from time import localtime, strftime
from typing import TYPE_CHECKING

from ..custom import (
    DEBUG,
    ERROR,
    INFO,
    WARNING,
)
from .base import BaseLogger

if TYPE_CHECKING:
    from ..tools import ColorfulConsole


class LoggerManager(BaseLogger):
    """日志记录"""

    encode = "UTF-8-SIG" if system() == "Windows" else "UTF-8"

    def __init__(
        self, main_path: Path, console: "ColorfulConsole", root="", folder="", name=""
    ):
        super().__init__(main_path, console, root, folder, name)

    def run(
        self,
        format_="%(asctime)s[%(levelname)s]:  %(message)s",
        filename=None,
    ):
        dir_ = self._root.joinpath(self._folder)
        self.compatible(dir_)
        dir_.mkdir(exist_ok=True)
        file_handler = FileHandler(
            dir_.joinpath(
                f"{filename}.log"
                if filename
                else f"{strftime(self._name, localtime())}.log"
            ),
            encoding=self.encode,
        )
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

    def debug(self, text: str, **kwargs):
        if self.DEBUG:
            self.console.print(text, style=DEBUG, **kwargs)
            self.log.debug(text.strip())

    def compatible(
        self,
        path: Path,
    ):
        if (
            old := self._root.parent.joinpath(self._folder)
        ).exists() and not path.exists():
            move(old, path)
