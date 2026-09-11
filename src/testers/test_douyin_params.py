from src.encrypt import DouYinParams


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
