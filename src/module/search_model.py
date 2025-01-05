from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

try:
    from src.translation import _
except ImportError:
    _ = lambda x: x


class BaseSearch(BaseModel):
    keyword: str
    pages: int = Field(99999, gt=0, )

    @field_validator("keyword")
    @classmethod
    def keyword_validator(cls, v):
        if not v:
            raise ValueError(_("keyword 参数无效"))
        return v


class GeneralSearch(BaseSearch):
    channel: Literal[0,] = 0
    sort_type: Literal[0, 1, 2,] = 0
    publish_time: Literal[0, 1, 7, 180,] = 0
    duration: Literal[0, 1, 2, 3,] = 0
    search_range: Literal[0, 1, 2, 3,] = 0
    content_type: Literal[0, 1, 2,] = 0

    @field_validator("sort_type", "publish_time", "duration", "search_range", "content_type", mode='before')
    @classmethod
    def val_number(cls, value: str | int) -> int:
        return int(value) if isinstance(value, str) else value


class VideoSearch(BaseSearch):
    channel: Literal[1,] = 1
    sort_type: Literal[0, 1, 2,] = 0
    publish_time: Literal[0, 1, 7, 180,] = 0
    duration: Literal[0, 1, 2, 3,] = 0
    search_range: Literal[0, 1, 2, 3,] = 0

    @field_validator("sort_type", "publish_time", "duration", "search_range", mode='before')
    @classmethod
    def val_number(cls, value: str | int) -> int:
        return int(value) if isinstance(value, str) else value


class UserSearch(BaseSearch):
    channel: Literal[2,] = 2
    douyin_user_fans: Literal[0, 1, 2, 3, 4, 5,] = 0
    douyin_user_type: Literal[0, 1, 2, 3,] = 0

    @field_validator("douyin_user_fans", "douyin_user_type", mode='before')
    @classmethod
    def val_number(cls, value: str | int) -> int:
        return int(value) if isinstance(value, str) else value


class LiveSearch(BaseSearch):
    channel: Literal[3,] = 3


if __name__ == '__main__':
    from pydantic import ValidationError

    try:
        search = BaseSearch(keyword="test", )
        print(search.model_dump())
    except ValidationError as e:
        print(repr(e))
    print(GeneralSearch(keyword="test", sort_type="2").model_dump())
