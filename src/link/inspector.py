from re import compile

__all__ = ["Inspector"]


class Inspector:
    URL = compile(r"(https?://\S+)")
