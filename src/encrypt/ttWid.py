from asyncio import run
from http import cookies
from typing import TYPE_CHECKING
from typing import Union

from src.custom import PARAMS_HEADERS
from src.custom import PARAMS_HEADERS_TIKTOK
from src.tools import request_params

if TYPE_CHECKING:
    from src.record import BaseLogger
    from src.record import LoggerManager
    from src.testers import Logger

__all__ = ["TtWid", "TtWidTikTok"]


class TtWid:
    NAME = "ttwid"
    API = "https://ttwid.bytedance.com/ttwid/union/register/"
    DATA = (
        '{"region":"cn","aid":1768,"needFid":false,"service":"www.ixigua.com","migrate_info":{"ticket":"",'
        '"source":"node"},"cbUrlProtocol":"https","union":true}')

    @classmethod
    async def get_tt_wid(cls, logger: Union["BaseLogger", "LoggerManager", "Logger"],
                         headers: dict,
                         **kwargs, ) -> dict | None:
        if response := await request_params(logger, cls.API, data=cls.DATA, headers=headers, **kwargs, ):
            return cls.extract(logger, response, cls.NAME)
        logger.error(f"获取 {cls.NAME} 参数失败！")

    @staticmethod
    def extract(logger: Union["BaseLogger", "LoggerManager", "Logger"],
                headers,
                key: str) -> dict | None:
        if c := headers.get("Set-Cookie"):
            cookie_jar = cookies.SimpleCookie()
            cookie_jar.load(c)
            if v := cookie_jar.get(key):
                return {key: v.value}
        logger.error(f"获取 {key} 参数失败！")


class TtWidTikTok(TtWid):
    API = "https://www.tiktok.com/ttwid/check/"
    DATA = (
        '{"aid":1988,"service":"www.tiktok.com","union":false,"unionHost":"","needFid":false,"fid":"",'
        '"migrate_priority":0}')

    @classmethod
    async def get_tt_wid(cls,
                         logger: Union["BaseLogger", "LoggerManager", "Logger"],
                         headers: dict,
                         cookie: str = "",
                         **kwargs,
                         ) -> dict | None:
        if response := await request_params(logger, cls.API, data=cls.DATA, headers=headers | {
            "Cookie": cookie,
            "Content-Type": "application/x-www-form-urlencoded",
        }, **kwargs, ):
            return cls.extract(logger, response, cls.NAME)
        logger.error(f"获取 {cls.NAME} 参数失败！")


async def demo():
    from src.testers import Logger
    print("抖音", await TtWid.get_tt_wid(Logger(), PARAMS_HEADERS, proxies={"http://": None, "https://": None}))
    print("TikTok",
          await TtWidTikTok.get_tt_wid(Logger(), PARAMS_HEADERS_TIKTOK,
                                       cookie="需要填入 Cookie",
                                       proxy="http://localhost:10809"))


if __name__ == "__main__":
    run(demo())
