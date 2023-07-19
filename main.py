from atexit import register
from functools import partial

from flask import Flask

from src.CookieTool import Cookie
from src.main_complete import TikTok
from src.main_complete import prompt
from src.main_server import Server
from src.main_web_UI import WebUI

VERSION = "3.3 beta"


def version():
    project = f"TikTokDownloader v{VERSION}"
    width = 33
    line = ">" * width
    print(f"{line}\n\n{project.center(width)}\n\n{line}\n")


def main():
    """选择运行模式"""
    mode = prompt(
        "请选择 TikTokDownloader 运行模式",
        ("写入 Cookie 信息", "单线程终端模式", "多进程终端模式", ''"Web UI 交互模式", "服务器部署模式"), 0)
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
    main()
