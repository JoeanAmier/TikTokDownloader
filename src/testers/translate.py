from src.tools import switch_language, _

if __name__ == '__main__':
    print(_("免责声明\n"))

    # 切换到英文并打印翻译
    switch_language("en_US")
    print(_("免责声明\n"))

    # 切换回中文并打印翻译
    switch_language("zh_CN")
    print(_("免责声明\n"))
