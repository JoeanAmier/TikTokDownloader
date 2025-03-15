from typing import TYPE_CHECKING
from typing import Union

from src.interface.template import API
from src.translation import _

if TYPE_CHECKING:
    from src.config import Parameter
    from src.testers import Params


class Info(API):
    def __init__(
        self,
        params: Union["Parameter", "Params"],
        cookie: str = "",
        proxy: str = None,
        sec_user_id: Union[str, list[str], tuple[str]] = ...,
        *args,
        **kwargs,
    ):
        super().__init__(params, cookie, proxy, *args, **kwargs)
        self.api = f"{self.domain}aweme/v1/web/im/user/info/"
        self.sec_user_id = sec_user_id
        self.static_params = self.params | {
            "version_code": "170400",
            "version_name": "17.4.0",
        }
        self.text = _("账号简略")

    async def run(
        self,
        first=True,
        *args,
        **kwargs,
    ) -> dict | list[dict]:
        self.set_referer()
        await self.run_single()
        if first:
            return self.response[0] if self.response else {}
        return self.response

    async def run_single(
        self,
        *args,
        **kwargs,
    ):
        await super().run_single(
            "",
            params=lambda: self.static_params,
            data=self.__generate_data,
            method="POST",
        )

    def check_response(
        self,
        data_dict: dict,
        *args,
        **kwargs,
    ):
        if d := data_dict.get("data"):
            self.append_response(d)
        else:
            self.log.warning(_("获取{text}失败").format(text=self.text))

    def __generate_data(
        self,
    ) -> dict:
        if isinstance(self.sec_user_id, str):
            self.sec_user_id = [self.sec_user_id]
        value = f"[{','.join(f'"{i}"' for i in self.sec_user_id)}]"
        return {
            "sec_user_ids": value,
        }


async def test():
    from src.testers import Params

    async with Params() as params:
        i = Info(
            params,
            sec_user_id="",
        )
        print(await i.run())


if __name__ == "__main__":
    from asyncio import run

    run(test())
