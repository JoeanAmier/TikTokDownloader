# 启用延迟需要取消注释
# from random import randint
# from time import sleep

# 线程池最大线程数量，多线程下载文件时使用
# 短期大批量下载文件可以适当设置更大的值
# 长期大批量下载文件不建议设置过大的值，可能会导致下载无响应（可能是抖音端风控）
MAX_WORKERS = 4


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
