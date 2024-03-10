from random import randint
from time import sleep
from typing import TYPE_CHECKING

# from time import time
from .static import GENERAL

if TYPE_CHECKING:
    from src.tools import ColorfulConsole

__all__ = [
    "wait",
    "failure_handling",
    "illegal_nickname",
    "condition_filter",
    "suspend",
    "verify_token",
]


def wait() -> None:
    """
    设置网络请求间隔时间，仅对获取数据生效，不影响下载文件
    """
    # 随机延时
    sleep(randint(15, 45) * 0.1)
    # 固定延时
    # sleep(2)
    # 取消延时
    # pass


def failure_handling() -> bool:
    """批量下载账号作品模式 和 批量下载合集作品模式 获取数据失败时，是否继续执行"""
    # 询问用户
    return bool(input("输入任意字符继续处理账号/合集，直接回车停止处理账号/合集: "))
    # 继续执行
    # return True
    # 结束执行
    # return False


def illegal_nickname() -> str:
    """当 账号昵称/标识 或者 合集标题/标识 过滤非法字符后不是有效的文件夹名称时，如何处理异常"""
    # 询问用户
    return input("当前 账号昵称/标识 或者 合集标题/标识 不是有效的文件夹名称，请输入临时的账号标识或者合集标识：")
    # 使用当前时间戳作为账号昵称/标识或者合集标题/标识
    # 需要将第 5 行代码取消注释
    # return str(time())[:10]


def condition_filter(data: dict) -> bool:
    """
    自定义作品筛选规则，例如：筛选作品点赞数、作品类型、视频分辨率等
    需要排除的作品返回 False，否则返回 True
    """
    # if data["ratio"] in ("720p", "540p"):
    #     return False  # 过滤低分辨率的视频作品
    return True


def suspend(count: int, console: "ColorfulConsole") -> None:
    """
    如需采集大量数据，请启用该函数，可以在处理指定数量的数据后，暂停一段时间，然后继续运行
    batches: 每次处理的数据数量上限，比如：每次处理 10 个数据，就会暂停程序
    rest_time: 程序暂停的时间，单位：秒；比如：每处理 10 个数据，就暂停 5 分钟
    仅对 批量下载账号作品模式 和 批量下载合集作品模式 生效
    说明: 此处的一个数据代表一个账号或者一个合集，并非代表一个数据包
    """
    # 启用该函数
    batches = 10  # 根据实际需求修改
    if not count % batches:
        rest_time = 60 * 5  # 根据实际需求修改
        console.print(
            f"程序已经处理了 {batches} 个数据，为了避免请求频率过高导致账号或 IP 被风控，程序已经暂停运行，"
            f"在 {rest_time} 秒后继续处理数据！", style=GENERAL)
        sleep(rest_time)
    # 默认不启用
    # pass


def verify_token(token: str) -> bool:
    """Web API 接口模式 和 服务器部署模式 设置 token 参数验证"""
    return True
