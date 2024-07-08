def truncate_string(s: str, length: int) -> str:
    count = 0
    result = ""
    for char in s:
        if '\u4e00' <= char <= '\u9fff':  # 判断是否为中文字符
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
