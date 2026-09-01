from src.encrypt import TikTokParams


def test_tiktok_sign():
    signer = TikTokParams()
    result = signer.sign(
        query="aid=1988&count=2",
        ms_token="test_ms_token_123",
    )
    assert result["X-Dynosaur"]
    assert result["X-Gnarly"]
    assert result["X-Bogus"]


def test_tiktok_sign_url_with_base():
    signer = TikTokParams()
    url = signer.sign_url(
        url="https://www.tiktok.com/api/feed",
        query="aid=1988&count=2",
        ms_token="test_ms_token_123",
    )
    assert url.startswith("https://www.tiktok.com/api/feed?")
    assert "aid=1988&count=2" in url
    assert "X-Dynosaur=" in url
    assert "msToken=test_ms_token_123" in url
    assert "X-Bogus=" in url
    assert "X-Gnarly=" in url


def test_tiktok_sign_url_without_base():
    signer = TikTokParams()
    query = signer.sign_url(
        url="",
        query="aid=1988&count=2",
        ms_token="test_ms_token_123",
    )
    assert "aid=1988&count=2" in query
    assert "X-Dynosaur=" in query
    assert "X-Bogus=" in query
    assert "X-Gnarly=" in query
