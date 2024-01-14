from pathlib import Path


class BaseTextLogger:
    def __init__(self, *args, **kwargs):
        self.field_keys = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def save(self, *args, **kwargs):
        pass

    @staticmethod
    def _rename(root: Path, type_: str, old: str, new_: str) -> str:
        mark = new_.split("_", 1)
        if not old or mark[-1] == old:
            return new_
        mark[-1] = old
        old_file = root.joinpath(f'{"_".join(mark)}.{type_}')
        if old_file.exists():
            new_file = root.joinpath(f"{new_}.{type_}")
            old_file.rename(new_file)
        return new_
