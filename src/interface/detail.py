from typing import Callable
from typing import TYPE_CHECKING

from .template import API

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["Detail"]


class Detail(API):
    def __init__(self,
                 params: "Parameter",
                 cookie: str = None,
                 proxy: str = None,
                 detail_id: str = "",
                 ):
        super().__init__(params, cookie, proxy, )
        self.detail_id = detail_id
        self.api = f"{self.domain}aweme/v1/web/aweme/detail/"
        self.text = "Dữ liệu videos" #作品数据

    def generate_params(self, ) -> dict:
        return self.params | {
            "aweme_id": self.detail_id,
            "version_code": "190500",
            "version_name": "19.5.0",
        }

    async def run(self,
                  referer: str = None,
                  single_page=True,
                  data_key: str = "aweme_detail",
                  error_text="",
                  cursor="cursor",
                  has_more="has_more",
                  params: Callable = lambda: {},
                  data: Callable = lambda: {},
                  method="GET",
                  headers: dict = None,
                  *args,
                  **kwargs,
                  ):
        return await super().run(
            referer,
            single_page,
            data_key,
            error_text or f"Không lấy được dữ liệu videos {self.detail_id}", #作品 {self.detail_id} 获取数据失败
            cursor,
            has_more,
            params,
            data,
            method,
            headers,
            *args,
            **kwargs,
        )

    def check_response(self,
                       data_dict: dict,
                       data_key: str,
                       error_text="",
                       cursor="cursor",
                       has_more="has_more",
                       *args,
                       **kwargs,
                       ):
        try:
            if not (d := data_dict[data_key]):
                self.log.info(error_text)
            else:
                self.response = d
        except KeyError:
            self.log.error(f"Phân tích dữ liệu không thành công, vui lòng thông báo cho tác giả để xử lý: {data_dict}") #数据解析失败，请告知作者处理
