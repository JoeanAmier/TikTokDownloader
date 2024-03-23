from .main_complete import TikTok

__all__ = ["ClipboardMonitor", "WorksMonitor"]


class ClipboardMonitor(TikTok):
    def __init__(self, parameter):
        super().__init__(parameter)


class WorksMonitor(TikTok):
    def __init__(self, parameter):
        super().__init__(parameter)
