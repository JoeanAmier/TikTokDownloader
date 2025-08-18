from typing import List

from pydantic import BaseModel, Field


class AccountUrl(BaseModel):
    mark: str = ""
    url: str
    tab: str = "post"
    earliest: str | int | float = ""
    latest: str | int | float = ""
    enable: bool = True


class MixUrl(BaseModel):
    mark: str = ""
    url: str
    enable: bool = True


class OwnerUrl(BaseModel):
    mark: str = ""
    url: str
    uid: str = ""
    sec_uid: str = ""
    nickname: str = ""


class BrowserInfo(BaseModel):
    User_Agent: str = Field(
        default="",
        alias="User-Agent",
    )
    pc_libra_divert: str = ""
    browser_language: str = ""
    browser_platform: str = ""
    browser_name: str = ""
    browser_version: str = ""
    engine_name: str = ""
    engine_version: str = ""
    os_name: str = ""
    os_version: str = ""
    webid: str = ""


class TikTokBrowserInfo(BaseModel):
    User_Agent: str = Field(
        "",
        alias="User-Agent",
    )
    app_language: str = ""
    browser_language: str = ""
    browser_name: str = ""
    browser_platform: str = ""
    browser_version: str = ""
    language: str = ""
    os: str = ""
    priority_region: str = ""
    region: str = ""
    tz_name: str = ""
    webcast_language: str = ""
    device_id: str = ""


class Settings(BaseModel):
    accounts_urls: List[AccountUrl] = []
    accounts_urls_tiktok: List[AccountUrl] = []
    mix_urls: List[MixUrl] = []
    mix_urls_tiktok: List[MixUrl] = []
    owner_url: OwnerUrl | dict[str, str] = {}
    owner_url_tiktok: None = None
    root: str | None = None
    folder_name: str | None = None
    name_format: str | None = None
    desc_length: int | None = None
    name_length: int | None = None
    date_format: str | None = None
    split: str | None = None
    folder_mode: bool | None = None
    music: bool | None = None
    truncate: int | None = None
    storage_format: str | None = None
    cookie: str | dict = ""
    cookie_tiktok: str | dict = ""
    dynamic_cover: bool | None = None
    static_cover: bool | None = None
    proxy: str | None = None
    proxy_tiktok: str | None = None
    twc_tiktok: str | None = None
    download: bool | None = None
    max_size: int | None = None
    chunk: int | None = None
    timeout: int | None = None
    max_retry: int | None = None
    max_pages: int | None = None
    run_command: str | None = None
    ffmpeg: str | None = None
    live_qualities: str | None = None
    douyin_platform: bool | None = None
    tiktok_platform: bool | None = None
    browser_info: BrowserInfo | None = None
    browser_info_tiktok: TikTokBrowserInfo | None = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            AccountUrl: lambda v: v.dict(),
            MixUrl: lambda v: v.dict(),
            OwnerUrl: lambda v: v.dict(),
            BrowserInfo: lambda v: v.dict(),
            TikTokBrowserInfo: lambda v: v.dict(),
        }
