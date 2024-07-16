# 本程序仅用于 5.3 更新至 5.4
# 已完成：更新配置文件参数
# 待完成：迁移旧版下载记录


from json import dump
from json import load
from platform import system

from src.config import Settings
from src.custom import PROJECT_ROOT

SETTING_ROOT = PROJECT_ROOT.joinpath("settings.json")
ENCODE = "UTF-8-SIG" if system() == "Windows" else "UTF-8"


def about():
    print("Chương trình này chỉ dành cho việc cập nhật từ 5.3 lên 5.4!") #本程序仅用于 5.3 更新至 5.4！
    print("Hãy đảm bảo rằng chương trình này được đặt trong cùng thư mục cấp độ với main.py hoặc main.exe!") #请确保本程序放置于 main.py 或 main.exe 同级文件夹！


def update_params():
    with SETTING_ROOT.open("r+", encoding=ENCODE) as f:
        old_data = load(f)
    with SETTING_ROOT.open("w", encoding=ENCODE) as f:
        new_data = Settings.default | old_data
        dump(new_data, f, indent=4, ensure_ascii=False)
    print("Đã cập nhật tập tin cấu hình!")


def main():
    about()
    if not input("File cấu hình sắp được cập nhật. Chỉ cần nhấn Enter để tiếp tục thực hiện."): #即将更新配置文件，直接回车继续执行，输入任意内容跳过执行：
        update_params()


if __name__ == '__main__':
    main()
