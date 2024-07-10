from datetime import datetime
from types import SimpleNamespace
from typing import Callable
from typing import TYPE_CHECKING
from typing import Union

from src.interface.template import API
from src.testers import Params

if TYPE_CHECKING:
    from src.config import Parameter


class Hot(API):
    board_params = (
        SimpleNamespace(
            name="抖音热榜",
            type=0,
            sub_type="",
        ),
        SimpleNamespace(
            name="娱乐榜",
            type=2,
            sub_type=2,
        ),
        SimpleNamespace(
            name="社会榜",
            type=2,
            sub_type=4,
        ),
        SimpleNamespace(
            name="挑战榜",
            type=2,
            sub_type="hotspot_challenge",
        ),
    )

    def __init__(self,
                 params: Union["Parameter", Params],
                 cookie: str = None,
                 proxy: str = None,
                 *args,
                 **kwargs,
                 ):
        super().__init__(params, cookie, proxy, *args, **kwargs, )
        self.headers = self.headers | {"Cookie": "", }
        self.api = f"{self.domain}aweme/v1/web/hot/search/list/"
        self.index = None
        self.time = None

    def generate_params(self, ) -> dict:
        return self.params | {
            "detail_list": "1",
            "source": "6",
            "board_type": self.board_params[self.index].type,
            "board_sub_type": self.board_params[self.index].sub_type,
            "version_code": "170400",
            "version_name": "17.4.0",
        }

    async def run(self,
                  referer: str = "https://www.douyin.com/discover",
                  single_page=True,
                  data_key: str = None,
                  error_text=None,
                  cursor=None,
                  has_more=None,
                  params: Callable = lambda: {},
                  data: Callable = lambda: {},
                  method="GET",
                  headers: dict = None,
                  *args,
                  **kwargs,
                  ):
        self.time = f"{datetime.now():%Y_%m_%d_%H_%M_%S}"
        self.set_referer(referer)
        for index, space in enumerate(self.board_params):
            self.index = index
            self.text = f"{space.name}数据"
            await self.run_single(
                data_key,
                f"获取{space.name}数据失败",
                cursor,
                has_more,
                params=self.generate_params,
                data=data,
                method=method,
                headers=headers,
                index=index,
                *args,
                **kwargs,
            )
        return self.time, self.response

    def check_response(self,
                       data_dict: dict,
                       data_key: str = None,
                       error_text=None,
                       cursor=None,
                       has_more=None,
                       index: int = None,
                       *args,
                       **kwargs,
                       ):
        try:
            if not (d := data_dict["data"]["word_list"]):
                self.log.info(error_text)
            else:
                self.response.append((index, d))
        except KeyError:
            self.log.error(f"数据解析失败，请告知作者处理: {data_dict}")
