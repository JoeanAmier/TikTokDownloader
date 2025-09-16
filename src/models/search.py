from typing import Literal

from pydantic import Field, field_validator

from src.models.base import APIModel

try:
    from src.translation import _
except ImportError:

    def _(x):
        return x


class BaseSearch(APIModel):
    keyword: str
    pages: int = Field(
        1,
        gt=0,
    )
    offset: int = Field(
        0,
        ge=0,
    )
    count: int = Field(
        10,
        ge=5,
    )

    @field_validator("keyword", mode="before")
    @classmethod
    def keyword_validator(cls, v):
        if not v:
            raise ValueError(_("keyword 参数无效"))
        return v


class GeneralSearch(BaseSearch):
    channel: Literal[0,] = 0
    sort_type: Literal[
        0,
        1,
        2,
    ] = 0
    publish_time: Literal[
        0,
        1,
        7,
        180,
    ] = 0
    duration: Literal[
        0,
        1,
        2,
        3,
    ] = 0
    search_range: Literal[
        0,
        1,
        2,
        3,
    ] = 0
    content_type: Literal[
        0,
        1,
        2,
    ] = 0

    @field_validator(
        "sort_type",
        "publish_time",
        "duration",
        "search_range",
        "content_type",
        mode="before",
    )
    @classmethod
    def val_number(cls, value: str | int) -> int:
        return int(value) if isinstance(value, str) else value


class VideoSearch(BaseSearch):
    channel: Literal[1,] = 1
    sort_type: Literal[
        0,
        1,
        2,
    ] = 0
    publish_time: Literal[
        0,
        1,
        7,
        180,
    ] = 0
    duration: Literal[
        0,
        1,
        2,
        3,
    ] = 0
    search_range: Literal[
        0,
        1,
        2,
        3,
    ] = 0

    @field_validator(
        "sort_type", "publish_time", "duration", "search_range", mode="before"
    )
    @classmethod
    def val_number(cls, value: str | int) -> int:
        return int(value) if isinstance(value, str) else value


class UserSearch(BaseSearch):
    channel: Literal[2,] = 2
    douyin_user_fans: Literal[
        0,
        1,
        2,
        3,
        4,
        5,
    ] = 0
    douyin_user_type: Literal[
        0,
        1,
        2,
        3,
    ] = 0

    @field_validator("douyin_user_fans", "douyin_user_type", mode="before")
    @classmethod
    def val_number(cls, value: str | int) -> int:
        return int(value) if isinstance(value, str) else value


class LiveSearch(BaseSearch):
    channel: Literal[3,] = 3
