import time
from datetime import datetime
from typing import TYPE_CHECKING, Callable, Type, Coroutine, Union

from src.interface.user import User
from src.interface.template import APITikTok
from src.testers import Params

if TYPE_CHECKING:
    from src.config import Parameter


class UserTikTok(User, APITikTok):
    def __init__(
        self,
        params: Union["Parameter", Params],
        cookie: str | dict = None,
        proxy: str = None,
        sec_user_id: str = ...,
        data_key: str = "userInfo",
        uniqueId: str = "",
        *args,
        **kwargs,
    ):
        super().__init__(
            params,
            cookie,
            proxy,
            sec_user_id,
            *args,
            **kwargs,
        )
        self.api = f"{APITikTok.domain}api/user/detail/"
        self.data_key = data_key
        self.uniqueId = uniqueId

    def generate_params(self) -> dict:
        return self.params | {
            "uniqueId": self.uniqueId,
            "priority_region": "",
        }

    async def run(
        self,
        referer: str = None,
        data_key: str = "userInfo",
        error_text="",
        *args,
        **kwargs
    ):
        self.set_referer(referer or f"{self.domain}@{self.sec_user_id}")

        data = await super().run(
            single_page=True,
            data_key=self.data_key,
            error_text=error_text,
            *args,
            **kwargs
        )

        def flatten_dict(d, sep='_'):
            items = []
            for k, v in d.items():
                if isinstance(v, dict):
                    items.extend(flatten_dict(v, sep=sep).items())
                else:
                    items.append((k, v))
            return dict(items)
        data = flatten_dict(data)
        return data


async def test():
    async with Params() as params:
        i = UserTikTok(
            params,
            sec_user_id="",
        )
        print(await i.run())


if __name__ == "__main__":
    from asyncio import run

    run(test())