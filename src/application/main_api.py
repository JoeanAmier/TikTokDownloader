from typing import TYPE_CHECKING

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import RedirectResponse
from uvicorn import Config, Server

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
    Response,
    UserSearch,
    VideoSearch,
    Settings,
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
            summary=_("项目仓库"),
            description=_("重定向至项目仓库"),
            tags=[_("项目")],
        )
        async def index():
            return RedirectResponse(url=REPOSITORY)

        @self.server.get(
            "/token",
            summary=_("令牌验证"),
            description=_("用于测试令牌有效性"),
            tags=[_("项目")],
            response_model=Response,
        )
        async def handle_test(token: str = Depends(token_dependency)):
            return Response(
                message=_("令牌验证成功！"),
                data=None,
                params=None,
            )

        @self.server.post(
            "/settings",
            summary=_("更新配置"),
            description=_("更新项目全局配置"),
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
            summary=_("查看配置"),
            description=_("获取项目全局配置"),
            tags=[_("配置")],
            response_model=Settings,
        )
        async def get_settings(token: str = Depends(token_dependency)):
            return Settings(**self.parameter.get_settings_data())

        @self.server.post(
            "/douyin/search/general",
            summary=_("综合搜索"),
            description=_("获取综合搜索数据"),
            tags=[_("抖音")],
            response_model=Response,
        )
        async def handle_general(
            extract: GeneralSearch, token: str = Depends(token_dependency)
        ):
            return await self.handle_search(extract)

        @self.server.post(
            "/douyin/search/video",
            summary=_("视频搜索"),
            description=_("获取视频搜索数据"),
            tags=[_("抖音")],
            response_model=Response,
        )
        async def handle_video(
            extract: VideoSearch, token: str = Depends(token_dependency)
        ):
            return await self.handle_search(extract)

        @self.server.post(
            "/douyin/search/user",
            summary=_("用户搜索"),
            description=_("获取用户搜索数据"),
            tags=[_("抖音")],
            response_model=Response,
        )
        async def handle_user(
            extract: UserSearch, token: str = Depends(token_dependency)
        ):
            return await self.handle_search(extract)

        @self.server.post(
            "/douyin/search/live",
            summary=_("直播搜索"),
            description=_("获取直播搜索数据"),
            tags=[_("抖音")],
            response_model=Response,
        )
        async def handle_live(
            extract: LiveSearch, token: str = Depends(token_dependency)
        ):
            return await self.handle_search(extract)

    async def handle_search(self, extract):
        if data := await self.deal_search_data(
            extract,
            extract.source,
        ):
            return Response(
                message=_("获取成功！"),
                data=data,
                params=extract.model_dump(),
            )
        return Response(
            message=_("获取失败！"),
            data=data,
            params=extract.model_dump(),
        )
