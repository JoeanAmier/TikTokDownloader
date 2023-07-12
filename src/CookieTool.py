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
        get_key = {
            "passport_csrf_token": None,
            "odin_tt": None,
            "sessionid_ss": None}
        for i in cookie.split('; '):
            text = i.split("=", 1)
            if (k := text[0]) in get_key:
                get_key[k] = text[1]
        if all(
                value for key,
                value in get_key.items() if key in (
                        'passport_csrf_token',
                        'odin_tt')):
            self.get_login_token(get_key)
            self.write(get_key, index)
            print("写入 Cookie 成功！")
        else:
            print("Cookie 缺少必需的键值对！")

    @staticmethod
    def get_login_token(items):
        if not items["sessionid_ss"]:
            del items["sessionid_ss"]
            print("当前 Cookie 未登录")
        else:
            print("当前 Cookie 已登录")

    def write(self, text, index):
        data = self.settings.read()
        while len(data["cookie"]) < index + 1:
            data["cookie"].append({})
        data["cookie"][index] = text
        self.settings.update(data)
