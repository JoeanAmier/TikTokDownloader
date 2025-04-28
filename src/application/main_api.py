from typing import TYPE_CHECKING

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import RedirectResponse
from uvicorn import Config, Server
from textwrap import dedent

from models import DetailTikTok
from ..custom import (
    __VERSION__,
    REPOSITORY,
    SERVER_HOST,
    SERVER_PORT,
    VERSION_BETA,
    is_valid_token,
)
from ..models import (
    GeneralSearch,
    LiveSearch,
    DataResponse,
    UserSearch,
    VideoSearch,
    Settings,
    ShortUrl,
    UrlResponse,
    Detail,
)
from ..translation import _
from .main_complete import TikTok

if TYPE_CHECKING:
    from ..config import Parameter
    from ..manager import Database

__all__ = ["APIServer"]


def token_dependency(token: str = Header(None)):
    if not is_valid_token(token):
        raise HTTPException(
            status_code=403,
            detail=_("无效令牌！"),
        )


class APIServer(TikTok):
    def __init__(
        self,
        parameter: "Parameter",
        database: "Database",
    ):
        super().__init__(
            parameter,
            database,
        )
        self.server = None

    async def handle_redirect(self, text: str, proxy: str = None) -> str:
        return await self.links.run(
            text,
            "",
            proxy,
        )

    async def handle_redirect_tiktok(self, text: str, proxy: str = None) -> str:
        return await self.links_tiktok.run(
            text,
            "",
            proxy,
        )

    async def run_server(
        self,
        host=SERVER_HOST,
        port=SERVER_PORT,
        log_level="info",
    ):
        self.server = FastAPI(
            debug=VERSION_BETA,
            title="TikTokDownloader",
            version=__VERSION__,
        )
        self.setup_routes()
        config = Config(
            self.server,
            host=host,
            port=port,
            log_level=log_level,
        )
        server = Server(config)
        await server.serve()

    def setup_routes(self):
        @self.server.get(
            "/",
            summary=_("访问项目 GitHub 仓库"),
            description=_("重定向至项目 GitHub 仓库主页"),
            tags=[_("项目")],
        )
        async def index():
            return RedirectResponse(url=REPOSITORY)

        @self.server.get(
            "/token",
            summary=_("测试令牌有效性"),
            tags=[_("项目")],
            response_model=DataResponse,
        )
        async def handle_test(token: str = Depends(token_dependency)):
            return DataResponse(
                message=_("验证成功！"),
                data=None,
                params=None,
            )

        @self.server.post(
            "/settings",
            summary=_("更新项目全局配置"),
            description=dedent(
                _("""
            待更新
            """)
            ),
            tags=[_("配置")],
            response_model=Settings,
        )
        async def handle_settings(
            extract: Settings, token: str = Depends(token_dependency)
        ):
            await self.parameter.set_settings_data(extract.model_dump())
            return Settings(**self.parameter.get_settings_data())

        @self.server.get(
            "/settings",
            summary=_("获取项目全局配置"),
            description=dedent(
                _("""
                待更新
                        """)
            ),
            tags=[_("配置")],
            response_model=Settings,
        )
        async def get_settings(token: str = Depends(token_dependency)):
            return Settings(**self.parameter.get_settings_data())

        @self.server.post(
            "/douyin/share",
            summary=_("获取分享链接重定向的完整链接"),
            description=dedent(
                _("""
                待更新
                        """)
            ),
            tags=[_("抖音")],
            response_model=UrlResponse,
        )
        async def handle_share(
            extract: ShortUrl, token: str = Depends(token_dependency)
        ):
            if url := await self.handle_redirect(extract.text, extract.proxy):
                return UrlResponse(
                    message=_("请求成功！"),
                    url=url,
                    params=extract.model_dump(),
                )
            return UrlResponse(
                message=_("请求失败！"),
                url=None,
                params=extract.model_dump(),
            )

        @self.server.post(
            "/douyin/detail",
            summary=_("获取作品数据"),
            description=dedent(
                _("""
                待更新
                        """)
            ),
            tags=[_("抖音")],
            response_model=DataResponse,
        )
        async def handle_detail(
            extract: Detail, token: str = Depends(token_dependency)
        ):
            root, params, logger = self.record.run(self.parameter)
            async with logger(root, console=self.console, **params) as record:
                if data := await self._handle_detail(
                    [extract.detail_id],
                    False,
                    record,
                    True,
                    extract.source,
                    extract.cookie,
                    extract.proxy,
                ):
                    return DataResponse(
                        message=_("获取成功！"),
                        data=data[0],
                        params=extract.model_dump(),
                    )
                return DataResponse(
                    message=_("获取失败！"),
                    data=None,
                    params=extract.model_dump(),
                )

        @self.server.post(
            "/douyin/search/general",
            summary=_("获取综合搜索数据"),
            description=dedent(
                _("""
                待更新
                        """)
            ),
            tags=[_("抖音")],
            response_model=DataResponse,
        )
        async def handle_general(
            extract: GeneralSearch, token: str = Depends(token_dependency)
        ):
            return await self.handle_search(extract)

        @self.server.post(
            "/douyin/search/video",
            summary=_("获取视频搜索数据"),
            description=dedent(
                _("""
                待更新
                        """)
            ),
            tags=[_("抖音")],
            response_model=DataResponse,
        )
        async def handle_video(
            extract: VideoSearch, token: str = Depends(token_dependency)
        ):
            return await self.handle_search(extract)

        @self.server.post(
            "/douyin/search/user",
            summary=_("获取用户搜索数据"),
            description=dedent(
                _("""
                待更新
                        """)
            ),
            tags=[_("抖音")],
            response_model=DataResponse,
        )
        async def handle_user(
            extract: UserSearch, token: str = Depends(token_dependency)
        ):
            return await self.handle_search(extract)

        @self.server.post(
            "/douyin/search/live",
            summary=_("获取直播搜索数据"),
            description=dedent(
                _("""
                待更新
                        """)
            ),
            tags=[_("抖音")],
            response_model=DataResponse,
        )
        async def handle_live(
            extract: LiveSearch, token: str = Depends(token_dependency)
        ):
            return await self.handle_search(extract)

        @self.server.post(
            "/tiktok/share",
            summary=_("获取分享链接重定向的完整链接"),
            description=dedent(
                _("""
                待更新
                        """)
            ),
            tags=["TikTok"],
            response_model=UrlResponse,
        )
        async def handle_share_tiktok(
            extract: ShortUrl, token: str = Depends(token_dependency)
        ):
            if url := await self.handle_redirect_tiktok(extract.text, extract.proxy):
                return UrlResponse(
                    message=_("请求成功！"),
                    url=url,
                    params=extract.model_dump(),
                )
            return UrlResponse(
                message=_("请求失败！"),
                url=None,
                params=extract.model_dump(),
            )

        @self.server.post(
            "/tiktok/detail",
            summary=_("获取作品数据"),
            description=dedent(
                _("""
                待更新
                        """)
            ),
            tags=["TikTok"],
            response_model=DataResponse,
        )
        async def handle_detail_tiktok(
            extract: DetailTikTok, token: str = Depends(token_dependency)
        ):
            root, params, logger = self.record.run(self.parameter)
            async with logger(root, console=self.console, **params) as record:
                if data := await self._handle_detail(
                    [extract.detail_id],
                    True,
                    record,
                    True,
                    extract.source,
                    extract.cookie,
                    extract.proxy,
                ):
                    return DataResponse(
                        message=_("获取成功！"),
                        data=data[0],
                        params=extract.model_dump(),
                    )
                return DataResponse(
                    message=_("获取失败！"),
                    data=None,
                    params=extract.model_dump(),
                )

    async def handle_search(self, extract):
        if data := await self.deal_search_data(
            extract,
            extract.source,
        ):
            return DataResponse(
                message=_("获取成功！"),
                data=data,
                params=extract.model_dump(),
            )
        return DataResponse(
            message=_("获取失败！"),
            data=data,
            params=extract.model_dump(),
        )
