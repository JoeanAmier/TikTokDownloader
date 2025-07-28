from pathlib import Path

from src.config import Settings
from src.custom import PROJECT_ROOT
from src.tools import ColorfulConsole
from src.translation import _
from src.custom import VERSION_BETA


class Write:
    def __init__(
        self,
    ):
        self.console = ColorfulConsole(
            debug=VERSION_BETA,
        )
        self.settings = Settings(PROJECT_ROOT, self.console)
        self.data = self.settings.read()

    def run(self):
        data = self.txt_inquire()
        self.generate_data(data)
        self.settings.update(self.data)

    def generate_data(self, data: str):
        for i in data.split("\n"):
            if i.strip():
                self.data["accounts_urls_tiktok"].append(
                    {
                        "mark": "",
                        "url": i,
                        "tab": "post",
                        "earliest": "",
                        "latest": "",
                        "enable": True,
                    }
                )

    def txt_inquire(self) -> str:
        if path := self.console.input(_("请输入文本文档路径：")):
            if (t := Path(path.replace('"', ""))).is_file():
                try:
                    with t.open("r", encoding=self.settings.encode) as f:
                        return f.read()
                except UnicodeEncodeError as e:
                    self.console.warning(
                        _("{path} 文件读取异常: {error}").format(path=path, error=e)
                    )
            else:
                self.console.print(_("{path} 文件不存在！").format(path=path))
        return ""


if __name__ == "__main__":
    Write().run()
