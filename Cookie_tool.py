from Configuration import Settings


class Cookie:
    def __init__(self):
        self.settings = Settings()

    def run(self):
        """提取 Cookie 并写入配置文件"""
        get_key = ("passport_csrf_token", "odin_tt")
        data = {}
        cookie = input("粘贴 Cookie 后回车：")
        for i in cookie.split('; '):
            text = i.split("=", 1)
            try:
                data[text[0]] = text[1]
            except IndexError:
                continue
        if result := "; ".join(f"{i}={data.get(i, '')}" for i in get_key):
            self.write(result)
            print(f"已写入 Cookie: {result}")
        else:
            print("写入 Cookie 失败！")

    def write(self, text):
        data = self.settings.read()
        data["cookie"] = text
        self.settings.update(data)


if __name__ == '__main__':
    Cookie().run()
