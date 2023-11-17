import json
from pathlib import Path

TIP = (
    "本工具使用说明：",
    "本工具仅适用于 TikTokDownloader 5.0 升级至 5.1",
    "本工具需要放置于 settings.json 同级文件夹",
    "本工具会更新您的配置文件，并重命名您已下载的作品文件名称为：发布时间-作品类型-账号昵称-描述",
    "本工具仅需在 TikTokDownloader 5.0 升级至 5.1 后运行一次，切勿多次运行",
    "运行本工具时，请关闭所有正在访问作品保存文件夹（root 参数）和配置文件的窗口和程序",
    "如果您是直接使用 TikTokDownloader 5.1，无需运行该工具，直接回车",
    "如果配置文件 name_format 参数与 date_format 参数未修改，请输入 1 回车，否则输入 0 回车",
    "运行结束请关注程序输出的提示！如有任何问题请联系作者！",
    "请根据实际情况输入内容（输入 0 或 1 开始运行，输入其他字符结束运行）：",
)
ROOT = Path(__file__).resolve().parent


def rename_files_in_directory(directory):
    for item in directory.iterdir():
        item = rename_file(item)
        if item.is_dir():
            rename_files_in_directory(item)


def rename_file(file_path):
    file_name = file_path.name

    # 检查文件名是否以"视频-"或"图集-"开头
    if file_name.startswith("视频-") or file_name.startswith("图集-"):
        prefix, *timestamp, rest = file_name.split('-', 4)

        new_name = f"{'-'.join(timestamp)}-{prefix}-{rest}"
        new_path = file_path.with_name(new_name)

        file_path.rename(new_path)
        print(f"重命名: {file_name} -> {new_name}")
        return new_path
    return file_path


def main():
    if (i := input("\n".join(TIP))) not in {"0", "1"}:
        print("未进行任何操作，您可以重新运行本工具！")
        return
    try:
        with ROOT.joinpath("./settings.json").open("r", encoding="UTF-8") as f:
            settings = json.load(f)
        if i == "1":
            settings["name_format"] = "create_time type nickname desc"
            rename_files_in_directory(Path(r) if (
                r := settings["root"]) else ROOT)
        settings["ffmpeg"] = settings.get("ffmpeg_path", "")
        with ROOT.joinpath("./settings.json").open("w", encoding="UTF-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        print("处理完成，请不要再次运行本工具！")
    except FileNotFoundError:
        print("settings.json 不存在，未进行任何操作，您可以重新运行本工具！")


if __name__ == '__main__':
    main()
