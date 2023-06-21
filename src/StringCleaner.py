import platform
from string import whitespace


class Cleaner:
    def __init__(self):
        """
        替换字符串中包含的非法字符，默认根据系统类型生成对应的非法字符字典，也可以自行设置非法字符字典
        """
        self.rule = self.default_rule()  # 默认非法字符字典

    @staticmethod
    def default_rule():
        """根据系统类型生成默认非法字符字典"""
        system = platform.system()
        match system:
            case "Windows":
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
                }  # Windows 系统
            case "Linux":
                rule = {}  # Linux 系统，待完善
            case _:
                rule = {}  # 其他系统需要自行设置
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
        return text or None


if __name__ == "__main__":
    demo = Cleaner()
    print(demo.rule)
