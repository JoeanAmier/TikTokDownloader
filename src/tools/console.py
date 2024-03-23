from rich.console import Console
from rich.text import Text

from src.custom import (
    PROMPT,
    GENERAL
)

__all__ = ["ColorfulConsole"]


class ColorfulConsole(Console):
    def print(self, *args, style=GENERAL, highlight=False, **kwargs):
        super().print(*args, style=style, highlight=highlight, **kwargs)

    def input(self, prompt="", style=PROMPT, *args, **kwargs):
        return super().input(
            Text(prompt, style=style), *args, **kwargs)
