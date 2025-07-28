from rich.console import Console
from rich.text import Text

from src.custom import (
    PROMPT,
    GENERAL,
    INFO,
    WARNING,
    ERROR,
    DEBUG,
)

__all__ = ["ColorfulConsole"]


class ColorfulConsole(Console):
    def __init__(self, *args, debug: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.debug_mode = debug

    def print(self, *args, style=GENERAL, highlight=False, **kwargs):
        super().print(*args, style=style, highlight=highlight, **kwargs)

    def info(self, *args, highlight=False, **kwargs):
        self.print(*args, style=INFO, highlight=highlight, **kwargs)

    def warning(self, *args, highlight=False, **kwargs):
        self.print(*args, style=WARNING, highlight=highlight, **kwargs)

    def error(self, *args, highlight=False, **kwargs):
        self.print(*args, style=ERROR, highlight=highlight, **kwargs)

    def debug(self, *args, highlight=False, **kwargs):
        if self.debug_mode:
            self.print(*args, style=DEBUG, highlight=highlight, **kwargs)

    def input(self, prompt="", style=PROMPT, *args, **kwargs):
        try:
            return super().input(Text(prompt, style=style), *args, **kwargs)
        except EOFError as e:
            raise KeyboardInterrupt from e
