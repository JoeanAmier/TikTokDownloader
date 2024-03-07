from asyncio import run
from contextlib import suppress
from typing import TYPE_CHECKING

from rich.console import Console

from src.custom import ERROR
from src.tools import request_post

if TYPE_CHECKING:
    from src.module import ColorfulConsole
__all__ = ["TtWid", "TtWidTikTok"]


class TtWid:
    NAME = "ttwid"
    API = "https://ttwid.bytedance.com/ttwid/union/register/"
    DATA = (
        '{"region":"cn","aid":1768,"needFid":false,"service":"www.ixigua.com","migrate_info":'
        '{"ticket":"","source":"node"},"cbUrlProtocol":"https","union":true}')

    @classmethod
    async def get_tt_wid(cls, console: "ColorfulConsole", ) -> dict | None:
        if response := await request_post(console, cls.API, cls.DATA):
            return cls.extract(console, response, cls.NAME)
        console.print(f"获取 {cls.NAME} 参数失败！", style=ERROR)

    @staticmethod
    def extract(console: "ColorfulConsole", headers, key: str) -> dict | None:
        if c := headers.get("Set-Cookie"):
            with suppress(IndexError):
                kv = c.split("; ")[0].split("=", 1)
                return {kv[0]: kv[1]}
        console.print(f"获取 {key} 参数失败！", style=ERROR)


class TtWidTikTok(TtWid):
    pass


async def debug():
    print(await TtWid.get_tt_wid(Console()))


if __name__ == "__main__":
    run(debug())
