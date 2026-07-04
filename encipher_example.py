# import httpx  # 可用于发送 HTTP 请求, Can be used to send HTTP requests
# import never_jscore  # 可用于执行 JavaScript 代码, Can be used to execute JavaScript code

__all__ = [
    "ABogus",
    "XBogus",
    "XGnarly",
]


class ABogus:
    """
    抖音接口加密参数
    """

    def __init__(self): ...
    def get_value(
        self,
        query: dict | str | None = None,
        data: dict | None = None,
        method: str | None = None,
        user_agent: str = "",
    ) -> str: ...


class XBogus:
    """
    TikTok 接口加密参数
    """

    def __init__(self): ...
    def get_x_bogus(
        self,
        query: dict | str | None = None,
        data: dict | None = None,
        method: str | None = None,
        user_agent: str = "",
    ) -> str: ...


class XGnarly:
    """
    TikTok 接口加密参数
    """

    def __init__(self): ...
    def generate(
        self,
        query: dict | str | None = None,
        data: dict | None = None,
        method: str | None = None,
        user_agent: str = "",
    ) -> str: ...
