from json import dumps
from types import SimpleNamespace
from typing import TYPE_CHECKING
from typing import Union
from urllib.parse import quote

from src.interface.template import API
from src.testers import Params
from src.tools import TikTokDownloaderError
from src.translation import _

if TYPE_CHECKING:
    from src.config import Parameter


class Search(API):
    search_params = (
        SimpleNamespace(
            note=_("综合搜索"),
            api=f"{API.domain}aweme/v1/web/general/search/single/",
            channel="aweme_general",
            type="general",
            key="data",
        ),
        SimpleNamespace(
            note=_("视频搜索"),
            api=f"{API.domain}aweme/v1/web/search/item/",
            channel="aweme_video_web",
            type="video",
            key="data",
        ),
        SimpleNamespace(
            note=_("用户搜索"),
            api=f"{API.domain}aweme/v1/web/discover/search/",
            channel="aweme_user_web",
            type="user",
            key="user_list",
        ),
        SimpleNamespace(
            note=_("直播搜索"),
            api=f"{API.domain}aweme/v1/web/live/search/",
            channel="aweme_live",
            type="live",
            key="data",
        ),
        SimpleNamespace(
            note=None,
            api=None,
            channel=None,
            type=None,
            key=None,
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
    douyin_user_fans_map = {
        0: [""],  # 不限
        1: ["0_1k"],  # 1000以下
        2: ["1k_1w"],  # 1000-1w
        3: ["1w_10w"],  # 1w-10w
        4: ["10w_100w"],  # 10w-100w
        5: ["100w_"],  # 100w以上
    }
    douyin_user_type_map = {
        0: [""],  # 不限
        1: ["common_user"],  # 普通用户
        2: ["enterprise_user"],  # 企业认证
        3: ["personal_user"]  # 个人认证
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
            douyin_user_fans: int = 0,
            douyin_user_type: int = 0,
            cursor: int = 0,
            count: int = 10,
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
        self.douyin_user_fans = self.douyin_user_fans_map.get(douyin_user_fans, [""])
        self.douyin_user_type = self.douyin_user_type_map.get(douyin_user_type, [""])
        self.cursor = cursor
        self.count = count
        self.type = self.channel.type
        self.api = self.channel.api
        self.key = self.channel.key
        self.text = f"{self.channel.note}"
        self.filter_selected = self.generate_filter_selected() if channel == 0 else None
        self.search_filter_value = self.generate_search_filter_value() if channel == 2 else None
        self.search_id = None
        self.params_func = {
            0: self._generate_params_general,
            1: self._generate_params_video,
            2: self._generate_params_user,
            3: self._generate_params_live,
        }.get(channel)

    async def run(self, single_page=False, *args, **kwargs):
        if not self.api:
            raise TikTokDownloaderError
        self.set_referer(f"{self.domain}root/search/{quote(self.key_word)}?type={self.type}")
        match single_page:
            case True:
                await self.run_single(
                    self.channel.key,
                    params=self.params_func,
                    *args,
                    **kwargs,
                )
            case False:
                await self.run_batch(
                    self.channel.key,
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

    def generate_search_filter_value(self, ) -> str | None:
        if any((
                self.douyin_user_fans,
                self.douyin_user_type,
        )):
            return dumps(
                {
                    "douyin_user_fans": self.douyin_user_fans,
                    "douyin_user_type": self.douyin_user_type, }
                ,
                separators=(",", ":"),
            )

    def _generate_params_general(self, ) -> dict:
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
            "need_filter_settings": "0",
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

    def _generate_params_video(self, ) -> dict:
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
            "need_filter_settings": "0",
            "list_type": "single",
            "version_code": "170400",
            "version_name": "17.4.0",
        }
        if self.search_id:
            params |= {"search_id": self.search_id}
        if self.sort_type:
            params |= {
                "sort_type": f"{self.sort_type}",
                "is_filter_search": "1",
            }
        if self.publish_time:
            params |= {
                "publish_time": f"{self.publish_time}",
                "is_filter_search": "1",
            }
        if self.duration:
            params |= {
                "filter_duration": f"{self.duration}",
                "is_filter_search": "1",
            }
        return params

    def _generate_params_user(self, ) -> dict:
        params = self._generate_params_live()
        if self.search_filter_value:
            params |= {
                "search_filter_value": self.search_filter_value,
                "is_filter_search": "1",
            }
        return params

    def _generate_params_live(self, ) -> dict:
        params = self.params | {
            "search_channel": self.channel.channel,
            "keyword": self.key_word,
            "search_source": "tab_search",
            "query_correct_type": "1",
            "is_filter_search": "0",
            "from_group_id": "",
            "offset": self.cursor,
            "count": self.count,
            "need_filter_settings": "0",
            "list_type": "single",
            "version_code": "170400",
            "version_name": "17.4.0",
        }
        if self.search_id:
            params |= {"search_id": self.search_id}
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
                match self.type:
                    case "general" | "user":
                        self.append_response(d)
                    case "video":
                        self.append_response_video(d, "aweme_info", )
                    case "live":
                        self.append_response_video(d, "lives", )
                    case _:
                        raise TikTokDownloaderError
                self.finished = not data_dict[has_more]
        except KeyError:
            self.log.error(_("数据解析失败，请告知作者处理: {data}").format(data=data_dict))
            self.finished = True

    def append_response_video(self, data: list[dict], key: str, ) -> None:
        self.append_response([i[key] for i in data])


async def test():
    async with Params() as params:
        i = Search(
            params,
            key_word="玉足",
            channel=3,
            sort_type=2,
            publish_time=7,
            duration=2,
            douyin_user_fans=5,
            pages=1,
        )
        print(await i.run())


if __name__ == "__main__":
    from asyncio import run

    run(test())
