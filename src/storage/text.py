from pathlib import Path
from typing import TYPE_CHECKING
from typing import Union

from ..tools import Retry

if TYPE_CHECKING:
    from typing import Iterable


def convert_to_string(function):
    async def _convert_to_string(self, data: Union["Iterable", list], *args, **kwargs):
        for index, value in enumerate(data):
            if isinstance(value, (int, float)):  # 如果值是数字（整型或浮点型）
                data[index] = str(value)  # 转换为字符串
            elif isinstance(value, list):  # 如果值是列表
                data[index] = " ".join(value)  # 将列表元素转换为字符串并连接
        return await function(self, data, *args, **kwargs)

    return _convert_to_string


class BaseTextLogger:
    def __init__(self, *args, **kwargs):
        self.field_keys = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    @convert_to_string
    async def save(self, data: "Iterable", *args, **kwargs):
        # 数据保存方法入口
        return await self._save(data, *args, **kwargs)

    async def _save(self, data: "Iterable", *args, **kwargs):
        # 实际数据保存逻辑
        pass

    @classmethod
    def _rename(cls, root: Path, type_: str, old: str, new_: str) -> str:
        mark = new_.split("_", 1)
        if not old or mark[-1] == old:
            return new_
        mark[-1] = old
        old_file = root.joinpath(f"{'_'.join(mark)}.{type_}")
        cls.__rename_file(old_file, root.joinpath(f"{new_}.{type_}"))
        return new_

    @staticmethod
    @Retry.retry_infinite
    def __rename_file(old_file: Path, new_file: Path) -> bool:
        if old_file.exists() and not new_file.exists():
            try:
                old_file.rename(new_file)
                return True
            except PermissionError:
                return False
        return True
