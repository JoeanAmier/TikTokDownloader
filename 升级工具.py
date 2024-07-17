from asyncio import run
from json import dump
from json import load
from platform import system

from src.config import Settings
from src.custom import PROJECT_ROOT
from src.manager import Database

SETTING_ROOT = PROJECT_ROOT.joinpath("settings.json")
ENCODE = "UTF-8-SIG" if system() == "Windows" else "UTF-8"


def about():
    print("本程序仅适用于 TikTokDownloader V5.3 更新至 V5.4！")
    print("请确保本程序放置于 main.py 或 main.exe 同级文件夹！")
    print("本程序功能：")
    print("更新配置文件参数")
    print("迁移旧版映射数据")
    print("迁移旧版下载记录")


def update_params():
    with SETTING_ROOT.open("r+", encoding=ENCODE) as f:
        old_data = load(f)
    with SETTING_ROOT.open("w", encoding=ENCODE) as f:
        new_data = Settings.default | old_data
        dump(new_data, f, indent=4, ensure_ascii=False)
    print("已更新配置文件！")


async def update_map(db):
    with PROJECT_ROOT.joinpath("cache/AccountCache.json").open("r+", encoding="utf-8") as f:
        data = load(f)
    for i, j in data.items():
        await db.update_mapping_data(i, j["name"], j["mark"])
        print("写入映射", i, j["name"], j["mark"])
    print("已更新映射数据！")


async def update_record(db):
    with PROJECT_ROOT.joinpath("cache/IDRecorder.txt").open("r+", encoding="utf-8") as f:
        data = {line.strip() for line in f}
    for i in data:
        await db.write_download_data(i)
        print("写入记录", i)
    print("已更新下载记录！")


async def main():
    about()
    if input("直接回车继续执行，输入任意内容结束运行："):
        return
    if not input("即将更新配置文件，直接回车继续执行，输入任意内容跳过执行："):
        update_params()
    async with Database() as db:
        if not input("即将迁移映射数据，直接回车继续执行，输入任意内容跳过执行："):
            await update_map(db)
        if not input("即将迁移下载记录，直接回车继续执行，输入任意内容跳过执行："):
            await update_record(db)
    print("程序运行完成！")


if __name__ == '__main__':
    run(main())
