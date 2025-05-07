from pydantic import Field

from .base import APIModel


class Mix(APIModel):
    mix_id: str | None = None
    detail_id: str | None = None
    cursor: int = 0
    count: int = Field(
        12,
        gt=0,
    )


class MixTikTok(APIModel):
    mix_id: str | None = None
    cursor: int = 0
    count: int = Field(
        30,
        gt=0,
    )
