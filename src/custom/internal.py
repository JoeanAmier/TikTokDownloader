from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
VERSION_MAJOR = 5
VERSION_MINOR = 6
VERSION_BETA = True
__VERSION__ = f"{VERSION_MAJOR}.{VERSION_MINOR}.{'beta' if VERSION_BETA else 'stable'}"
PROJECT_NAME = f"TikTokDownloader V{VERSION_MAJOR}.{VERSION_MINOR} {
    'Beta' if VERSION_BETA else 'Stable'
}"

REPOSITORY = "https://github.com/JoeanAmier/TikTokDownloader"
LICENCE = "GNU General Public License v3.0"
DOCUMENTATION_URL = "https://github.com/JoeanAmier/TikTokDownloader/wiki/Documentation"
RELEASES = "https://github.com/JoeanAmier/TikTokDownloader/releases/latest"

DISCLAIMER_TEXT = (
    ""
    "关于 TikTokDownloader 的 免责声明：\n"
    "\n"
    "1.使用者对本项目的使用由使用者自行决定，并自行承担风险。作者对使用者使用本项"
    "目所产生的任何损失、责任、或风险概不负责。\n"
    "2.本项目的作者提供的代码和功能是基于现有知识和技术的开发成果。作者尽力确保代"
    "码的正确性和安全性，但不保证代码完全没有错误或缺陷。\n"
    "3.使用者在使用本项目时必须严格遵守 GNU General Public License v3.0 的要求，并"
    "在适当的地方注明使用了 GNU General Public License v3.0 的代码。\n"
    "4.使用者在任何情况下均不得将本项目的作者、贡献者或其他相关方与使用者的使用行"
    "为联系起来，或要求其对使用者使用本项目所产生的任何损失或损害负责。\n"
    "5.使用者在使用本项目的代码和功能时，必须自行研究相关法律法规，并确保其使用行"
    "为合法合规。任何因违反法律法规而导致的法律责任和风险，均由使用者自行承担。\n"
    "6.本项目的作者不会提供 TikTokDownloader 项目的付费版本，也不会提供与 "
    "TikTokDownloader 项目相关的任何商业服务。\n"
    "7.基于本项目进行的任何二次开发、修改或编译的程序与原创作者无关，原创作者不承"
    "担与二次开发行为或其结果相关的任何责任，使用者应自行对因二次开发可能带来的各"
    "种情况负全部责任。\n"
    "\n"
    "在使用本项目的代码和功能之前，请您认真考虑并接受以上免责声明。如果您对上述声"
    "明有任何疑问或不同意，请不要使用本项目的代码和功能。如果您使用了本项目的代码"
    "和功能，则视为您已完全理解并接受上述免责声明，并自愿承担使用本项目的一切风险"
    "和后果。\n"
)

RETRY = 5
TIMEOUT = 10

PHONE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "CriOS/125.0.6422.51 Mobile/15E148 Safari/604.1",
}
USERAGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 "
    "Safari/537.36"
)
BLANK_HEADERS = {
    "User-Agent": USERAGENT,
}
REFERER = "https://www.douyin.com/?recommend=1"
REFERER_TIKTOK = "https://www.tiktok.com/explore"
PARAMS_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "*/*",
    "Content-Type": "text/plain;charset=UTF-8",
    "Referer": REFERER,
    "User-Agent": USERAGENT,
}
PARAMS_HEADERS_TIKTOK = PARAMS_HEADERS | {
    "Referer": REFERER_TIKTOK,
}
DATA_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "*/*",
    "Referer": REFERER,
    "User-Agent": USERAGENT,
}
DATA_HEADERS_TIKTOK = DATA_HEADERS | {
    "Referer": REFERER_TIKTOK,
}
DOWNLOAD_HEADERS = {
    "Accept": "*/*",
    "Range": "bytes=0-",
    "Referer": REFERER,
    "User-Agent": USERAGENT,
}
DOWNLOAD_HEADERS_TIKTOK = DOWNLOAD_HEADERS | {
    "Referer": REFERER_TIKTOK,
}
QRCODE_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "*/*",
    "Referer": REFERER,
    "User-Agent": USERAGENT,
}

BLANK_PREVIEW = "static/images/blank.png"

VIDEO_INDEX: int = -1
VIDEO_TIKTOK_INDEX: int = 0
IMAGE_INDEX: int = -1
IMAGE_TIKTOK_INDEX: int = -1
VIDEOS_INDEX: int = -1
DYNAMIC_COVER_INDEX: int = -1
STATIC_COVER_INDEX: int = -1
MUSIC_INDEX: int = -1
COMMENT_IMAGE_INDEX: int = -1
COMMENT_STICKER_INDEX: int = -1
LIVE_COVER_INDEX: int = -1
AUTHOR_COVER_INDEX: int = -1
HOT_WORD_COVER_INDEX: int = -1
COMMENT_IMAGE_LIST_INDEX: int = 0
BITRATE_INFO_TIKTOK_INDEX: int = 0
LIVE_DATA_INDEX: int = 0
AVATAR_LARGER_INDEX: int = 0
AUTHOR_COVER_URL_INDEX: int = 0
SEARCH_USER_INDEX: int = 0
SEARCH_AVATAR_INDEX: int = 0
MUSIC_COLLECTION_COVER_INDEX: int = 0
MUSIC_COLLECTION_DOWNLOAD_INDEX: int = 0

if __name__ == "__main__":
    print(__VERSION__)
