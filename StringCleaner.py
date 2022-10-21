from string import whitespace


class Cleaner:
    def __init__(self):
        """
        Replace illegal Windows system characters contained in the string,
        or you can customize the replacement rules.
        """
        self.replace = {
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

    def set_rule(self, rule: dict[str, str], update=False):
        """
        Set custom replacement rules.

        :param rule: Replacement rules, dictionary keys and values are string types.
        :param update: If True, update the default rule, if False, replace the default rule.
        """
        if update:
            for i, j in rule.items():
                self.replace[i] = j
        else:
            self.replace = rule

    def filter(self, text: str) -> str:
        """
        Replace string.

        :param text: String to be processed.
        :return: Replaced string.
        """
        for i in self.replace:
            text = text.replace(i, self.replace[i])
            text = "".join(i for i in text if i not in whitespace)
        if text:
            return text
        raise ValueError("The processed string is empty!")
