from pathlib import Path
from typing import TYPE_CHECKING

from ..tools import Retry
from ..translation import _

if TYPE_CHECKING:
    from ..config import Parameter
    from .database import Database

__all__ = ["Cache"]


class Cache:
    def __init__(
        self,
        parameter: "Parameter",
        database: "Database",
        mark: bool,
        name: bool,
    ):
        self.console = parameter.console
        self.log = parameter.logger  # 日志记录对象
        self.database = database
        self.root = parameter.root  # 作品文件保存根目录
        self.mark = mark
        self.name = name

    async def update_cache(
        self,
        solo_mode: bool,
        prefix: str,
        suffix: str,
        id_: str,
        name: str,
        mark: str,
    ):
        if d := await self.has_cache(id_):
            self.__check_file(
                solo_mode,
                prefix,
                suffix,
                id_,
                name,
                mark,
                d,
            )
        data = (
            id_,
            name,
            mark,
        )
        await self.database.update_mapping_data(*data)
        self.log.info(f"更新缓存数据: {', '.join(data)}", False)

    async def has_cache(self, id_: str) -> dict:
        return await self.database.read_mapping_data(id_)

    def __check_file(
        self,
        solo_mode: bool,
        prefix: str,
        suffix: str,
        id_: str,
        name: str,
        mark: str,
        data: dict,
    ):
        if not (
            old_folder := self.root.joinpath(
                f"{prefix}{id_}_{data['mark'] or data['name']}_{suffix}"
            )
        ).is_dir():
            self.log.info(f"{old_folder} 文件夹不存在，自动跳过", False)
            return
        if data["mark"] != mark:
            self.__rename_folder(old_folder, prefix, suffix, id_, mark)
            if self.mark:
                self.__scan_file(
                    solo_mode,
                    prefix,
                    suffix,
                    id_,
                    name,
                    mark,
                    key="mark",
                    data=data,
                )
        if data["name"] != name and self.name:
            self.__scan_file(
                solo_mode,
                prefix,
                suffix,
                id_,
                name,
                mark,
                data=data,
            )

    def __rename_folder(
        self,
        old_folder: Path,
        prefix: str,
        suffix: str,
        id_: str,
        mark: str,
    ):
        new_folder = self.root.joinpath(f"{prefix}{id_}_{mark}_{suffix}")
        self.__rename(
            old_folder,
            new_folder,
            _("文件夹"),
        )
        self.log.info(f"文件夹 {old_folder} 已重命名为 {new_folder}", False)

    def __rename_works_folder(
        self,
        old_: Path,
        mark: str,
        name: str,
        key: str,
        data: dict,
    ) -> Path:
        if (s := data[key]) in old_.name:
            new_ = old_.parent / old_.name.replace(
                s, {"name": name, "mark": mark}[key], 1
            )
            self.__rename(
                old_,
                new_,
                _("文件夹"),
            )
            self.log.info(f"文件夹 {old_} 重命名为 {new_}", False)
            return new_
        return old_

    def __scan_file(
        self,
        solo_mode: bool,
        prefix: str,
        suffix: str,
        id_: str,
        name: str,
        mark: str,
        data: dict,
        key="name",
    ):
        root = self.root.joinpath(f"{prefix}{id_}_{mark}_{suffix}")
        item_list = root.iterdir()
        if solo_mode:
            for f in item_list:
                if f.is_dir():
                    f = self.__rename_works_folder(
                        f,
                        mark,
                        name,
                        key,
                        data,
                    )
                    files = f.iterdir()
                    self.__batch_rename(
                        f,
                        files,
                        mark,
                        name,
                        key,
                        data,
                    )
        else:
            self.__batch_rename(
                root,
                item_list,
                mark,
                name,
                key,
                data,
            )

    def __batch_rename(
        self,
        root: Path,
        files,
        mark: str,
        name: str,
        key: str,
        data: dict,
    ):
        for old_file in files:
            if (s := data[key]) not in old_file.name:
                break
            self.__rename_file(root, old_file, s, mark, name, key)

    def __rename_file(
        self,
        root: Path,
        old_file: Path,
        keywords: str,
        mark: str,
        name: str,
        field: str,
    ):
        new_file = root.joinpath(
            old_file.name.replace(keywords, {"name": name, "mark": mark}[field], 1)
        )
        self.__rename(
            old_file,
            new_file,
            _("文件"),
        )
        self.log.info(f"文件 {old_file} 重命名为 {new_file}", False)
        return True

    @Retry.retry_limited
    def __rename(
        self,
        old_: Path,
        new_: Path,
        type_=_("文件"),
    ) -> bool:
        try:
            old_.rename(new_)
            return True
        except PermissionError as e:
            self.console.error(
                _("{type} {old}被占用，重命名失败: {error}").format(
                    type=type_, old=old_, error=e
                ),
            )
            return False
        except FileExistsError as e:
            self.console.error(
                _("{type} {new}名称重复，重命名失败: {error}").format(
                    type=type_, new=new_, error=e
                ),
            )
            return False
        except OSError as e:
            self.console.error(
                _("处理{type} {old}时发生预期之外的错误: {error}").format(
                    type=type_, old=old_, error=e
                ),
            )
            return True
