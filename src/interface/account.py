from datetime import date, datetime, timedelta
from typing import TYPE_CHECKING, Callable, Coroutine, Type, Union

from src.interface.template import API
from src.translation import _

if TYPE_CHECKING:
    from src.config import Parameter
    from src.testers import Params


class Account(API):
    post_api = f"{API.domain}aweme/v1/web/aweme/post/"
    favorite_api = f"{API.domain}aweme/v1/web/aweme/favorite/"

    def __init__(
        self,
        params: Union["Parameter", "Params"],
        cookie: str = "",
        proxy: str = None,
        sec_user_id: str = ...,
        tab="post",
        earliest: str | float | int = "",
        latest: str | float | int = "",
        pages: int = None,
        cursor=0,
        count=18,
        *args,
        **kwargs,
    ):
        super().__init__(params, cookie, proxy, *args, **kwargs)
        self.sec_user_id = sec_user_id
        self.api, self.favorite, self.pages = self.check_type(
            tab, pages or params.max_pages
        )
        # TODO: 重构数据验证逻辑
        self.latest: date = self.check_latest(latest)
        self.earliest: date = self.check_earliest(earliest)
        self.cursor = cursor
        self.count = count
        self.text = _("账号喜欢作品") if self.favorite else _("账号发布作品")

    async def run(
        self,
        referer: str = None,
        single_page=False,
        data_key: str = "aweme_list",
        error_text="",
        cursor="max_cursor",
        has_more="has_more",
        params: Callable = lambda: {},
        data: Callable = lambda: {},
        method="GET",
        headers: dict = None,
        *args,
        **kwargs,
    ):
        if self.favorite:
            self.set_referer(f"{self.domain}user/{self.sec_user_id}?showTab=like")
        else:
            self.set_referer(f"{self.domain}user/{self.sec_user_id}")
        match single_page:
            case True:
                await self.run_single(
                    data_key,
                    error_text
                    or _(
                        "该账号为私密账号，需要使用登录后的 Cookie，且登录的账号需要关注该私密账号"
                    ),
                    cursor,
                    has_more,
                    params,
                    data,
                    method,
                    headers,
                    *args,
                    **kwargs,
                )
                return self.response
            case False:
                await self.run_batch(
                    data_key,
                    error_text
                    or _(
                        "该账号为私密账号，需要使用登录后的 Cookie，且登录的账号需要关注该私密账号"
                    ),
                    cursor,
                    has_more,
                    params,
                    data,
                    method,
                    headers,
                    *args,
                    **kwargs,
                )
                return self.response, self.earliest, self.latest
        raise ValueError

    async def run_single(
        self,
        data_key: str = "aweme_list",
        error_text="",
        cursor="max_cursor",
        has_more="has_more",
        params: Callable = lambda: {},
        data: Callable = lambda: {},
        method="GET",
        headers: dict = None,
        *args,
        **kwargs,
    ):
        await super().run_single(
            data_key,
            error_text,
            cursor,
            has_more,
            params,
            data,
            method,
            headers,
            *args,
            **kwargs,
        )

    async def run_batch(
        self,
        data_key: str = "aweme_list",
        error_text="",
        cursor="max_cursor",
        has_more="has_more",
        params: Callable = lambda: {},
        data: Callable = lambda: {},
        method="GET",
        headers: dict = None,
        callback: Type[Coroutine] = None,
        *args,
        **kwargs,
    ):
        await super().run_batch(
            data_key,
            error_text,
            cursor,
            has_more,
            params,
            data,
            method,
            headers,
            callback=callback or self.early_stop,
            *args,
            **kwargs,
        )
        self.summary_works()

    async def early_stop(self):
        """如果获取数据的发布日期已经早于限制日期，就不需要再获取下一页的数据了"""
        if (
            not self.favorite
            and self.earliest
            > datetime.fromtimestamp(max(int(self.cursor) / 1000, 0)).date()
        ):
            self.finished = True

    def generate_params(
        self,
    ) -> dict:
        match self.favorite:
            case True:
                return self.generate_favorite_params()
            case False:
                return self.generate_post_params()

    def generate_favorite_params(self) -> dict:
        return self.params | {
            "sec_user_id": self.sec_user_id,
            "max_cursor": self.cursor,
            "min_cursor": "0",
            "whale_cut_token": "",
            "cut_version": "1",
            "count": self.count,
            "publish_video_strategy_type": "2",
            "version_code": "170400",
            "version_name": "17.4.0",
        }

    def generate_post_params(self) -> dict:
        return self.params | {
            "sec_user_id": self.sec_user_id,
            "max_cursor": self.cursor,
            "locate_query": "false",
            "show_live_replay_strategy": "1",
            "need_time_list": "1",
            "time_list_query": "0",
            "whale_cut_token": "",
            "cut_version": "1",
            "count": self.count,
            "publish_video_strategy_type": "2",
        }

    def check_type(self, tab: str, pages: int) -> tuple[str, bool, int]:
        match tab:
            case "favorite":
                return self.favorite_api, True, pages
            case "post":
                pass
            case _:
                self.log.warning(
                    _("tab 参数 {tab} 设置错误，程序将使用默认值: post").format(tab=tab)
                )
        return self.post_api, False, 99999

    def check_earliest(self, date_: str | float | int) -> date:
        return self.check_date(date(2016, 9, 20), self.latest, _("最早"), date_)

    def check_latest(self, date_: str | float | int) -> date:
        return self.check_date(date.today(), date.today(), _("最晚"), date_)

    def check_date(
        self, default: date, start: date, tip: str, value: str | float | int
    ) -> date:
        if not value:
            return default
        if isinstance(value, (int, float)):
            date_ = start - timedelta(days=value)
        elif isinstance(value, str):
            try:
                date_ = datetime.strptime(value, "%Y/%m/%d").date()
            except ValueError:
                self.log.warning(
                    _("作品{tip}发布日期无效 {date}").format(tip=tip, date=value)
                )
                return default
        else:
            raise ValueError(
                _("作品{tip}发布日期参数 {date} 类型错误").format(tip=tip, date=value)
            )
        self.log.info(
            _("作品{tip}发布日期: {latest_date}").format(tip=tip, latest_date=date_)
        )
        return date_  # 返回 date 对象

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
                self.append_response(d)
                self.finished = not data_dict[has_more]
        except KeyError:
            if data_dict.get("status_code") == 0:
                self.log.warning(_("配置文件 cookie 参数未登录，数据获取已提前结束"))
            else:
                self.log.error(
                    _("数据解析失败，请告知作者处理: {data}").format(data=data_dict)
                )
            self.finished = True


async def test():
    from src.testers import Params

    async with Params() as params:
        i = Account(
            params,
            sec_user_id="",
        )
        print(await i.run())


if __name__ == "__main__":
    from asyncio import run

    run(test())
