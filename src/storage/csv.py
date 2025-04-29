from csv import writer
from os.path import getsize
from pathlib import Path
from platform import system
from typing import TYPE_CHECKING

from .text import BaseTextLogger

if TYPE_CHECKING:
    from ..tools import ColorfulConsole

__all__ = ["CSVLogger"]


class CSVLogger(BaseTextLogger):
    """CSV 格式保存数据"""

    __type = "csv"
    encode = "UTF-8-SIG" if system() == "Windows" else "UTF-8"

    def __init__(
        self,
        root: Path,
        title_line: tuple,
        field_keys: tuple,
        console: "ColorfulConsole",
        old=None,
        name="Download",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.console = console
        self.file = None  # 文件对象
        self.writer = None  # CSV对象
        self.name = self._rename(root, self.__type, old, name)  # 文件名称
        self.path = root.joinpath(f"{self.name}.{self.__type}")  # 文件路径
        self.title_line = title_line  # 标题行
        self.field_keys = field_keys

    async def __aenter__(self):
        self.file = self.path.open("a", encoding=self.encode, newline="")
        self.writer = writer(self.file)
        await self.title()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    async def title(self):
        if getsize(self.path) == 0:
            # 如果文件没有任何数据，则写入标题行
            await self.save(self.title_line)

    async def _save(self, data, *args, **kwargs):
        self.writer.writerow(data)
