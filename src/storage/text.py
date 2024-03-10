from pathlib import Path

from src.tools import PrivateRetry

__all__ = ["BaseTextLogger"]


class BaseTextLogger:
    def __init__(self, *args, **kwargs):
        self.field_keys = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def save(self, *args, **kwargs):
        pass

    @classmethod
    def _rename(cls, root: Path, type_: str, old: str, new_: str) -> str:
        mark = new_.split("_", 1)
        if not old or mark[-1] == old:
            return new_
        mark[-1] = old
        old_file = root.joinpath(f'{"_".join(mark)}.{type_}')
        cls.__rename_file(old_file, root.joinpath(f"{new_}.{type_}"))
        return new_

    @staticmethod
    @PrivateRetry.retry_infinite
    def __rename_file(old_file: Path, new_file: Path) -> bool:
        if old_file.exists() and not new_file.exists():
            try:
                old_file.rename(new_file)
                return True
            except PermissionError:
                return False
        return True
