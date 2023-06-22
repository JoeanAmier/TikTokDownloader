from flask import Flask

from src.main_complete import TikTok
from src.main_web_UI import webui


def main():
    try:
        mode = int(input(
            "请输入 TikTokDownloader 运行模式: \n1. 单线程终端模式: 支持所有功能\n2. 多进程终端模式: 仅支持多账号批量下载功能\n3. Web UI 交互模式: 不支持直播下载功能\n"))
    except ValueError:
        return
    match mode:
        case 1:
            example = TikTok()
            example.run()
        case 2:
            pass
        case 3:
            webui(Flask(__name__)).run(host=None, debug=True)


if __name__ == '__main__':
    main()
