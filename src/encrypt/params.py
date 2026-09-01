from abc import ABC, abstractmethod


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
