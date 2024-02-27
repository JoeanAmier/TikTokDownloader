from .main_complete import TikTok

__all__ = ["ClipboardMonitor", "WorksMonitor"]


class ClipboardMonitor(TikTok):
    def __init__(self, parameter, key=None):
        super().__init__(parameter, key)


class WorksMonitor(TikTok):
    def __init__(self, parameter, key=None):
        super().__init__(parameter, key)
