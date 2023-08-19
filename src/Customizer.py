from random import randint
from time import sleep


def wait():
    """设置网络请求间隔时间，仅对获取数据生效，不影响下载文件"""
    # 随机延时
    sleep(randint(15, 35) * 0.1)
    # 固定间隔
    # sleep(2)
    # 取消间隔
    # pass


def failed():
    """获取数据失败时，是否继续执行"""
    # 询问用户
    return input("输入任意字符继续运行，直接回车结束运行: ")
    # 继续执行
    # return True
    # 结束执行
    # return False
