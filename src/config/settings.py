from json import dump, load
from json.decoder import JSONDecodeError
from platform import system
from shutil import move
from types import SimpleNamespace
from typing import TYPE_CHECKING

from ..translation import _

if TYPE_CHECKING:
    from pathlib import Path

    from ..tools import ColorfulConsole

__all__ = ["Settings"]


class Settings:
    encode = "UTF-8-SIG" if system() == "Windows" else "UTF-8"
    default = {
        "accounts_urls": [
            {
                "mark": "",
                "url": "",
                "tab": "",
                "earliest": "",
                "latest": "",
                "enable": True,
            },
        ],
        "accounts_urls_tiktok": [
            {
                "mark": "",
                "url": "",
                "tab": "",
                "earliest": "",
                "latest": "",
                "enable": True,
            },
        ],
        "mix_urls": [
            {
                "mark": "",
                "url": "",
                "enable": True,
            },
        ],
        "mix_urls_tiktok": [
            {
                "mark": "",
                "url": "",
                "enable": True,
            },
        ],
        "owner_url": {
            "mark": "",
            "url": "",
            "uid": "",
            "sec_uid": "",
            "nickname": "",
        },
        "owner_url_tiktok": None,
        "root": "",
        "folder_name": "Download",
        "name_format": "create_time type nickname desc",
        "date_format": "%Y-%m-%d %H:%M:%S",
        "split": "-",
        "folder_mode": False,
        "music": False,
        "truncate": 50,
        "storage_format": "",
        "cookie": "",
        "cookie_tiktok": "",
        "dynamic_cover": False,
        "static_cover": False,
        "proxy": "",
        "proxy_tiktok": "",
        "twc_tiktok": "",
        "download": True,
        "max_size": 0,
        "chunk": 1024 * 1024 * 2,  # 每次从服务器接收的数据块大小
        "timeout": 10,
        "max_retry": 5,  # 重试最大次数
        "max_pages": 0,
        "run_command": "",
        "ffmpeg": "",
        "live_qualities": "",
        "douyin_platform": True,
        "tiktok_platform": True,
        "browser_info": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "pc_libra_divert": "Windows",
            "browser_platform": "Win32",
            "browser_name": "Chrome",
            "browser_version": "136.0.0.0",
            "engine_name": "Blink",
            "engine_version": "136.0.0.0",
            "os_name": "Windows",
            "os_version": "10",
            "webid": "",
        },
        "browser_info_tiktok": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "app_language": "zh-Hans",
            "browser_language": "zh-SG",
            "browser_name": "Mozilla",
            "browser_platform": "Win32",
            "browser_version": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "language": "zh-Hans",
            "os": "windows",
            "priority_region": "CN",
            "region": "US",
            "tz_name": "Asia/Shanghai",
            "webcast_language": "zh-Hans",
            "device_id": "",
        },
    }  # 默认配置
    rename_params = (
        (
            "default_mode",
            "run_command",
            "",
        ),
        (
            "update_cookie",
            "douyin_platform",
            True,
        ),
        (
            "update_cookie_tiktok",
            "tiktok_platform",
            True,
        ),
        (
            "original_cover",
            "static_cover",
            False,
        ),
    )  # 兼容旧版本配置文件

    def __init__(self, root: "Path", console: "ColorfulConsole"):
        self.root = root
        self.file = "settings.json"
        self.path = root.joinpath(self.file)  # 配置文件
        self.console = console

    def __create(self) -> dict:
        """创建默认配置文件"""
        with self.path.open("w", encoding=self.encode) as f:
            dump(self.default, f, indent=4, ensure_ascii=False)
        self.console.info(
            _(
                "创建默认配置文件 settings.json 成功！\n"
                "请参考项目文档的快速入门部分，设置 Cookie 后重新运行程序！\n"
                "建议根据实际使用需求修改配置文件 settings.json！\n"
            ),
        )
        return self.default

    def read(self) -> dict:
        """读取配置文件，如果没有配置文件，则生成配置文件"""
        self.compatible()
        try:
            if self.path.exists():
                with self.path.open("r", encoding=self.encode) as f:
                    return self.__check(load(f))
            return self.__create()  # 生成的默认配置文件必须设置 cookie 才可以正常运行
        except JSONDecodeError:
            self.console.error(
                _("配置文件 settings.json 格式错误，请检查 JSON 格式！"),
            )
            return self.default  # 读取配置文件发生错误时返回空配置

    def __check(self, data: dict) -> dict:
        data = self.__compatible_with_old_settings(data)
        update = False
        for i, j in self.default.items():
            if i not in data:
                data[i] = j
                update = True
                self.console.info(
                    _("配置文件 settings.json 缺少参数 {i}，已自动添加该参数！").format(
                        i=i
                    ),
                )
        if update:
            self.update(data)
        return data

    def update(self, settings: dict | SimpleNamespace):
        """更新配置文件"""
        with self.path.open("w", encoding=self.encode) as f:
            dump(
                settings if isinstance(settings, dict) else vars(settings),
                f,
                indent=4,
                ensure_ascii=False,
            )
        self.console.info(
            _("保存配置成功！"),
        )

    def __compatible_with_old_settings(
        self,
        data: dict,
    ) -> dict:
        """兼容旧版本配置文件"""
        for old, new_, default in self.rename_params:
            if old in data:
                self.console.info(
                    _(
                        "配置文件 {old} 参数已变更为 {new} 参数，请注意修改配置文件！"
                    ).format(old=old, new=new_),
                )
                data[new_] = data.get(
                    new_,
                    data.get(
                        old,
                        default,
                    ),
                )
        return data

    def compatible(self):
        if (
            old := self.root.parent.joinpath(self.file)
        ).exists() and not self.path.exists():
            move(old, self.path)
