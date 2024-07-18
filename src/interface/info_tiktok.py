from asyncio import run
from typing import TYPE_CHECKING
from typing import Union

from src.interface.template import APITikTok
from src.testers import Params

if TYPE_CHECKING:
    from src.config import Parameter


class InfoTikTok(APITikTok):
    def __init__(
            self,
            params: Union["Parameter", Params],
            cookie: str | dict = None,
            proxy: str = None,
            unique_id: Union[str] = "",
            sec_user_id: Union[str] = "",
            *args,
            **kwargs,
    ):
        super().__init__(params, cookie, proxy, *args, **kwargs, )
        self.api = f"{self.domain}api/user/detail/"
        self.unique_id = unique_id
        self.sec_user_id = sec_user_id
        self.text = "账号简略信息"

    async def run(self, first=True, *args, **kwargs, ) -> dict | list[dict]:
        self.set_referer()
        await self.run_single()
        return self.response

    async def run_single(self, *args, **kwargs, ):
        await super().run_single("", )

    def check_response(self, data_dict: dict, *args, **kwargs, ):
        if d := data_dict.get("userInfo"):
            self.append_response(d)
        else:
            self.log.warning(f"获取{self.text}失败")

    def append_response(
            self,
            data: dict,
            *args,
            **kwargs,
    ) -> None:
        self.response.append(data)

    def generate_params(self, ) -> dict:
        return self.params | {
            "abTestVersion": "[object Object]",
            "appType": "m",
            "data_collection_enabled": "true",
            "secUid": self.sec_user_id,
            "uniqueId": self.unique_id,
            "user": "[object Object]",
            "user_is_login": "true",
        }


async def main():
    async with Params() as params:
        i = InfoTikTok(params, )
        print(await i.run())


if __name__ == "__main__":
    run(main())
