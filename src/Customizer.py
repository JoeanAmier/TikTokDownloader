# 启用延迟需要取消注释
# from random import randint
# from time import sleep

__all__ = [
    "MAX_WORKERS",
    "wait",
    "failed",
    "illegal_nickname",
    "check_login",
    "DESCRIPTION_LENGTH",
    "TEXT_REPLACEMENT",
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


def wait():
    """设置网络请求间隔时间，仅对获取数据生效，不影响下载文件"""
    # 随机延时
    # sleep(randint(15, 35) * 0.1)
    # 固定延时
    # sleep(2)
    # 取消延时
    pass


def failed():
    """获取数据失败时，是否继续执行"""
    # 询问用户
    return input("输入任意字符继续运行，直接回车结束运行: ")
    # 继续执行
    # return True
    # 结束执行
    # return False


def illegal_nickname():
    """当账号昵称 / 合集标题过滤非法字符后不是有效的文件夹名称时，如何处理"""
    # 询问用户
    return input("当前账号昵称或者合集标题不是有效的文件夹名称，请输入自定义的账号标识或者合集标识：")
    # 使用当前时间戳作为账号昵称或者合集标题
    # return str(time())[:10]


def check_login():
    """扫描二维码登录账号时，是否询问用户再进行登录结果检查"""
    # 询问用户
    return input("是否已完成扫码登录？直接回车开始检查登录结果，输入任何字符放弃操作：")
    # 直接检查
    # return False
