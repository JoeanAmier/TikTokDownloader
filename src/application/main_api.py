from typing import TYPE_CHECKING

from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.responses import RedirectResponse
from uvicorn import Config
from uvicorn import Server

from .main_complete import TikTok
from ..custom import (
    SERVER_HOST,
    SERVER_PORT,
    VERSION_BETA,
    REPOSITORY,
    __VERSION__,
    is_valid_token,
)
from ..models import (
    GeneralSearch,
    Response,
)
from ..translation import _

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
        @self.server.get("/")
        async def index():
            return RedirectResponse(url=REPOSITORY)

        @self.server.post(
            "/search/general",
            response_model=Response,
        )
        async def handle(
                extract: GeneralSearch, token: str = Depends(token_dependency)
        ):
            if data := await self.deal_search_data(
                    extract,
                    extract.source,
            ):
                return Response(
                    message=_("获取成功！"),
                    data=data,
                )
            return Response(
                message=_("获取失败！"),
                data=data,
            )
