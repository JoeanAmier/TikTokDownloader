import json
from pathlib import Path
from pathlib import PurePath


def retry(function):
    def inner(self, *args, **kwargs):
        while True:
            if function(self, *args, **kwargs):
                return
            _ = input("请关闭所有正在访问作品保存文件夹的窗口和程序，按下回车继续运行")

    return inner


class Cache:
    def __init__(self, record, root: str, type_: str, mark: bool):
        self.log = record  # 日志记录对象
        self.file = Path("./src/FileCache.json")  # 缓存文件
        self.root = Path(root)  # 作品文件保存根目录
        self.type_ = type_
        self.mark = mark
        self.cache = self.read_cache()

    def read_cache(self):
        try:
            if self.file.exists():
                with self.file.open("r", encoding="UTF-8") as f:
                    cache = json.load(f)
                    self.log.info("缓存文件读取成功")
                    return cache
            else:
                self.log.info("缓存文件不存在")
                return {}
        except json.decoder.JSONDecodeError:
            self.log.warning("缓存文件已损坏")
            return {}

    def save_cache(self):
        with self.file.open("w", encoding="UTF-8") as f:
            json.dump(self.cache, f)
        self.log.info("缓存文件已保存")

    def update_cache(self, uid: str, mark: str, name: str):
        if self.cache.get(uid):
            self.check_file(uid, mark, name)
        self.cache[uid] = {"mark": mark, "name": name}
        self.log.info(f"更新缓存: {uid, mark, name}", False)

    def check_file(self, uid: str, mark: str, name: str):
        if not (old_folder := PurePath.joinpath(
                self.root,
                f"{self.type_}{uid}_{self.cache[uid]['mark']}")).is_dir():
            self.log.info(f"{old_folder} 不存在，自动跳过")
            return
        if self.cache[uid]["mark"] != mark:
            self.rename_folder(old_folder, uid, mark)
            if self.mark:
                self.rename_file(uid, mark, name, field="mark")
        if self.cache[uid]["name"] != name:
            self.rename_file(uid, mark, name)

    @retry
    def rename_folder(self, old_folder, uid: str, mark: str):
        new_folder = PurePath.joinpath(self.root, f"{self.type_}{uid}_{mark}")
        try:
            old_folder.rename(new_folder)
        except PermissionError as e:
            self.log.warning(f"文件已被占用，重命名失败: {e}")
            return False
        except FileExistsError as e:
            self.log.warning(f"文件名称重复，重命名失败: {e}")
            return False
        self.log.info(f"文件夹 {old_folder} 重命名为 {new_folder}", False)
        return True

    def rename_file(self, uid, mark, name, field="name"):
        def rename(type_: str):
            nonlocal folder, uid, mark, name, field
            deal_folder = PurePath.joinpath(folder, type_)
            file_list = deal_folder.iterdir()
            for old_file in file_list:
                if (s := self.cache[uid][field]) not in old_file.name:
                    break
                new_file = PurePath.joinpath(deal_folder, old_file.name.replace(
                    s, {"name": name, "mark": mark}[field], 1))
                old_file.rename(new_file)
                self.log.info(f"文件 {old_file} 重命名为 {new_file}", False)

        folder = PurePath.joinpath(self.root, f"{self.type_}{uid}_{mark}")
        rename("video")
        rename("images")
