from flask import Flask

from src.CookieTool import Cookie
from src.main_complete import TikTok
from src.main_web_UI import WebUI

VERSION = "2.4"


def version():
    project = f"TikTokDownloader v{VERSION}"
    width = 33
    line = ">" * width
    print(f"{line}\n\n{project.center(width)}\n\n{line}\n")


def main():
    compatible(3)


def complete():
    """单线程终端模式"""
    example = TikTok()
    example.run()


def multiprocess():
    """多进程终端模式"""
    pass


def web_ui():
    """
    Web UI 交互模式
    设置host=0.0.0.0可以启用局域网访问
    但是本项目暂时不支持直接部署至公开服务器
    """
    app = WebUI().webui_run(Flask(__name__))
    app.run(host=None, debug=False)


def compatible(mode: int):
    if mode == 0:
        Cookie().run()
    elif mode == 1:
        complete()
    elif mode == 2:
        multiprocess()
    elif mode == 3:
        web_ui()


if __name__ == '__main__':
    version()
    main()
