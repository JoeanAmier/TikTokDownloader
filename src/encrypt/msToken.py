from asyncio import run
from json import dumps
from random import randint
from string import ascii_lowercase, ascii_uppercase, digits
from time import time
from typing import TYPE_CHECKING, Union
from urllib.parse import quote

from src.custom import PARAMS_HEADERS, PARAMS_HEADERS_TIKTOK, USERAGENT
from src.encrypt.ttWid import TtWid
from src.encrypt.xBogus import XBogusTikTok
from src.tools import request_params
from src.translation import _

if TYPE_CHECKING:
    from src.record import BaseLogger, LoggerManager
    from src.testers import Logger

__all__ = ["MsToken", "MsTokenTikTok"]


class MsToken:
    NAME = "msToken"
    # API = "https://mssdk.bytedance.com/web/report"
    API = "https://mssdk.bytedance.com/web/common"
    DATA = {
        "magic": 538969122,
        "version": 1,
        "dataType": 8,
        "strData": "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",
        "tspFromClient": 0,
        "ulr": 0,
    }
    TOKEN = (
        "9cguMjz4GIfQV50B_D49quM-cEyIvWMwWi0gj1bf"
        "-4YprIjt29ZrAxmDb5oIhmzEhwvcmcC4BR_kEZGmXdS1q7Ad3V94izdpXwtxgPPpozVUzQVm7KDrc5H9nfN3pLw="
    )

    @staticmethod
    def get_fake_ms_token(key="msToken", size=156) -> dict:
        """
        根据传入长度产生随机字符串
        """
        base_str = digits + ascii_uppercase + ascii_lowercase
        length = len(base_str) - 1
        return {key: "".join(base_str[randint(0, length)] for _ in range(size))}

    @classmethod
    async def _get_ms_token(
        cls,
        logger: Union["BaseLogger", "LoggerManager", "Logger"],
        params: dict,
        headers: dict,
        proxy: str,
        **kwargs,
    ) -> dict | None:
        if response := await request_params(
            logger,
            cls.API,
            data=dumps(cls.DATA | {"tspFromClient": int(time() * 1000)}),
            headers=headers,
            params=params,
            proxy=proxy,
            **kwargs,
        ):
            return TtWid.extract(logger, response, cls.NAME)
        logger.error(_("获取 {name} 参数失败！").format(name=cls.NAME))

    @classmethod
    async def get_real_ms_token(
        cls,
        logger: Union["BaseLogger", "LoggerManager", "Logger"],
        headers: dict,
        token="",
        proxy: str = None,
        **kwargs,
    ) -> dict | None:
        params = {cls.NAME: token}
        return await cls._get_ms_token(
            logger,
            params,
            headers,
            proxy,
            **kwargs,
        )

    @classmethod
    async def get_long_ms_token(
        cls,
        logger: Union["BaseLogger", "LoggerManager", "Logger"],
        headers: dict,
        token="",
        proxy: str = None,
        **kwargs,
    ) -> dict | None:
        return await cls.get_real_ms_token(
            logger,
            headers,
            token or cls.TOKEN,
            proxy,
            **kwargs,
        )


class MsTokenTikTok(MsToken):
    REFERER = "https://www.tiktok.com/"
    API = "https://mssdk-ttp2.tiktokw.us/web/report"
    DATA = {
        "magic": 538969122,
        "version": 1,
        "dataType": 8,
        "strData": "3DWMSoJNifh/BoM1CDv7lbH3G7vd6C7zPt0YWMVrYRi369yWaBxCOhq+WMznjr1QWKkr/uLgcnRh+LQDtMl/JDLHSPlEqNPz"
        "/iuxeOktia3YM/pJtUX4EQYqBMW8uAx4qFcN8M5H5XhB1FEkk76W09Xq5DwtcjoO4dpH18G3UcI1hasCXVW8B"
        "+igwPIeEuOIayxuf3OZlTmZbNI1guSUBbccxoph0SEb1TVc4/DeQjQvXkXZOmuN144LcENdtflWmcQPqcwnfD2bWGuR4"
        "+LUgRke1GcyVYa440PH/VOm+DYNcbKeBG87gqTHg+Y724ph1RQKlKX4nsi7Wa+V08ESimNbT8DMsbA"
        "//MovFbr0CiVmvqtXg6VLloJH7UlZRQTC7T0l90KssOt0Y4T/H2EbU5XywcZd8OpICK4wB"
        "/m8KuHGzrheYGmIfxUQtWhrlJdtqzoNI/GiEceTHxp4NahNof4KH6+BZMv87B7nYyE2x7eH2AaeG8iVoiyYKrE7ckQX8mjvj12"
        "+BIkhUiKhpe3SGewK0iEB8NYH3fSqap/QnGsYcSy3lCwHlq7wHUcNdwhKFXkMS65Op"
        "/zpS4uOEZqK9a0v8iGwBrd1VSfFki7sXGUFm5fGMh1Z9Z+4tycL7MYk5fzdUkZ+e56h4p5vPg4qpG17ntvn1LcXR/HXZKgMlx"
        "+qqd3hOpnFOGcC2PahUp+zQ3Y/pZ3Jr+0XRmlHm4zpDmYJkqo3XZrTetOI5JwBkTN/GUkWyVC8hV48WyXpUxUiSHSBeN17735"
        "+PrijcAZh/1+R"
        "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",
    }
    TOKEN = (
        "DFrAJZtLAY2Lrd8Tvmh5cqHYng42N9aIQxG0Rhos9kNznkm4oSeGUOmPptqIveuXzrQARNP"
        "-F08uUkIaCQo_kaYSN6d7X5pQIM8pOFckqCgBLbTMqTZC9rEheMlW88EOKPMVBJ7t-CGQDTTfx0k8tEyx"
    )

    @classmethod
    async def get_real_ms_token(
        cls,
        logger: Union["BaseLogger", "LoggerManager", "Logger"],
        headers: dict,
        token="",
        proxy: str = None,
        **kwargs,
    ) -> dict | None:
        params = {cls.NAME: token}
        if token:
            headers |= {"Cookie": f"{cls.NAME}={token}"}
            params["X-Bogus"] = quote(
                XBogusTikTok().get_x_bogus(
                    params, user_agent=headers.get("User-Agent", USERAGENT)
                ),
                safe="",
            )
        return await cls._get_ms_token(
            logger,
            params,
            headers,
            proxy,
            **kwargs,
        )


async def test():
    from src.testers import Logger

    print("抖音", await MsToken.get_real_ms_token(Logger(), PARAMS_HEADERS, proxy=None))
    print(
        "抖音",
        await MsToken.get_long_ms_token(
            Logger(),
            PARAMS_HEADERS,
            proxy=None,
        ),
    )
    print(
        "TikTok",
        await MsTokenTikTok.get_real_ms_token(
            Logger(), PARAMS_HEADERS_TIKTOK, proxy="http://127.0.0.1:10809"
        ),
    )
    print(
        "TikTok",
        await MsTokenTikTok.get_long_ms_token(
            Logger(), PARAMS_HEADERS_TIKTOK, proxy="http://127.0.0.1:10809"
        ),
    )


if __name__ == "__main__":
    run(test())
