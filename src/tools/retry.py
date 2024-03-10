from src.custom import RETRY

__all__ = ["PrivateRetry"]


class PrivateRetry:
    """重试器，仅适用于本项目！"""

    @staticmethod
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

    @staticmethod
    def retry_lite(function):
        def inner(*args, **kwargs):
            if r := function(*args, **kwargs):
                return r
            for _ in range(RETRY):
                if r := function(*args, **kwargs):
                    return r
            return r

        return inner

    @staticmethod
    def retry_limited(function):
        def inner(self, *args, **kwargs):
            while True:
                if function(self, *args, **kwargs):
                    return
                if self.console.input(
                        "如需重新尝试处理该对象，请关闭所有正在访问该对象的窗口或程序，然后直接按下回车键！\n如需跳过处理该对象，请输入任意字符后按下回车键！"):
                    return

        return inner

    @staticmethod
    def retry_infinite(function):
        def inner(self, *args, **kwargs):
            while True:
                if function(self, *args, **kwargs):
                    return
                self.console.input("请关闭所有正在访问该对象的窗口或程序，然后按下回车键继续处理！")

        return inner
