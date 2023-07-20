from atexit import register
from functools import partial
from pathlib import Path

from flask import Flask
from requests import exceptions
from requests import get

from src.CookieTool import Cookie
from src.FileManager import deal_config
from src.StringCleaner import colored_text
from src.main_complete import TikTok
from src.main_complete import prompt
from src.main_server import Server
from src.main_web_UI import WebUI

VERSION = 3.3
STABLE = False

RELEASES = "https://github.com/JoeanAmier/TikTokDownloader/releases/latest"
NAME = f"TikTokDownloader v{VERSION}{'' if STABLE else ' Beta'}"
WIDTH = 50
LINE = ">" * WIDTH

UPDATE = {"path": Path("./src/config/Disable_Update")}
COLOUR = {"path": Path("./src/config/Disable_Colour")}


def version():
    print(
        colored_text(
            f"{LINE}\n\n\n{NAME.center(WIDTH)}\n\n\n{LINE}\n",
            93, bold=1))


def check_config():
    global UPDATE, COLOUR
    UPDATE["tip"] = "启用" if UPDATE["path"].exists() else "禁用"
    COLOUR["tip"] = "启用" if COLOUR["path"].exists() else "禁用"


def check_update():
    if Path("src/config/Disable_Update").exists():
        return
    print(colored_text("正在检测新版本", 92), end="", flush=True)
    try:
        response = get(RELEASES, allow_redirects=False, timeout=0.01)
        tag = float(response.headers['Location'].split("/")[-1])
        if tag > VERSION:
            print(colored_text(f"\r检测到新版本: {tag}", 92), flush=True)
            print(response.url)
        else:
            print(colored_text("\r当前已是最新版本", 92), flush=True)
    except (exceptions.ReadTimeout, exceptions.ConnectionError):
        print(colored_text("\r检测新版本失败", 91), flush=True)
    print()


def main():
    """选择运行模式"""
    mode = prompt(
        "请选择 TikTokDownloader 运行模式",
        ("写入 Cookie 信息", "单进程终端模式", "多进程终端模式", "Web UI 交互模式", "服务器部署模式",
         f"{UPDATE['tip']}检查更新功能", f"{COLOUR['tip']}彩色提示功能",))
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


def change_config(file: Path):
    deal_config(file)
    print("修改设置成功！")
    check_config()
    main()


def compatible(mode: str):
    if mode == "1":
        Cookie().run()
    elif mode == "2":
        complete()
    elif mode == "3":
        multiprocess()
    elif mode == "4":
        web_ui()
    elif mode == "5":
        server()
    elif mode == "6":
        change_config(UPDATE["path"])
    elif mode == "7":
        change_config(COLOUR["path"])


if __name__ == '__main__':
    version()
    check_config()
    check_update()
    main()
