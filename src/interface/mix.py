from typing import TYPE_CHECKING

from src.extract import Extractor
from .detail import Detail
from .template import API

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["Mix"]


class Mix(API):
    def __init__(self,
                 params: "Parameter",
                 cookie: str = None,
                 proxy: str = None,
                 mix_id: str = None,
                 detail_id: str = None,
                 cursor=0,
                 count=20,
                 *args,
                 **kwargs,
                 ):
        super().__init__(params, cookie, proxy, *args, **kwargs, )
        self.mix_id = mix_id
        self.detail_id = detail_id
        self.count = count
        self.cursor = cursor
        self.api = f"{self.domain}aweme/v1/web/mix/aweme/"
        self.text = "合集作品数据"
        self.detail = Detail(params, cookie, proxy, self.detail_id, )

    def generate_params(self, *args, **kwargs) -> dict:
        return self.params | {
            "mix_id": self.mix_id,
            "cursor": self.cursor,
            "count": self.count,
            "version_code": "170400",
            "version_name": "17.4.0",
        }

    async def run(self,
                  referer: str = None,
                  single_page=False,
                  data_key: str = "aweme_list",
                  error_text="",
                  cursor="cursor",
                  has_more="has_more",
                  params: dict = None,
                  data: dict = None,
                  method="get",
                  headers: dict = None,
                  proxy: str = None,
                  *args,
                  **kwargs,
                  ):
        await self.__get_mix_id()
        if not self.mix_id:
            self.log.warning("获取合集 ID 失败")
            return self.response
        return await super().run(
            referer,
            single_page,
            data_key,
            error_text or f"获取{self.text}失败",
            cursor,
            has_more,
            params,
            data,
            method,
            headers,
            proxy,
            *args,
            **kwargs,
        )

    async def __get_mix_id(self):
        if not self.mix_id:
            self.mix_id = Extractor.extract_mix_id(await self.detail.run())
