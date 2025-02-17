from pydantic import BaseModel


class APIModel(BaseModel):
    cookie: str = ""
    proxy: str = ""
    source: bool = False
