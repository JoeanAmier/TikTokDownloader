from pydantic import Field

from .base import APIModel


class Comment(APIModel):
    detail_id: str
    pages: int = Field(
        1,
        gt=0,
    )
    cursor: int = 0
    count: int = Field(
        20,
        gt=0,
    )
    count_reply: int = Field(
        3,
        gt=0,
    )
    reply: bool = False
