from atexit import register
from functools import partial
from pathlib import Path
from urllib.parse import urlparse

from flask import Flask
from requests import exceptions
from requests import get

from src.CookieTool import Cookie
from src.main_complete import TikTok
from src.main_complete import prompt
from src.main_server import Server
from src.main_web_UI import WebUI

VERSION = 3.3
STABLE = False

RELEASES = "https://github.com/JoeanAmier/TikTokDownloader/releases/latest"
PROJECT = f"TikTokDownloader v{VERSION}{'' if STABLE else ' Beta'}"
WIDTH = 50
LINE = ">" * WIDTH


def version():
    print(f"{LINE}\n\n\n{PROJECT.center(WIDTH)}\n\n\n{LINE}\n")


def check_update():
    if Path("./src/Disable_Update.txt").exists():
        return
    print("正在检测新版本", end="", flush=True)
    try:
        response = get(RELEASES, timeout=10)
        tag = float(urlparse(response.url).path.split("/")[-1])
        if tag > VERSION:
            print(f"\r检测到新版本: {tag}", flush=True)
            print(response.url)
        else:
            print("\r当前已是最新版本", flush=True)
    except (exceptions.ReadTimeout, exceptions.ConnectionError):
        print("\r检测新版本失败", flush=True)
    print("")


def main():
    """选择运行模式"""
    mode = prompt(
        "请选择 TikTokDownloader 运行模式",
        ("写入 Cookie 信息", "单进程终端模式", "多进程终端模式", "Web UI 交互模式", "服务器部署模式"), 0)
    compatible(mode)


def complete():
    """单线程终端模式"""
    example = TikTok()
    example.run()


def multiprocess():
    """多进程终端模式"""
    print("敬请期待！")


def web_ui():
    """
    Web UI 交互模式
    """
    master = WebUI()
    app = master.webui_run(Flask(__name__))
    close_file_handler = partial(close_file, [master.xb.file])
    register(close_file_handler)
    app.run(host="0.0.0.0", debug=False)


def server():
    """
    服务器部署模式
    """
    master = Server()
    app = master.server_run(Flask(__name__))
    close_file_handler = partial(close_file, [master.xb.file])
    register(close_file_handler)
    app.run(host="0.0.0.0", debug=False)


def close_file(files: list | tuple):
    for f in files:
        f.close()


def compatible(mode: str):
    if mode == "0":
        Cookie().run()
    elif mode == "1":
        complete()
    elif mode == "2":
        multiprocess()
    elif mode == "3":
        web_ui()
    elif mode == "4":
        server()


if __name__ == '__main__':
    version()
    check_update()
    main()
