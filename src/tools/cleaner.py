from platform import system
from re import compile
from string import whitespace

from emoji import replace_emoji

try:
    from ..translation import _
except ImportError:
    _ = lambda x: x

__all__ = ["Cleaner"]


class Cleaner:
    CONTROL_CHARACTERS = compile(r"[\x00-\x1F\x7F]")

    def __init__(self):
        """
        替换字符串中包含的非法字符，默认根据系统类型生成对应的非法字符字典，也可以自行设置非法字符字典
        """
        self.rule = self.default_rule()  # 默认非法字符字典

    @staticmethod
    def default_rule():
        """根据系统类型生成默认非法字符字典"""
        if (s := system()) in ("Windows", "Darwin"):
            rule = {
                "/": "",
                "\\": "",
                "|": "",
                "<": "",
                ">": "",
                '"': "",
                "?": "",
                ":": "",
                "*": "",
                "\x00": "",
            }  # Windows 系统和 Mac 系统
        elif s == "Linux":
            rule = {
                "/": "",
                "\x00": "",
            }  # Linux 系统
        else:
            print(_("不受支持的操作系统类型，可能无法正常去除非法字符！"))
            rule = {}
        cache = {i: "" for i in whitespace[1:]}  # 补充换行符等非法字符
        return rule | cache

    def set_rule(self, rule: dict[str, str], update=False):
        """
        设置非法字符字典

        :param rule: 替换规则，字典格式，键为非法字符，值为替换后的内容
        :param update: 如果是 True，则与原有规则字典合并，否则替换原有规则字典
        """
        self.rule = {**self.rule, **rule} if update else rule

    def filter(self, text: str) -> str:
        """
        去除非法字符

        :param text: 待处理的字符串
        :return: 替换后的字符串，如果替换后字符串为空，则返回 None
        """
        for i in self.rule:
            text = text.replace(i, self.rule[i])
        return text

    def filter_name(
        self,
        text: str,
        default: str = "",
    ) -> str:
        """过滤文件夹名称中的非法字符"""
        text = text.replace(":", ".")

        text = self.remove_control_characters(text)

        text = self.filter(text)

        text = replace_emoji(text)

        text = self.clear_spaces(text)

        text = text.strip().strip(".")

        return text or default

    @staticmethod
    def clear_spaces(string: str):
        """将连续的空格转换为单个空格"""
        return " ".join(string.split())

    @classmethod
    def remove_control_characters(
        cls,
        text,
        replace="",
    ):
        # 使用正则表达式匹配所有控制字符
        return cls.CONTROL_CHARACTERS.sub(
            replace,
            text,
        )


if __name__ == "__main__":
    demo = Cleaner()
    print(demo.rule)
    print(demo.filter_name(""))
    print(demo.remove_control_characters("hello \x08world"))
