from http.cookiejar import CookieJar
from re import compile

__all__ = [
    "cookie_str_to_dict",
    "cookie_dict_to_str",
    "cookie_jar_to_dict",
    "cookie_str_to_str",
]


def cookie_str_to_dict(cookie_str: str) -> dict:
    if not cookie_str:
        return {}
    cookie = {}
    pattern = compile(r"(?P<key>[^=;,]+)=(?P<value>[^;,]+)")
    matches = pattern.finditer(cookie_str)
    for match in matches:
        key = match.group('key').strip()
        value = match.group('value').strip()
        cookie[key] = value
    return cookie


def cookie_str_to_str(cookie_str: str) -> str:
    if not cookie_str:
        return ""
    pattern = compile(r", (?=\D)")
    return "; ".join(cookie.split("; ")[0]
                     for cookie in pattern.split(cookie_str))


def cookie_dict_to_str(cookie_dict: dict | CookieJar) -> str:
    if not cookie_dict:
        return ""
    cookie_pairs = [f"{key}={value}" for key, value in cookie_dict.items()]
    return "; ".join(cookie_pairs)


def cookie_jar_to_dict(cookie_jar: CookieJar) -> dict:
    return {i.name: i.value for i in cookie_jar}
