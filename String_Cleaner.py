class StringCleaner:
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

    def set_rule(self, rule: dict[str, str]):
        """
        Set custom replacement rules.

        :param rule: Replacement rules, dictionary keys and values are string types.
        """
        self.replace = rule

    def filter(self, text: str) -> str:
        """
        Replace string.

        :param text: String to be processed.
        :return: Replaced string.
        """
        for i in self.replace:
            text = text.replace(i, self.replace[i])
        return text
