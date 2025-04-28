from pydantic import BaseModel


class ShortUrl(BaseModel):
    text: str
    proxy: str = ""
