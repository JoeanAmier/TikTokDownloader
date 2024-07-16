from typing import Callable
from typing import TYPE_CHECKING

from .template import APITikTok

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["DetailTikTok"]


class DetailTikTok(APITikTok):
    def __init__(self,
                 params: "Parameter",
                 cookie: str = None,
                 proxy: str = None,
                 detail_id: str = "",
                 ):
        super().__init__(params, cookie, proxy, )
        self.detail_id = detail_id
        self.api = f"{self.domain}/api/item/detail/"
        self.text = "Dữ liệu videos" #作品数据

    def generate_params(self, ) -> dict:
        return self.params | {
            "itemId": self.detail_id,
        }

    async def run(self,
                  referer: str = None,
                  single_page=True,
                  data_key: str = None,
                  error_text="",
                  cursor=None,
                  has_more=None,
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
            error_text or f"Không lấy được dữ liệu cho công việc {self.detail_id}", # 作品 {self.detail_id} 获取数据失败作品 {self.detail_id} 获取数据失败
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
                       data_key: str = None,
                       error_text="",
                       cursor=None,
                       has_more=None,
                       *args,
                       **kwargs,
                       ):
        try:
            if not (d := data_dict["itemInfo"]["itemStruct"]):
                self.log.info(error_text)
            else:
                self.response = d
        except KeyError:
            self.log.error(f"Phân tích dữ liệu không thành công, vui lòng thông báo cho tác giả để xử lý: {data_dict}") #数据解析失败，请告知作者处理
