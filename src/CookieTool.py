from src.Configuration import Settings


class Cookie:
    def __init__(self):
        self.settings = Settings()

    def run(self):
        """提取 Cookie 并写入配置文件"""
        if not (cookie := input("请粘贴 Cookie 内容：")):
            return
        try:
            index = int(input("请输入该 Cookie 的写入位置(索引，默认为0)：") or 0)
        except ValueError:
            print("写入位置错误！")
        else:
            self.extract(cookie, index)

    def extract(self, cookie: str, index: int):
        get_key = {"passport_csrf_token": None, "odin_tt": None, }
        for i in cookie.split('; '):
            text = i.split("=", 1)
            try:
                if (k := text[0]) in get_key:
                    get_key[k] = text[1]
            except IndexError:
                continue
        if None in get_key.values():
            print("Cookie 缺少必需的键值对！")
        else:
            self.write("; ".join(
                [f"{key}={value}" for key, value in get_key.items()]), index)
            print("写入 Cookie 成功！")

    def write(self, text, index):
        data = self.settings.read()
        while len(data["cookie"]) < index + 1:
            data["cookie"].append("")
        data["cookie"][index] = text
        self.settings.update(data)


if __name__ == '__main__':
    Cookie().run()
