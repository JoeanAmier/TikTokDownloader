from src.custom import RETRY

__all__ = ["retry", "retry_lite", "retry_infinite", ]


def retry(function):
    """发生错误时尝试重新执行，装饰的函数需要返回布尔值"""

    def inner(self, *args, **kwargs):
        finished = kwargs.pop("finished", False)
        for i in range(self.max_retry):
            if result := function(self, *args, **kwargs):
                return result
            self.log.warning(f"正在尝试第 {i + 1} 次重试")
        if not (result := function(self, *args, **kwargs)) and finished:
            self.finished = True
        return result

    return inner


def retry_lite(function):
    def inner(*args, **kwargs):
        if r := function(*args, **kwargs):
            return r
        for _ in range(RETRY):
            if r := function(*args, **kwargs):
                return r
        return r

    return inner


def retry_infinite(function):
    def inner(self, *args, **kwargs):
        while True:
            if function(self, *args, **kwargs):
                return
            _ = self.console.input(
                "请关闭所有正在访问作品保存文件夹的窗口和程序，按下回车继续运行！")

    return inner
