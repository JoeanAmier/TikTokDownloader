from typing import TYPE_CHECKING

from .main_complete import TikTok

if TYPE_CHECKING:
    from ..config import Parameter
    from ..manager import Database

__all__ = ["ClipboardMonitor", "WorksMonitor"]


class ClipboardMonitor(TikTok):
    def __init__(self, parameter: "Parameter", database: "Database", ):
        super().__init__(parameter, database, )


class WorksMonitor(TikTok):
    def __init__(self, parameter: "Parameter", database: "Database", ):
        super().__init__(parameter, database, )
