from pathlib import Path

__all__ = [
    "PROJECT_ROOT",
    "VERSION_MAJOR",
    "VERSION_MINOR",
    "VERSION_BETA",
    "REPOSITORY",
    "LICENCE",
    "DOCUMENTATION_URL",
    "RELEASES",
    "RETRY",
    "USERAGENT",
    "DISCLAIMER_TEXT",
    "BLANK_PREVIEW",
    "TIMEOUT",
    "PROJECT_NAME",
    "PARAMS_HEADERS",
    "DATA_HEADERS",
    "WID_COOKIE",
    "DOWNLOAD_HEADERS",
    "QRCODE_HEADERS",
    "DOWNLOAD_HEADERS_TIKTOK",
]

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
VERSION_MAJOR = 5
VERSION_MINOR = 4
VERSION_BETA = True
PROJECT_NAME = f"TikTokDownloader V{VERSION_MAJOR}.{
VERSION_MINOR}{" Beta" if VERSION_BETA else ""}"

REPOSITORY = "https://github.com/JoeanAmier/TikTokDownloader"
LICENCE = "GNU General Public License v3.0"
DOCUMENTATION_URL = "https://github.com/JoeanAmier/TikTokDownloader/wiki/Documentation"
RELEASES = "https://github.com/JoeanAmier/TikTokDownloader/releases/latest"
DISCLAIMER_TEXT = (
    "关于 TikTokDownloader 的 免责声明：",
    "",
    "1. 使用者对本项目的使用由使用者自行决定，并自行承担风险。作者对使用者使用本项目所产生的任何损失、责任、或风险概不负责。",
    "2. 本项目的作者提供的代码和功能是基于现有知识和技术的开发成果。作者尽力确保代码的正确性和安全性，但不保证代码完全没有错误或缺陷。",
    "3. 使用者在使用本项目时必须严格遵守 GNU General Public License v3.0 的要求，并在适当的地方注明使用了 GNU General Public License v3.0 的代码。",
    "4. 使用者在任何情况下均不得将本项目的作者、贡献者或其他相关方与使用者的使用行为联系起来，或要求其对使用者使用本项目所产生的任何损失或损害负责。",
    "5. 使用者在使用本项目的代码和功能时，必须自行研究相关法律法规，并确保其使用行为合法合规。任何因违反法律法规而导致的法律责任和风险，均由使用者自行承担。",
    "6. 本项目的作者不会提供 TikTokDownloader 项目的付费版本，也不会提供与 TikTokDownloader 项目相关的任何商业服务。",
    "7. 基于本项目进行的任何二次开发、修改或编译的程序与原创作者无关，原创作者不承担与二次开发行为或其结果相关的任何责任，使用者应自行对因"
    "二次开发可能带来的各种情况负全部责任。",
    "",
    "在使用本项目的代码和功能之前，请您认真考虑并接受以上免责声明。如果您对上述声明有任何疑问或不同意，请不要使用本项目的代码和功能。如果"
    "您使用了本项目的代码和功能，则视为您已完全理解并接受上述免责声明，并自愿承担使用本项目的一切风险和后果。",
    "",
)

RETRY = 5
TIMEOUT = 10

USERAGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 "
             "Safari/537.36")
SEC_CH_UA = '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"'
PARAMS_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Content-Type": "text/plain;charset=UTF-8",
    "Dnt": "1",
    "Origin": "https://www.douyin.com",
    "Referer": "https://www.douyin.com/",
    "Sec-Ch-Ua": SEC_CH_UA,
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": USERAGENT,
}
DATA_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Dnt": "1",
    "Referer": "https://www.douyin.com/?recommend=1",
    "Sec-Ch-Ua": SEC_CH_UA,
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": USERAGENT,
}
DOWNLOAD_HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Dnt': '1',
    'Origin': 'https://www.douyin.com',
    'Priority': 'i',
    'Range': 'bytes=0-',
    'Referer': 'https://www.douyin.com/',
    'Sec-Ch-Ua': SEC_CH_UA,
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    # 'Sec-Fetch-Dest': 'video',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': USERAGENT,
}
DOWNLOAD_HEADERS_TIKTOK = {
    "Accept": "*/*",
    # "Accept-Encoding": "identity;q=1, *;q=0",
    "Accept-Language": "zh-SG,zh-CN;q=0.9,zh;q=0.8",
    "Connection": "keep-alive",
    "DNT": "1",
    # "Host": "v16-webapp-prime.us.tiktok.com",
    "Origin": "https://www.tiktok.com",
    "Range": "bytes=0-",
    "Referer": "https://www.tiktok.com/",
    # "Sec-Fetch-Dest": "video",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": USERAGENT,
    "sec-ch-ua": SEC_CH_UA,
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
QRCODE_HEADERS = {
    "Accept": "application/json, text/javascript",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Dnt": "1",
    "Origin": "https://www.douyin.com",
    "Referer": "https://www.douyin.com/",
    "Sec-Ch-Ua": SEC_CH_UA,
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": USERAGENT,
}
WID_COOKIE = (
    "ttwid=1%7CovVQu2St-HXSHAdEfZ7tljPe151SZ88AbrlTirlaC6w%7C1701072604"
    "%7C49b17849da69bafc3638e794f3f26b30fe9677c5253e65a2a5f615489846ce02")

BLANK_PREVIEW = "static/images/blank.png"
