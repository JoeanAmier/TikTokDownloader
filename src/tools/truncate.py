from unicodedata import name


def is_chinese_char(char: str) -> bool:
    return "CJK" in name(char, "")


def truncate_string(s: str, length: int = 64) -> str:
    count = 0
    result = ""
    for char in s:
        count += 2 if is_chinese_char(char) else 1
        if count > length:
            break
        result += char
    return result


def trim_string(s: str, length: int = 64) -> str:
    length = length // 2 - 2
    return f"{s[:length]}...{s[-length:]}" if len(s) > length else s


def beautify_string(s: str, length: int = 64) -> str:
    count = 0
    for char in s:
        count += 2 if is_chinese_char(char) else 1
        if count > length:
            break
    else:
        return s
    length //= 2
    start = truncate_string(s, length)
    end = truncate_string(s[::-1], length)[::-1]
    return f"{start}...{end}"
