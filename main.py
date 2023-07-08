from flask import Flask

from src.CookieTool import Cookie
from src.main_complete import TikTok
from src.main_server import Server
from src.main_web_UI import WebUI

VERSION = "3.0"


def version():
    project = f"TikTokDownloader v{VERSION}"
    width = 33
    line = ">" * width
    print(f"{line}\n\n{project.center(width)}\n\n{line}\n")


def main():
    """选择运行模式"""
    try:
        mode = int(
            input(
                "请输入 TikTokDownloader 运行模式: \n0. 写入 Cookie 信息\n1. 单线程终端模式\n2. 多进程终端模式\n3. Web UI 交互模式\n4. 服务器部署模式\n"))
    except ValueError:
        return
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
    app = WebUI().webui_run(Flask(__name__))
    app.run(host="0.0.0.0", debug=False)


def server():
    """
    服务器部署模式
    """
    app = Server().server_run(Flask(__name__))
    app.run(host="0.0.0.0", debug=False)


def compatible(mode: int):
    if mode == 0:
        Cookie().run()
    elif mode == 1:
        complete()
    elif mode == 2:
        multiprocess()
    elif mode == 3:
        web_ui()
    elif mode == 4:
        server()


if __name__ == '__main__':
    version()
    main()
