from asyncio import run
from re import compile
from typing import TYPE_CHECKING, Union

from src.custom import PARAMS_HEADERS_TIKTOK
from src.tools import request_params

if TYPE_CHECKING:
    from src.record import BaseLogger, LoggerManager
    from src.testers import Logger


class DeviceId:
    NAME = "device_id"
    URL = "https://www.tiktok.com/explore"
    DEVICE_ID = compile(r'"wid":"(\d{19})"')

    @classmethod
    async def get_device_id(
        cls,
        logger: Union["BaseLogger", "LoggerManager", "Logger"],
        headers: dict,
        **kwargs,
    ) -> [str, str]:
        response = await request_params(
            logger,
            cls.URL,
            "GET",
            headers=headers,
            resp="response",
            **kwargs,
        )
        response.raise_for_status()
        device_id = d.group(1) if (d := cls.DEVICE_ID.search(response.text)) else ""
        cookie = "; ".join(
            [f"{key}={value}" for key, value in response.cookies.items()]
        )
        return device_id, cookie

    @classmethod
    async def get_device_ids(
        cls,
        logger: Union["BaseLogger", "LoggerManager", "Logger"],
        headers: dict,
        number: int,
        **kwargs,
    ) -> [[str, str]]:
        return [
            await cls.get_device_id(
                logger,
                headers,
                **kwargs,
            )
            for _ in range(number)
        ]


async def test():
    from src.testers import Logger

    print(
        await DeviceId.get_device_id(
            Logger(),
            PARAMS_HEADERS_TIKTOK,
            proxy="http://127.0.0.1:10809",
        )
    )
    # print(await DeviceId.get_device_ids(
    #     Logger(),
    #     PARAMS_HEADERS_TIKTOK,
    #     5,
    #     proxy="http://127.0.0.1:10809",
    # ))


if __name__ == "__main__":
    run(test())
