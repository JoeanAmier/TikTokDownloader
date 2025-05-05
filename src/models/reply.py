from pydantic import Field

from .base import APIModel


class Reply(APIModel):
    detail_id: str
    comment_id: str
    pages: int = Field(
        1,
        gt=0,
    )
    cursor: int = 0
    count: int = Field(
        3,
        gt=0,
    )
