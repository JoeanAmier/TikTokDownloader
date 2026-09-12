from src.encrypt import DouYinParams
from src.encrypt.douyin_params import _normalize_query
from src.encrypt.websign import sign as websign_sign


def test_douyin_sign():
    signer = DouYinParams()
    result = signer.sign(query="aid=6383&sec_user_id=test_sec_user_id&count=10")
    assert "a_bogus" in result
    assert result["a_bogus"]


def test_douyin_sign_url_with_base():
    signer = DouYinParams()
    query = signer.sign_url(
        url="https://www.douyin.com/aweme/v1/web/aweme/post",
        query="aid=6383&sec_user_id=test_sec_user_id&count=10",
    )
    # sign_url 返回纯 query 字符串，URL 由传输层拼接
    assert query.startswith("aid=6383&sec_user_id=test_sec_user_id&count=10&")
    assert "a_bogus=" in query


def test_douyin_sign_url_without_base():
    signer = DouYinParams()
    query = signer.sign_url(
        url="",
        query="aid=6383&sec_user_id=test_sec_user_id&count=10",
    )
    assert query.startswith("aid=6383&sec_user_id=test_sec_user_id&count=10&")
    assert "a_bogus=" in query


def test_douyin_sign_url_websign_with_uifid():
    signer = DouYinParams()
    query = signer.sign_url(
        url="https://www.douyin.com/aweme/v1/web/aweme/post",
        query="aid=6383&uifid=test_uifid&count=10",
    )
    # query 含 uifid 时追加 timestamp 与 x-secsdk-web-signature，
    # 且签名参数位于末尾
    assert query.startswith("aid=6383&uifid=test_uifid&count=10&")
    assert "timestamp=" in query
    name, _, value = query.split("&")[-1].partition("=")
    assert name == "x-secsdk-web-signature"
    assert len(value) == 32


def test_douyin_sign_url_websign_without_uifid():
    signer = DouYinParams()
    query = signer.sign_url(
        url="https://www.douyin.com/aweme/v1/web/aweme/post",
        query="aid=6383&count=10",
    )
    assert "timestamp=" not in query
    assert "x-secsdk-web-signature=" not in query


def test_douyin_sign_url_websign_skips_unprotected_endpoint():
    signer = DouYinParams()
    query = signer.sign_url(
        url="https://www.douyin.com/aweme/v1/web/user/profile/other/",
        query="aid=6383&uifid=test_uifid&count=10",
    )
    # 未受保护的接口即使携带 uifid 也不附加 WebSign
    assert "timestamp=" not in query
    assert "x-secsdk-web-signature=" not in query
    assert "a_bogus=" in query


def test_douyin_query_uses_standard_form_encoding_inside_signer():
    # This matches the main project's A-Bogus query encoder: quote_plus with
    # no extra safe characters.
    assert _normalize_query({"keyword": "hello world", "value": "x=y"}) == (
        "keyword=hello+world&value=x%3Dy"
    )


def test_douyin_normalizes_raw_query_string():
    assert _normalize_query("keyword=hello%20world&value=x%3dy") == (
        "keyword=hello+world&value=x%3Dy"
    )


def test_douyin_sign_url_accepts_raw_mapping_and_encodes_once():
    query = DouYinParams().sign_url(
        url="https://www.douyin.com/aweme/v1/web/user/profile/other/",
        query={"keyword": "hello world", "value": "x=y"},
    )
    assert query.startswith("keyword=hello+world&value=x%3Dy&")


def test_douyin_websign_reencodes_query_like_native_signer():
    query, _ = websign_sign(
        "keyword=hello+world&uifid=test_uifid&a_bogus=sig%2Bwith%2Fchars",
        "test_uifid",
        timestamp=1788848901,
    )
    assert query.startswith(
        "keyword=hello%2Bworld&uifid=test_uifid&"
        "a_bogus=sig%2Bwith%2Fchars&timestamp=1788848901&"
    )


def test_douyin_websign_keeps_literal_plus_in_uifid():
    query, _ = websign_sign(
        "aid=6383&uifid=visitor+id&count=10",
        "visitor+id",
        timestamp=1788848901,
    )
    assert "uifid=visitor%2Bid" in query


def test_douyin_protected_query_is_canonicalized_before_a_bogus(monkeypatch):
    captured_queries = []
    signer = DouYinParams()

    def capture_a_bogus(query, data, user_agent):
        captured_queries.append(query)
        return "test_a_bogus"

    monkeypatch.setattr(signer, "_get_a_bogus", capture_a_bogus)
    query = signer.sign_url(
        url="https://www.douyin.com/aweme/v1/web/aweme/post/",
        query={"os_name": "Mac OS", "uifid": "test_uifid"},
    )

    # A-Bogus receives WebSign's canonical query representation.
    assert captured_queries == ["os_name=Mac%2BOS&uifid=test_uifid"]
    assert query.startswith("os_name=Mac%2BOS&uifid=test_uifid&")
