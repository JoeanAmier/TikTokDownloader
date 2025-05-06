from typing import TYPE_CHECKING
from typing import Union

from src.interface.template import APITikTok
from src.translation import _

if TYPE_CHECKING:
    from src.config import Parameter
    from src.testers import Params


class InfoTikTok(APITikTok):
    def __init__(
        self,
        params: Union["Parameter", "Params"],
        cookie: str = "",
        proxy: str = None,
        unique_id: Union[str] = "",
        sec_user_id: Union[str] = "",
        *args,
        **kwargs,
    ):
        super().__init__(params, cookie, proxy, *args, **kwargs)
        self.api = f"{self.domain}api/user/detail/"
        self.unique_id = unique_id
        self.sec_user_id = sec_user_id
        self.text = _("账号简略")

    async def run(
        self,
        # first=True,
        *args,
        **kwargs,
    ) -> dict | list[dict]:
        self.set_referer()
        await self.run_single()
        return self.response[0] if self.response else {}

    async def run_single(
        self,
        *args,
        **kwargs,
    ):
        await super().run_single(
            "",
        )

    def check_response(
        self,
        data_dict: dict,
        *args,
        **kwargs,
    ):
        if d := data_dict.get("userInfo"):
            self.append_response(d)
        else:
            self.log.warning(_("获取{text}失败").format(text=self.text))

    def append_response(
        self,
        data: dict,
        *args,
        **kwargs,
    ) -> None:
        self.response.append(data)

    def generate_params(
        self,
    ) -> dict:
        return self.params | {
            "abTestVersion": "[object Object]",
            "appType": "t",
            "secUid": self.sec_user_id,
            "uniqueId": self.unique_id,
            "user": "[object Object]",
        }


async def test():
    from src.testers import Params

    async with Params() as params:
        i = InfoTikTok(
            params,
            unique_id="",
            sec_user_id="",
        )
        print(await i.run())


if __name__ == "__main__":
    from asyncio import run

    run(test())
