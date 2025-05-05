from pydantic import Field

from .base import APIModel


class Account(APIModel):
    sec_user_id: str
    tab: str = "post"
    earliest: str | float | int | None = None
    latest: str | float | int | None = None
    pages: int | None = None
    cursor: int = 0
    count: int = Field(
        18,
        gt=0,
    )


class AccountTiktok(Account):
    pass
