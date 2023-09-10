from platform import system
from re import sub
from string import whitespace

from src.Customizer import illegal_nickname

__all__ = ['Cleaner', 'Colour']


class Cleaner:
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
                "\"": "",
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
            print("不受支持的操作系统类型，可能无法正常去除非法字符！")
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

    @staticmethod
    def clean_name(text):
        """清洗字符串，仅保留中文、英文、数字和下划线"""
        # 使用正则表达式匹配非中文、英文、数字和下划线字符，并替换为单个下划线
        text = sub(r'[^\u4e00-\u9fa5a-zA-Z0-9_]+', '_', text)

        # 去除连续的下划线
        text = sub(r'_+', '_', text)

        # 去除首尾的下划线
        text = text.strip('_')

        return text or illegal_nickname()

    @staticmethod
    def clear_spaces(string: str):
        """将连续的空格转换为单个空格"""
        return " ".join(string.split())


class Colour:

    def __init__(self, switch):
        self.switch = switch

    def colorize(
            self,
            text: str,
            font: int,
            background=None,
            bold=None,
            default="97;1"):
        if not self.switch:
            return text
        code = ";".join(
            [str(i) for i in (font, background, bold) if isinstance(i, int)])
        return f"\x1b[{code}m{text}\x1b[{default}m"


if __name__ == "__main__":
    demo = Cleaner()
    print(demo.rule)
