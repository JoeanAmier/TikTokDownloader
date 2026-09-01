from src.encrypt import DouYinParams


def test_douyin_sign():
    signer = DouYinParams()
    result = signer.sign(query="aid=6383&sec_user_id=test_sec_user_id&count=10")
    assert "a_bogus" in result
    assert result["a_bogus"]


def test_douyin_sign_url_with_base():
    signer = DouYinParams()
    url = signer.sign_url(
        url="https://www.douyin.com/aweme/v1/web/aweme/post",
        query="aid=6383&sec_user_id=test_sec_user_id&count=10",
    )
    assert url.startswith("https://www.douyin.com/aweme/v1/web/aweme/post?")
    assert "aid=6383&sec_user_id=test_sec_user_id&count=10" in url
    assert "a_bogus=" in url


def test_douyin_sign_url_without_base():
    signer = DouYinParams()
    query = signer.sign_url(
        url="",
        query="aid=6383&sec_user_id=test_sec_user_id&count=10",
    )
    assert "aid=6383&sec_user_id=test_sec_user_id&count=10" in query
    assert "a_bogus=" in query
    assert "?" not in query.split("&")[0] or query.startswith("aid=")
