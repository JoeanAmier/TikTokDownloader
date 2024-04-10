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

USERAGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 "
    "Safari/537.36 Edg/124.0.0.0")
SEC_CH_UA = "\"Chromium\";v=\"124\", \"Microsoft Edge\";v=\"124\", \"Not-A.Brand\";v=\"99\""
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
    "User-Agent": USERAGENT}
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
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Dnt': '1',
    'Origin': 'https://www.tiktok.com',
    'Priority': 'i',
    'Range': 'bytes=0-',
    'Referer': 'https://www.tiktok.com/',
    'Sec-Ch-Ua': SEC_CH_UA,
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    # 'Sec-Fetch-Dest': 'video',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': USERAGENT,
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
    "ttwid=1%7Cznatb_I92hSI92DSLFuzG4dH4UGyTM6iA4u8oVJhh5Q%7C1713708721"
    "%7Cbefda5206897461f8f07ad2b907a09899ee962d721f8494fa0bbaeb21165e913; "
    "tt_csrf_token=w6agcZyI-EjvAR03XH7lT_658y7enOeZ0-9g; tt_chain_token=8E/OiizxuQi7/JroG1Ox+A==; "
    "ak_bmsc=2B9322FE0CED5C3A9AC3A1554D146008~000000000000000000000000000000~YAAQEwzEF1MnQcyOAQAADOX"
    "/ABfoCqW70939e+uu3kswNd/hL1xa5lV0oOlFUMKpaNLhc2wMa2sq78ckNYECSPD5DfuKjVmjeGTHux6sLZX"
    "+Pv5WSD6yTeG7eRiQNYMXneEkYLrHjVPu8Wn+XUjDhLRqifMt9U"
    "/lIDNXqaVr7GKpidqBM15bpftOcrXxZTpPJoAX6BnxmDvoX9NdzQOImDYjYRsFNP11yNIpFv8yjnRbeYol0VSY7h5IphMH8ChiWvl"
    "9Ea4uo875GNH1twNfvnLDOTM8W/DBkSKYH+UWk1VXVPpN31shuSgVG46TctLZV9AcpU9vFOM8px/LOZ04x32NlU9LCaFhkXnl9Nh3"
    "RNoBc2s+VAIIwQY0E9ofhMDW35D3j7TfTU6fEZg=")

BLANK_PREVIEW = "static/images/blank.png"
