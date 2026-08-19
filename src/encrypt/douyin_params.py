from urllib.parse import quote, urlencode

from src.encrypt.aBogus import ABogus

from ..custom import USERAGENT
from .params import Params

__all__ = ["DouYinParams"]


class DouYinParams(Params):
    def __init__(self) -> None:
        super().__init__()
        self._ab = ABogus()

    def sign(
        self,
        query: dict | str = "",
        data: dict | str | None = None,
        method: str = "",
        user_agent: str = USERAGENT,
        ms_token: str = "",
    ) -> dict[str, str]:
        if isinstance(query, dict):
            query = urlencode(query, safe="=", quote_via=quote)
        a_bogus = self._ab.get_value(query, data, method, user_agent=user_agent)
        return {"a_bogus": a_bogus}

    def sign_url(
        self,
        base_url: str = "",
        query: dict | str = "",
        data: dict | str | None = None,
        method: str = "",
        user_agent: str = USERAGENT,
        ms_token: str = "",
    ) -> str:
        if isinstance(query, dict):
            query = urlencode(query, safe="=", quote_via=quote)
        a_bogus = self.sign(query, data, method, user_agent)["a_bogus"]
        signed_query = f"{query}&a_bogus={a_bogus}"
        if not base_url:
            return signed_query
        sep = "&" if "?" in base_url else "?"
        return f"{base_url}{sep}{signed_query}"
