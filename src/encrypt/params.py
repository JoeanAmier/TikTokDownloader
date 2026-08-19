class Params:
    def __init__(self): ...
    def sign(
        self,
        query: dict | str = "",
        data: dict | str | None = None,
        method: str = "",
        user_agent: str = "",
        ms_token: str = "",
    ) -> dict[str, str]: ...
    def sign_url(
        self,
        base_url: str = "",
        query: dict | str = "",
        data: dict | str | None = None,
        method: str = "",
        user_agent: str = "",
        ms_token: str = "",
    ) -> str: ...
