from pydantic import BaseModel, Field
from typing import Optional, List


class AccountUrl(BaseModel):
    mark: str = ""
    url: str = ""
    tab: str = "post"
    earliest: str | int | float = ""
    latest: str | int | float = ""
    enable: bool = True


class MixUrl(BaseModel):
    mark: str = ""
    url: str = ""
    enable: bool = True


class OwnerUrl(BaseModel):
    mark: str = ""
    url: str = ""
    uid: str = ""
    sec_uid: str = ""
    nickname: str = ""


class BrowserInfo(BaseModel):
    User_Agent: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        alias="User-Agent",
    )
    pc_libra_divert: str = "Windows"
    browser_platform: str = "Win32"
    browser_name: str = "Chrome"
    browser_version: str = "126.0.0.0"
    engine_name: str = "Blink"
    engine_version: str = "126.0.0.0"
    os_name: str = "Windows"
    os_version: str = "10"
    webid: str = ""


class TikTokBrowserInfo(BaseModel):
    User_Agent: str = Field(
        "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        alias="User-Agent",
    )
    app_language: str = "zh-Hans"
    browser_language: str = "zh-SG"
    browser_name: str = "Mozilla"
    browser_platform: str = "Win32"
    browser_version: str = "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    language: str = "zh-Hans"
    os: str = "windows"
    priority_region: str = "CN"
    region: str = "US"
    tz_name: str = "Asia/Shanghai"
    webcast_language: str = "zh-Hans"
    device_id: str = ""


class Settings(BaseModel):
    accounts_urls: List[AccountUrl] = [AccountUrl()]
    accounts_urls_tiktok: List[AccountUrl] = [AccountUrl()]
    mix_urls: List[MixUrl] = [MixUrl()]
    mix_urls_tiktok: List[MixUrl] = [MixUrl()]
    owner_url: OwnerUrl = OwnerUrl()
    owner_url_tiktok: OwnerUrl | None = None
    root: str = ""
    folder_name: str = "Download"
    name_format: str = "create_time type nickname desc"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    split: str = "-"
    folder_mode: bool = False
    music: bool = False
    truncate: int = 50
    storage_format: str = ""
    cookie: str | dict = ""
    cookie_tiktok: str | dict = ""
    dynamic_cover: bool = False
    static_cover: bool = False
    proxy: Optional[str] = None
    proxy_tiktok: Optional[str] = None
    twc_tiktok: str = ""
    download: bool = True
    max_size: int = 0
    chunk: int = 1024 * 1024 * 2
    timeout: int = 10
    max_retry: int = 5
    max_pages: int = 0
    run_command: str = ""
    ffmpeg: str = ""
    # douyin_platform: bool = True
    # tiktok_platform: bool = True
    browser_info: BrowserInfo = BrowserInfo()
    browser_info_tiktok: TikTokBrowserInfo = TikTokBrowserInfo()

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
