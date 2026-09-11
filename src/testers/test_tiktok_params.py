from src.encrypt import TikTokParams
from src.encrypt.tiktok_params import _query_to_string


def test_tiktok_sign():
    signer = TikTokParams()
    result = signer.sign(
        query="aid=1988&count=2",
        ms_token="test_ms_token_123",
    )
    assert result["X-Dynosaur"]
    assert result["X-Gnarly"]
    # HTTP 请求上 X-Bogus 为字面量 "1"，与 SDK 行为一致
    assert result["X-Bogus"] == "1"
    assert result["msToken"] == "test_ms_token_123"


def test_tiktok_sign_url_with_base():
    signer = TikTokParams()
    query = signer.sign_url(
        url="https://www.tiktok.com/api/feed",
        query="aid=1988&count=2",
        ms_token="test_ms_token_123",
    )
    # sign_url 返回纯 query 字符串，URL 由传输层拼接
    assert query.startswith("aid=1988&count=2&X-Dynosaur=")
    assert "msToken=test_ms_token_123" in query
    assert "X-Bogus=1" in query
    assert "X-Gnarly=" in query


def test_tiktok_sign_url_without_base():
    signer = TikTokParams()
    query = signer.sign_url(
        url="",
        query="aid=1988&count=2",
        ms_token="test_ms_token_123",
    )
    assert query.startswith("aid=1988&count=2&X-Dynosaur=")
    assert "X-Bogus=1" in query
    assert "X-Gnarly=" in query


def test_tiktok_sign_url_parameter_order():
    signer = TikTokParams()
    query = signer.sign_url(
        url="",
        query="aid=1988&count=2",
        ms_token="test_ms_token_123",
    )
    # 参数顺序由 SDK 决定：X-Dynosaur、msToken、X-Bogus、X-Gnarly
    assert (
        query.index("X-Dynosaur=")
        < query.index("msToken=")
        < query.index("X-Bogus=")
        < query.index("X-Gnarly=")
    )


def test_tiktok_sign_url_ms_token_in_query():
    signer = TikTokParams()
    query = signer.sign_url(
        url="",
        query="aid=1988&count=2&msToken=test_ms_token_123",
    )
    # query 自带的 msToken 被摘出并移至 SDK 固定位置，不出现第二份
    assert query.count("msToken=") == 1
    assert "msToken=test_ms_token_123" in query


def test_tiktok_query_uses_browser_encoding():
    assert _query_to_string(
        {
            "browser_version": "5.0 (Windows)",
            "root_referer": "https://www.tiktok.com/",
            "tz_name": "America/Los_Angeles",
            "q": "中",
        }
    ) == (
        "browser_version=5.0%20(Windows)"
        "&root_referer=https://www.tiktok.com/"
        "&tz_name=America/Los_Angeles"
        "&q=%E4%B8%AD"
    )


def test_tiktok_query_ms_token_wins_over_explicit_argument():
    query = TikTokParams().sign_url(
        query="aid=1988&msToken=from-query",
        ms_token="from-argument",
    )
    assert "&msToken=from-query&" in query
    assert "from-argument" not in query
