import platform
from string import whitespace


class Cleaner:
    def __init__(self):
        """
        Replace illegal Windows system characters contained in the string,
        or you can customize the replacement rules.
        """
        self.rule = self.default_rule()

    @staticmethod
    def default_rule():
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
                }  # Windows system illegal characters
            case "Linux":
                rule = {}
            case _:
                rule = {}
        cache = {i: "" for i in whitespace[1:]}
        rule = {**rule, **cache}
        return rule

    def get_rule(self):
        print(self.rule)
        return self.rule

    def set_rule(self, rule: dict[str, str], update=False):
        """
        Set custom replacement rules.

        :param rule: Replacement rules, dictionary keys and values are string types.
        :param update: If True, update the default rule, if False, replace the default rule.
        """
        self.rule = {**self.rule, **rule} if update else rule

    def filter(self, text: str) -> str:
        """
        Replace string.

        :param text: String to be processed.
        :return: Replaced string.
        """
        for i in self.rule:
            text = text.replace(i, self.rule[i])
        return text or None


if __name__ == "__main__":
    demo = Cleaner()
    demo.get_rule()
