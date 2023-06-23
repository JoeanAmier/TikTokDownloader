from flask import Flask

from src.main_complete import TikTok
from src.main_web_UI import WebUI


def main():
    try:
        mode = int(
            input("请输入 TikTokDownloader 运行模式: \n1. 单线程终端模式\n2. 多进程终端模式\n3. Web UI 交互模式\n"))
    except ValueError:
        return
    # mode = 3
    match mode:
        case 1:
            example = TikTok()
            example.run()
        case 2:
            pass
        case 3:
            app = WebUI().webui_run(Flask(__name__))
            app.run(host=None, debug=True)


if __name__ == '__main__':
    main()
