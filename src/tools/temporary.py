from time import time

__all__ = ["timestamp"]


def timestamp() -> str:
    return str(time())[:10]
