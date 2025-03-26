from http.cookiejar import Cookie, CookieJar

from pytest import mark

from src.tools import (
    cookie_dict_to_str,
    cookie_jar_to_dict,
    cookie_str_to_dict,
    cookie_str_to_str,
    format_size,
)


@mark.parametrize(
    "x, y",
    [
        (
            "UIFID_V=2; UIFID_TEMP=aaa; fpk1=aaa; fpk2=aaa; tiktok",
            {"UIFID_V": "2", "UIFID_TEMP": "aaa", "fpk1": "aaa", "fpk2": "aaa"},
        ),
    ],
)
def test_cookie_str_to_dict(x, y):
    assert cookie_str_to_dict(x) == y


@mark.parametrize(
    "x, y",
    [
        (
            "ixigua-a-s=1; path=/; secure; httponly",
            "ixigua-a-s=1",
        ),
    ],
)
def test_cookie_str_to_str(x, y):
    assert cookie_str_to_str(x) == y


@mark.parametrize(
    "x, y",
    [
        (
            {"UIFID_V": "2", "UIFID_TEMP": "aaa", "fpk1": "aaa", "fpk2": "aaa"},
            "UIFID_V=2; UIFID_TEMP=aaa; fpk1=aaa; fpk2=aaa",
        ),
        ({"name": "value"}, "name=value"),
    ],
)
def test_cookie_dict_to_str(x, y):
    assert cookie_dict_to_str(x) == y


def create_test_cookie_jar():
    jar = CookieJar()
    jar.set_cookie(
        Cookie(
            version=0,
            name="cookie_name",
            value="cookie_value",
            port=None,
            port_specified=False,
            domain="example.com",
            domain_specified=True,
            domain_initial_dot=False,
            path="/",
            path_specified=True,
            secure=False,
            expires=None,
            discard=False,
            comment=None,
            comment_url=None,
            rest={},
        )
    )
    return jar


@mark.parametrize(
    "x, y",
    [
        (
            create_test_cookie_jar(),
            {"cookie_name": "cookie_value"},
        ),
    ],
)
def test_cookie_jar_to_dict(x, y):
    assert cookie_jar_to_dict(x) == y


@mark.parametrize(
    "x, y",
    [
        (1024 * 1024, "1.00 MB"),
        (1024 * 512, "512.00 KB"),
        (1024 * 1024 * 2.25, "2.25 MB"),
    ],
)
def test_format_size(x, y):
    assert format_size(x) == y
