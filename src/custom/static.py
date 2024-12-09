# 同时下载作品文件的最大任务数，对直播无效
MAX_WORKERS = 4

# 作品描述最大长度限制，仅对作品文件名称生效，不影响数据储存，设置时需要考虑系统文件名称最大长度限制
DESCRIPTION_LENGTH = 64

# 文件名称最大长度限制
MAX_FILENAME_LENGTH = 128

# 非法字符替换规则，key 为替换前的文本，value 为替换后的文本
TEXT_REPLACEMENT = {
    " ": " ",
}

# 服务器模式主机，仅对 Web API 接口模式 生效，设置为 "0.0.0.0" 可以启用局域网访问（外部可用）
SERVER_HOST = "127.0.0.1"

# 服务器模式端口，对 Web API 接口模式、Web UI 交互模式、服务器部署模式 生效
SERVER_PORT = 5000

# Cookie 更新间隔，单位：秒
COOKIE_UPDATE_INTERVAL = 20 * 60

# 彩色交互提示颜色设置，支持标准颜色名称、Hex、RGB 格式
MASTER = "b #fff200"
PROMPT = "b turquoise2"
GENERAL = "b bright_white"
PROGRESS = "b bright_magenta"
ERROR = "b bright_red"
WARNING = "b bright_yellow"
INFO = "b bright_green"
DEBUG = "b dark_orange"

# 文件类型签名
FILE_SIGNATURES: tuple[tuple[int, bytes, str,], ...] = (
    # 分别为偏移量(字节)、十六进制签名、后缀
    # 参考：https://en.wikipedia.org/wiki/List_of_file_signatures
    # 参考：https://www.garykessler.net/library/file_sigs.html
    (0, b"\xFF\xD8\xFF", "jpg"),
    (0, b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A", "png"),
    (4, b"\x66\x74\x79\x70\x61\x76\x69\x66", "avif"),
    (4, b"\x66\x74\x79\x70\x68\x65\x69\x63", "heic"),
    (8, b"\x57\x45\x42\x50", "webp"),
    (4, b"\x66\x74\x79\x70\x4D\x53\x4E\x56", "mp4"),
    (4, b"\x66\x74\x79\x70\x69\x73\x6F\x6D", "mp4"),
    (4, b"\x66\x74\x79\x70\x6D\x70\x34\x32", "m4v"),
    (4, b"\x66\x74\x79\x70\x71\x74\x20\x20", "mov"),
    (0, b"\x1A\x45\xDF\xA3", "mkv"),
    (0, b"\x00\x00\x01\xB3", "mpg"),
    (0, b"\x00\x00\x01\xBA", "mpg"),
    (0, b"\x46\x4c\x56\x01", "flv"),
    (8, b"\x41\x56\x49\x20", "avi"),
)
FILE_SIGNATURES_LENGTH = max(offset + len(signature) for offset, signature, _ in FILE_SIGNATURES)
