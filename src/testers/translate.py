from src.translation import _, switch_language
from src.custom import DISCLAIMER_TEXT

if __name__ == "__main__":
    print(_(DISCLAIMER_TEXT))

    # 切换到英文并打印翻译
    switch_language("en_US")
    print(_(DISCLAIMER_TEXT))

    # 切换回中文并打印翻译
    switch_language("zh_CN")
    print(_(DISCLAIMER_TEXT))
