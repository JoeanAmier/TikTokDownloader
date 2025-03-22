from asyncio import run
from typing import TYPE_CHECKING, Union

from src.custom import PARAMS_HEADERS
from src.tools import request_params
from src.translation import _

if TYPE_CHECKING:
    from src.record import BaseLogger, LoggerManager
    from src.testers import Logger

__all__ = ["WebId"]


class WebId:
    NAME = "webid"
    API = "https://mcs.zijieapi.com/webid"
    PARAMS = {"aid": "6383", "sdk_version": "5.1.18_zip", "device_platform": "web"}

    @classmethod
    async def get_web_id(
        cls,
        logger: Union["BaseLogger", "LoggerManager", "Logger"],
        headers: dict,
        proxy: str = None,
        **kwargs,
    ) -> str | None:
        user_agent = headers.get("User-Agent")
        data = (
            f'{{"app_id":6383,"url":"https://www.douyin.com/","user_agent":"{user_agent}","referer":"https://www'
            f'.douyin.com/","user_unique_id":""}}'
        )
        if response := await request_params(
            logger,
            cls.API,
            params=cls.PARAMS,
            data=data,
            headers=headers,
            resp="json",
            proxy=proxy,
            **kwargs,
        ):
            return response.get("web_id")
        logger.error(_("获取 {name} 参数失败！").format(name=cls.NAME))


async def test():
    from src.testers import Logger

    print(await WebId.get_web_id(Logger(), PARAMS_HEADERS, proxy=None))


if __name__ == "__main__":
    run(test())
