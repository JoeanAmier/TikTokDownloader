from abc import ABC, abstractmethod

# import curl_cffi  # 可用于发送 HTTP 请求, Can be used to send HTTP requests
# https://github.com/lexiforest/curl_cffi
# import javascript  # 可用于执行 JavaScript 代码, Can be used to execute JavaScript code
# Requires Node.js 18 or newer.
# https://github.com/extremeheat/JSPyBridge

__all__ = [
    "DouYinParams",
    "TikTokParams",
]


class Params(ABC):
    def __init__(self): ...
    @abstractmethod
    def sign(
        self,
        url: str = "",
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
        url: str = "",
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
