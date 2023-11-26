from json import dump
from json import load
from json.decoder import JSONDecodeError
from pathlib import Path

from rich import print

from src.Customizer import (
    ERROR,
    WARNING,
    INFO,
)

__all__ = ['Cache', 'FileManager', 'DownloadRecorder']


def retry(function):
    def inner(self, *args, **kwargs):
        while True:
            if function(self, *args, **kwargs):
                return
            _ = self.console.input(
                "请关闭所有正在访问作品保存文件夹的窗口和程序，按下回车继续运行！")

    return inner


class Cache:
    def __init__(
            self,
            parameter,
            mark: bool,
            name: bool):
        self.console = parameter.console
        self.log = parameter.logger  # 日志记录对象
        self.file = parameter.main_path.joinpath(
            "./cache/AccountCache.json")  # 缓存数据文件
        self.root = parameter.root  # 作品文件保存根目录
        self.mark = mark
        self.name = name
        self.data = self.read_cache()

    def read_cache(self):
        try:
            if self.file.exists():
                with self.file.open("r", encoding="UTF-8") as f:
                    cache = load(f)
                    self.log.info("读取缓存数据成功\n")
                    return cache
            else:
                self.log.info("缓存数据文件不存在\n")
                return {}
        except JSONDecodeError:
            self.log.warning("缓存数据文件已损坏\n")
            return {}

    def save_cache(self):
        with self.file.open("w", encoding="UTF-8") as f:
            dump(self.data, f, indent=4)
        self.log.info("缓存数据已保存至文件")

    def update_cache(
            self,
            solo_mode: bool,
            type_: str,
            id_: str,
            mark: str,
            name: str):
        if self.data.get(id_):
            self.check_file(solo_mode, type_, id_, mark, name)
        self.data[id_] = {"mark": mark, "name": name}
        self.log.info(f"更新缓存数据: {id_, mark, name}", False)
        self.save_cache()

    def check_file(
            self,
            solo_mode: bool,
            type_: str,
            id_: str,
            mark: str,
            name: str):
        for i in ("喜欢作品", "收藏作品", "发布作品", "合集作品"):
            if not (
                    old_folder := self.root.joinpath(
                        f"{type_}{id_}_{
                        self.data[id_]["mark"] or self.data[id_]["name"]}_{i}")).is_dir():
                self.log.info(f"{old_folder} 文件夹不存在，自动跳过", False)
                continue
            if self.data[id_]["mark"] != mark:
                self.rename_folder(old_folder, type_, id_, mark)
                if self.mark:
                    self.scan_file(
                        solo_mode, type_, id_, mark, name, field="mark")
            if self.data[id_]["name"] != name and self.name:
                self.scan_file(solo_mode, type_, id_, mark, name)

    def rename_folder(self, old_folder, type_: str, id_: str, mark: str):
        new_folder = self.root.joinpath(f"{type_}{id_}_{mark}")
        self.rename(old_folder, new_folder, "文件夹")
        self.log.info(f"文件夹 {old_folder} 已重命名为 {new_folder}", False)
        return True

    def scan_file(
            self,
            solo_mode: bool,
            type_: str,
            id_: str,
            mark: str,
            name: str,
            field="name"):
        root = self.root.joinpath(f"{type_}{id_}_{mark}")
        item_list = root.iterdir()
        if solo_mode:
            for f in item_list:
                if f.isdir():
                    files = f.iterdir()
                    self.batch_rename(f, files, id_, mark, name, field)
        else:
            self.batch_rename(root, item_list, id_, mark, name, field)

    def batch_rename(
            self,
            root: Path,
            files: tuple,
            id_: str,
            mark: str,
            name: str,
            field: str):
        for old_file in files:
            if (s := self.data[id_][field]) not in old_file.name:
                break
            self.rename_file(root, old_file, s, mark, name, field)

    def rename_file(
            self,
            root: Path,
            old_file: Path,
            key_words: str,
            mark: str,
            name: str,
            field: str):
        new_file = root.joinpath(old_file.name.replace(
            key_words, {"name": name, "mark": mark}[field], 1))
        self.rename(old_file, new_file)
        self.log.info(f"文件 {old_file} 重命名为 {new_file}", False)
        return True

    @retry
    def rename(self, old_: Path, new_: Path, type_="文件") -> bool:
        try:
            old_.rename(new_)
            return True
        except PermissionError as e:
            self.console.print(f"{type_}被占用，重命名失败: {e}", style=ERROR)
            return False
        except FileExistsError as e:
            self.console.print(f"{type_}名称重复，重命名失败: {e}", style=ERROR)
            return False


class FileManager:
    @staticmethod
    def deal_config(path: Path):
        if path.exists():
            path.unlink()
        else:
            path.touch()


class DownloadRecorder:
    def __init__(self, switch, folder: Path):
        self.switch = switch
        self.backup = folder.joinpath("IDRecorder_backup.txt")
        self.path = folder.joinpath("IDRecorder.txt")
        self.file = None
        self.record = self.__get_set()

    def __get_set(self) -> set:
        return self.__read_file() if self.switch else set()

    def __read_file(self):
        if not self.path.is_file():
            blacklist = set()
        else:
            with self.path.open("r", encoding="utf-8") as f:
                blacklist = self.__restore_data({line.strip() for line in f})
                # blacklist = self.__restore_data({i for i in range(100)})
        self.file = self.path.open("w", encoding="utf-8")
        return blacklist

    def __save_file(self, file):
        file.write("\n".join(f"{i}" for i in self.record))

    def update_id(self, id_):
        self.record.add(id_)

    def backup_file(self):
        if self.file and self.record:
            # print("Backup IDRecorder")
            with self.backup.open("w", encoding="utf-8") as f:
                self.__save_file(f)

    def close(self):
        if self.file:
            self.__save_file(self.file)
            self.file.close()
            self.file = None
            # print("Close IDRecorder")

    def __restore_data(self, ids: set) -> set:
        if ids:
            return ids
        print(f"[{ERROR}]{self.path.resolve()
        } 数据为空，可能是程序上次运行异常退出导致数据丢失！[/{ERROR}]")
        if self.backup.exists():
            print(
                f"[{WARNING}]检测到 IDRecorder 备份文件，是否恢复最后一次备份的数据(YES/NO): [/{WARNING}]", end="")
            if input().upper() == "YES":
                self.path.write_text(self.backup.read_text())
                print(f"[{INFO}]IDRecorder 已恢复最后一次备份的数据，请重新运行程序！[/{INFO}]")
                return set(self.backup.read_text().split())
            else:
                print(
                    f"[{ERROR}]IDRecorder 数据未恢复，下载任意作品之后，备份数据会被覆盖导致无法恢复！[/{ERROR}]")
        else:
            print(f"[{ERROR}]未检测到 IDRecorder 备份文件，您的作品下载记录数据无法恢复！[/{ERROR}]")
        return set()
