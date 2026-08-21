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
        # if isinstance(query, dict):
        #     query = urlencode(query, safe="=", quote_via=quote)
        # a_bogus = self._ab.get_value(query, data, method, user_agent=user_agent)
        # return {"a_bogus": a_bogus}
        return {
            "a_bogus": "dv0Rge7imxQbadKb8cBqy5VU8tnlrBSyhsTobG1PyxKSyq0TDmPc"
            "/neMbxoQ4Ahv1upzwHQH6DsATjxbN0UTp9OkzmhDus7W7t2VIumLgqq6Tl4/DHDFe8vFuwsCWcsw"
            "-/deEeyRWs0i6d5l9qCiABB7w/4n-mRmMr-UVZutx9KsUAujhn/Ca-S2Y7iqPj=="
        }

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
