from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

__all__ = ["FileSwitch"]


class FileSwitch:
    @staticmethod
    def deal_config(path: "Path"):
        if path.exists():
            path.unlink()
        else:
            path.touch()
