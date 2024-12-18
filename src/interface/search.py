from json import dumps
from types import SimpleNamespace
from typing import TYPE_CHECKING
from typing import Union
from urllib.parse import quote

from src.interface.template import API
from src.testers import Params
from src.tools import TikTokDownloaderError

if TYPE_CHECKING:
    from src.config import Parameter


class Search(API):
    search_params = (
        SimpleNamespace(
            note="综合搜索",
            api=f"{API.domain}aweme/v1/web/general/search/single/",
            count=10,
            channel="aweme_general",
            type="general",
        ),
        SimpleNamespace(
            note="视频搜索",
            api=f"{API.domain}aweme/v1/web/search/item/",
            count=20,
            channel="aweme_video_web",
            type="video",
        ),
        SimpleNamespace(
            note="用户搜索",
            api=f"{API.domain}aweme/v1/web/discover/search/",
            count=12,
            channel="aweme_user_web",
            type="user",
        ),
        SimpleNamespace(
            note="直播搜索",
            api=f"{API.domain}aweme/v1/web/live/search/",
            count=15,
            channel="aweme_live",
            type="live",
        ),
        SimpleNamespace(
            note=None,
            api=None,
            count=None,
            channel=None,
            type=None,
        ),
    )
    channel_map = {
        0: search_params[0],
        1: search_params[1],
        2: search_params[2],
        3: search_params[3],
    }
    sort_type_map = {
        0,  # 综合排序
        1,  # 最多点赞
        2,  # 最新发布
    }
    publish_time_map = {
        0,  # 不限
        1,  # 一天内
        7,  # 一周内
        180,  # 半年内
    }
    duration_map = {
        0: "",  # 不限
        1: "0-1",  # 一分钟以内
        2: "1-5",  # 一到五分钟
        3: "5-10000",  # 五分钟以上
    }
    content_type_map = {
        0,  # 不限
        1,  # 视频
        2,  # 图文
    }

    def __init__(
            self,
            params: Union["Parameter", Params],
            cookie: str = None,
            proxy: str = None,
            key_word: str = ...,
            channel: int = 0,
            pages: int = 99999,
            sort_type: int = 0,
            publish_time: int = 0,
            duration: int = 0,
            content_type: int = 0,
            cursor: int = 0,
            count: int = None,
            *args,
            **kwargs,
    ):
        super().__init__(params, cookie, proxy, *args, **kwargs, )
        self.key_word = key_word
        self.channel = self.channel_map.get(channel, self.search_params[-1])
        self.pages = pages
        self.sort_type = sort_type
        self.publish_time = publish_time
        self.duration = self.duration_map.get(duration, "")
        self.content_type = content_type
        self.cursor = cursor
        self.count = count or self.channel.count
        self.type = self.channel.type
        self.api = self.channel.api
        self.text = f"{self.channel.note}"
        self.filter_selected = self.generate_filter_selected()
        self.search_id = None
        self.params_func = {
            0: self.generate_params_general,
        }.get(channel)

    async def run(self, single_page=False, *args, **kwargs):
        if not self.api:
            raise TikTokDownloaderError
        self.set_referer(f"https://www.douyin.com/root/search/{quote(self.key_word)}?type={self.type}")
        match single_page:
            case True:
                await self.run_single(
                    "data",
                    params=self.params_func,
                    *args,
                    **kwargs,
                )
            case False:
                await self.run_batch(
                    "data",
                    params=self.params_func,
                    *args,
                    **kwargs,
                )
            case _:
                raise TikTokDownloaderError
        return self.response

    def generate_filter_selected(self, ) -> str | None:
        if any((
                self.sort_type,
                self.publish_time,
                self.duration,
                self.content_type,
        )):
            return dumps(
                {
                    "sort_type": f"{self.sort_type}",
                    "publish_time": f"{self.publish_time}",
                    "filter_duration": f"{self.duration}",
                    "content_type": f"{self.content_type}",
                },
                separators=(",", ":"),
            )

    def generate_params_general(self, ) -> dict:
        params = self.params | {
            "search_channel": self.channel.channel,
            "enable_history": "1",
            "keyword": self.key_word,
            "search_source": "tab_search",
            "query_correct_type": "1",
            "is_filter_search": "0",
            "from_group_id": "",
            "offset": self.cursor,
            "count": self.count,
            "need_filter_settings": "1",
            "list_type": "single",
            "version_code": "190600",
            "version_name": "19.6.0",
        }
        if self.search_id:
            params |= {"search_id": self.search_id}
        if self.filter_selected:
            params |= {
                "filter_selected": self.filter_selected,
                "is_filter_search": "1",
            }
        return params

    def check_response(
            self,
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
                self.log.warning(error_text)
                self.finished = True
            else:
                self.cursor = data_dict[cursor]
                self.search_id = data_dict["log_pb"]["impr_id"]
                self.append_response(d)
                self.finished = not data_dict[has_more]
        except KeyError:
            self.log.error(f"数据解析失败，请告知作者处理: {data_dict}")
            self.finished = True


async def test():
    async with Params() as params:
        i = Search(
            params,
            key_word="玉足",
            pages=2,
        )
        print(await i.run())


if __name__ == "__main__":
    from asyncio import run

    run(test())
