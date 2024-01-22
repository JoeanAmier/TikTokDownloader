from .main_complete import TikTok

__all__ = ["Monitor"]


class Monitor(TikTok):
    def __init__(self, parameter):
        super().__init__(parameter)
