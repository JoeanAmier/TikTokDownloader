from gettext import translation
from locale import getlocale
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


class TranslationManager:
    """管理gettext翻译的类"""

    _instance = None  # 单例实例

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TranslationManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, domain="tk", localedir=None):
        self.domain = domain
        if not localedir:
            localedir = ROOT.joinpath("locale")
        self.localedir = Path(localedir)
        self.current_translator = self.setup_translation(
            self.get_language_code(),
        )

    @staticmethod
    def get_language_code() -> str:
        # 获取当前系统的语言和区域设置
        language_code, __ = getlocale()
        if not language_code:
            return "en_US"
        return (
            "zh_CN"
            if any(
                s in language_code.upper()
                for s in (
                    "CHINESE",
                    "ZH",
                    "CHINA",
                )
            )
            else "en_US"
        )

    def setup_translation(self, language: str = "zh_CN"):
        """设置gettext翻译环境"""
        try:
            return translation(
                self.domain,
                localedir=self.localedir,
                languages=[language],
                fallback=True,
            )
        except FileNotFoundError as e:
            print(
                f"Warning: Translation files for '{self.domain}' not found. Error: {e}"
            )
            return translation(self.domain, fallback=True)

    def switch_language(self, language: str = "en_US"):
        """切换当前使用的语言"""
        self.current_translator = self.setup_translation(language)

    def gettext(self, message):
        """提供gettext方法"""
        return self.current_translator.gettext(message)


# 初始化TranslationManager单例实例
translation_manager = TranslationManager()


def _translate(message):
    """辅助函数来简化翻译调用"""
    return translation_manager.gettext(message)


def switch_language(language: str = "en_US"):
    """切换语言并刷新翻译函数"""
    global _
    translation_manager.switch_language(language)
    _ = translation_manager.gettext


# 设置默认翻译函数
_ = _translate
