import json
import os


def retry(function):
    def inner(self, *args, **kwargs):
        while True:
            if function(self, *args, **kwargs):
                return
            _ = input("请关闭所有正在访问作品保存文件夹的窗口和程序，按下回车继续运行")

    return inner


class Cache:
    def __init__(self, record, root: str, type_: str):
        self.log = record  # 日志记录对象
        self.file = "./src/FileCache.json"  # 缓存文件
        self.root = root  # 作品文件保存根目录
        self.type_ = type_
        self.cache = self.read_cache()

    def read_cache(self):
        try:
            if os.path.exists(self.file):
                with open(self.file, "r", encoding="UTF-8") as f:
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
        with open(self.file, "w", encoding="UTF-8") as f:
            json.dump(self.cache, f)

    def update_cache(self, uid: str, mark: str, name: str):
        if self.cache.get(uid):
            self.check_file(uid, mark, name)
        self.cache[uid] = {"mark": mark, "name": name}
        self.log.info(f"更新缓存: {uid, mark, name}", False)

    def check_file(self, uid: str, mark: str, name: str):
        if not os.path.exists(
                old_folder := os.path.join(
                    self.root,
                    f"{self.type_}{uid}_{self.cache[uid]['mark']}")):
            self.log.info(f"{old_folder} 不存在，自动跳过")
            return
        if self.cache[uid]["mark"] != mark:
            self.rename_folder(old_folder, uid, mark)
        if self.cache[uid]["name"] != name:
            self.rename_file(uid, mark, name)

    @retry
    def rename_folder(self, old_folder, uid: str, mark: str):
        new_folder = os.path.join(self.root, f"{self.type_}{uid}_{mark}")
        try:
            os.rename(old_folder, new_folder)
        except PermissionError as e:
            self.log.warning(f"文件夹被占用，重命名失败: {e}")
            return False
        self.log.info(f"文件夹 {old_folder} 重命名为 {new_folder}")
        return True

    def rename_file(self, uid, mark, name):
        def rename(type_: str):
            nonlocal folder, uid, mark, name
            deal_folder = os.path.join(folder, type_)
            file_list = os.listdir(deal_folder)
            for item in file_list:
                if (s := self.cache[uid]["name"]) not in item:
                    break
                old_path = os.path.join(deal_folder, item)
                new_path = os.path.join(deal_folder, item.replace(s, name, 1))
                os.rename(old_path, new_path)
                self.log.info(f"文件 {old_path} 重命名为 {new_path}")
            for item in file_list:
                if (s := self.cache[uid]["mark"]) not in item:
                    break
                old_path = os.path.join(deal_folder, item)
                new_path = os.path.join(deal_folder, item.replace(s, mark, 1))
                os.rename(old_path, new_path)
                self.log.info(f"文件 {old_path} 重命名为 {new_path}")

        folder = os.path.join(self.root, f"{self.type_}{uid}_{mark}")
        rename("video")
        rename("images")
