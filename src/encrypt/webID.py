from asyncio import run
from typing import TYPE_CHECKING
from typing import Union

from src.custom import USERAGENT
from src.testers import Logger
from src.tools import request_post

if TYPE_CHECKING:
    from src.record import BaseLogger
    from src.record import LoggerManager

__all__ = ["WebId"]


class WebId:
    NAME = "webid"
    API = "https://mcs.zijieapi.com/webid"

    @classmethod
    async def get_web_id(cls, logger: Union["BaseLogger", "LoggerManager", "Logger"], user_agent: str,
                         proxy: str = None, ) -> str | None:
        data = (f'{{"app_id":6383,"url":"https://www.douyin.com/","user_agent":'
                f'"{user_agent}","referer":"https://www.douyin.com/","user_unique_id":""}}')
        if response := await request_post(logger, cls.API, data, user_agent, content="json", proxy=proxy):
            return response.get("web_id")
        logger.error(f"获取 {cls.NAME} 参数失败！")


async def demo():
    print(await WebId.get_web_id(Logger(), USERAGENT))


if __name__ == "__main__":
    run(demo())
