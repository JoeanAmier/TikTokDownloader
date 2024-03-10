from json import dump
from json import load
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import TYPE_CHECKING

from src.custom import (
    ERROR,
)
from src.tools import PrivateRetry

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["Cache"]


class Cache:
    encode = "UTF-8"

    def __init__(
            self,
            parameter: "Parameter",
            mark: bool,
            name: bool):
        self.console = parameter.console
        self.log = parameter.logger  # 日志记录对象
        self.file = parameter.main_path.joinpath(
            "./cache/AccountCache.json")  # 缓存数据文件
        self.root = parameter.root  # 作品文件保存根目录
        self.mark = mark
        self.name = name
        self.data = self.__read_cache()

    def __read_cache(self):
        try:
            if self.file.exists():
                with self.file.open("r", encoding=self.encode) as f:
                    cache = load(f)
                    self.log.info("读取缓存数据成功\n")
                    return cache
            else:
                self.log.info("缓存数据文件不存在\n")
                return {}
        except JSONDecodeError:
            self.log.warning("缓存数据文件已损坏\n")
            return {}

    def __save_cache(self):
        with self.file.open("w", encoding=self.encode) as f:
            dump(self.data, f, indent=4, ensure_ascii=False)
        self.log.info("缓存数据已保存至文件")

    def update_cache(
            self,
            solo_mode: bool,
            type_: str,
            id_: str,
            mark: str,
            name: str,
            addition: str, ):
        if self.data.get(id_):
            self.__check_file(solo_mode, type_, id_, mark, name, addition)
        self.data[id_] = {"mark": mark, "name": name}
        self.log.info(f"更新缓存数据: {id_, mark, name}", False)
        self.__save_cache()

    def __check_file(
            self,
            solo_mode: bool,
            type_: str,
            id_: str,
            mark: str,
            name: str,
            addition: str):
        if not (
                old_folder := self.root.joinpath(
                    f"{type_}{id_}_{
                    self.data[id_]["mark"] or self.data[id_]["name"]}_{addition}")).is_dir():
            self.log.info(f"{old_folder} 文件夹不存在，自动跳过", False)
            return
        if self.data[id_]["mark"] != mark:
            self.__rename_folder(old_folder, type_, id_, mark, addition)
            if self.mark:
                self.__scan_file(
                    solo_mode, type_, id_, mark, name, addition, field="mark")
        if self.data[id_]["name"] != name and self.name:
            self.__scan_file(solo_mode, type_, id_, mark, name, addition)

    def __rename_folder(
            self,
            old_folder,
            type_: str,
            id_: str,
            mark: str,
            addition: str):
        new_folder = self.root.joinpath(f"{type_}{id_}_{mark}_{addition}")
        self.__rename(old_folder, new_folder, "文件夹")
        self.log.info(f"文件夹 {old_folder} 已重命名为 {new_folder}", False)

    def __rename_works_folder(self,
                              old_: Path,
                              id_: str,
                              mark: str,
                              name: str,
                              field: str) -> Path:
        if (s := self.data[id_][field]) in old_.name:
            new_ = old_.parent / old_.name.replace(
                s, {"name": name, "mark": mark}[field], 1)
            self.__rename(old_, new_)
            self.log.info(f"文件夹 {old_} 重命名为 {new_}", False)
            return new_
        return old_

    def __scan_file(
            self,
            solo_mode: bool,
            type_: str,
            id_: str,
            mark: str,
            name: str,
            addition: str,
            field="name", ):
        root = self.root.joinpath(f"{type_}{id_}_{mark}_{addition}")
        item_list = root.iterdir()
        if solo_mode:
            for f in item_list:
                if f.is_dir():
                    f = self.__rename_works_folder(f, id_, mark, name, field)
                    files = f.iterdir()
                    self.__batch_rename(f, files, id_, mark, name, field)
        else:
            self.__batch_rename(root, item_list, id_, mark, name, field)

    def __batch_rename(
            self,
            root: Path,
            files,
            id_: str,
            mark: str,
            name: str,
            field: str):
        for old_file in files:
            if (s := self.data[id_][field]) not in old_file.name:
                break
            self.__rename_file(root, old_file, s, mark, name, field)

    def __rename_file(
            self,
            root: Path,
            old_file: Path,
            key_words: str,
            mark: str,
            name: str,
            field: str):
        new_file = root.joinpath(old_file.name.replace(
            key_words, {"name": name, "mark": mark}[field], 1))
        self.__rename(old_file, new_file)
        self.log.info(f"文件 {old_file} 重命名为 {new_file}", False)
        return True

    @PrivateRetry.retry_limited
    def __rename(self, old_: Path, new_: Path, type_="文件") -> bool:
        try:
            old_.rename(new_)
            return True
        except PermissionError as e:
            self.console.print(f"{type_}被占用，重命名失败: {e}", style=ERROR)
            return False
        except FileExistsError as e:
            self.console.print(f"{type_}名称重复，重命名失败: {e}", style=ERROR)
            return False
        except OSError as e:
            self.console.print(f"处理{type_}时发生预期之外的错误: {e}", style=ERROR)
            return True
