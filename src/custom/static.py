__all__ = [
    "MAX_WORKERS",
    "DESCRIPTION_LENGTH",
    "TEXT_REPLACEMENT",
    "SERVER_HOST",
    "SERVER_PORT",
    "MASTER",
    "PROMPT",
    "WARNING",
    "ERROR",
    "INFO",
    "GENERAL",
    "PROGRESS",
    "COOKIE_UPDATE_INTERVAL",
    "BACKUP_RECORD_INTERVAL",
]

# 线程池最大线程数量，多线程下载文件时使用
# 短期大批量下载文件可以适当设置更大的值
# 长期大批量下载文件不建议设置过大的值，可能会导致下载无响应（可能是抖音端风控）
MAX_WORKERS = 4

# 作品描述最大长度限制，仅对作品文件名称生效，不影响数据储存，设置时需要考虑系统文件名称最大长度限制
DESCRIPTION_LENGTH = 64

# 非法字符替换规则，key 为替换前的文本，value 为替换后的文本
TEXT_REPLACEMENT = {
    " ": " ",
}

# 服务器模式主机，仅对 Web API 接口模式 生效，设置为 "0.0.0.0" 可以启用局域网访问（外部可用）
SERVER_HOST = "127.0.0.1"

# 服务器模式端口，对 Web API 接口模式、Web UI 交互模式、服务器部署模式 生效
SERVER_PORT = 5000

# Cookie 更新间隔，单位：秒
COOKIE_UPDATE_INTERVAL = 10 * 60

# 作品下载记录数据备份间隔，单位：秒
BACKUP_RECORD_INTERVAL = 5 * 60

# 彩色交互提示颜色设置，支持标准颜色名称、Hex、RGB 格式
MASTER = "b #fff200"
PROMPT = "b turquoise2"
GENERAL = "b bright_white"
PROGRESS = "b bright_magenta"
ERROR = "b bright_red"
WARNING = "b bright_yellow"
INFO = "b bright_green"
