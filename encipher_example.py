from abc import ABC, abstractmethod

# import curl_cffi  # 可用于发送 HTTP 请求, Can be used to send HTTP requests
# import never_jscore  # 可用于执行 JavaScript 代码, Can be used to execute JavaScript code

__all__ = [
    "DouYinParams",
    "TikTokParams",
]


class Params(ABC):
    def __init__(self): ...
    @abstractmethod
    def sign(
        self,
        query: dict | str = "",
        data: dict | str | None = None,
        method: str = "",
        user_agent: str = "",
        ms_token: str = "",
    ) -> dict[str, str]:
        raise NotImplementedError

    @abstractmethod
    def sign_url(
        self,
        base_url: str = "",
        query: dict | str = "",
        data: dict | str | None = None,
        method: str = "",
        user_agent: str = "",
        ms_token: str = "",
    ) -> str:
        raise NotImplementedError


class DouYinParams(Params):
    """
    抖音接口加密参数
    """

    ...


class TikTokParams(Params):
    """
    TikTok 接口加密参数
    """

    ...
