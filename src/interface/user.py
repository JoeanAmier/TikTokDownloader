from typing import TYPE_CHECKING, Callable, Type, Coroutine
from typing import Union

from src.interface.template import API
from src.testers import Params
from src.translation import _

if TYPE_CHECKING:
    from src.config import Parameter


class User(API):
    def __init__(
            self,
            params: Union["Parameter", Params],
            cookie: str = None,
            proxy: str = None,
            sec_user_id: str = ...,
            data_key: str = "user",
            *args,
            **kwargs,
    ):
        super().__init__(params, cookie, proxy, *args, **kwargs, )
        self.sec_user_id = sec_user_id
        self.api = f"{self.domain}aweme/v1/web/user/profile/other/"
        self.text = _("账号简略")
        self.data_key = data_key
    async def run(self, *args, **kwargs):
        return await super().run(
            single_page=True,
            data_key=self.data_key,
        )

    async def run_batch(
            self,
            data_key: str,
            error_text="",
            cursor="cursor",
            has_more="has_more",
            params: Callable = lambda: {},
            data: Callable = lambda: {},
            method="GET",
            headers: dict = None,
            callback: Type[Coroutine] = None,
            *args,
            **kwargs, ):
        pass

    def check_response(
            self,
            data_dict: dict,
            data_key: str,
            error_text="",
            *args,
            **kwargs,
    ):
        try:
            if not (d := data_dict[data_key]):
                self.log.warning(error_text)
            else:
                self.response = d
        except KeyError:
            self.log.error(_("数据解析失败，请告知作者处理: {data}").format(data=data_dict))
            self.finished = True

    def generate_params(self, ) -> dict:
        return self.params | {
            "publish_video_strategy_type": "2",
            "sec_user_id": self.sec_user_id,
            "personal_center_strategy": "1",
            "profile_other_record_enable": "1",
            "land_to": "1",
            "version_code": "170400",
            "version_name": "17.4.0",
        }


async def test():
    async with Params() as params:
        i = User(
            params,
            sec_user_id="",
        )
        print(await i.run())


if __name__ == "__main__":
    from asyncio import run

    run(test())
