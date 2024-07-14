from unicodedata import name


def is_chinese_char(char: str) -> bool:
    return 'CJK' in name(char, "")


def truncate_string(s: str, length: int) -> str:
    count = 0
    result = ""
    for char in s:
        if is_chinese_char(char):  # 判断是否为中文字符
            count += 2
        else:
            count += 1
        if count > length:
            break
        result += char
    return result


def trim_string(s: str, length: int) -> str:
    length = length // 2 - 2
    return f"{s[:length]}...{s[-length:]}" if len(s) > length else s


def beautify_string(s: str, length: int) -> str:
    count = 0
    for char in s:
        if is_chinese_char(char):  # 判断是否为中文字符
            count += 2
        else:
            count += 1
        if count > length:
            break
    else:
        return s
    length = length // 2
    start = truncate_string(s, length)
    end = truncate_string(s[::-1], length)[::-1]
    return f"{start}...{end}"
