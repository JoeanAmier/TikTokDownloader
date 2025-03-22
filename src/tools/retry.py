from ..custom import RETRY, wait
from ..translation import _

__all__ = ["Retry"]


class Retry:
    """重试器，仅适用于本项目！"""

    @staticmethod
    def retry(function):
        """发生错误时尝试重新执行，装饰的函数需要返回布尔值"""

        async def inner(self, *args, **kwargs):
            finished = kwargs.pop("finished", False)
            for i in range(self.max_retry):
                if result := await function(self, *args, **kwargs):
                    return result
                self.log.warning(_("正在进行第 {index} 次重试").format(index=i + 1))
                await wait()
            if not (result := await function(self, *args, **kwargs)) and finished:
                self.finished = True
            return result

        return inner

    @staticmethod
    def retry_lite(function):
        async def inner(*args, **kwargs):
            if r := await function(*args, **kwargs):
                return r
            for _ in range(RETRY):
                if r := await function(*args, **kwargs):
                    return r
                await wait()
            return r

        return inner

    @staticmethod
    def retry_limited(function):
        def inner(self, *args, **kwargs):
            while True:
                if function(self, *args, **kwargs):
                    return
                if self.console.input(
                    _(
                        "如需重新尝试处理该对象，请关闭所有正在访问该对象的窗口或程序，然后直接按下回车键！\n"
                        "如需跳过处理该对象，请输入任意字符后按下回车键！"
                    ),
                ):
                    return

        return inner

    @staticmethod
    def retry_infinite(function):
        def inner(self, *args, **kwargs):
            while True:
                if function(self, *args, **kwargs):
                    return
                self.console.input(
                    _("请关闭所有正在访问该对象的窗口或程序，然后按下回车键继续处理！")
                )

        return inner
