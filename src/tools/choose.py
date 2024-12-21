from typing import TYPE_CHECKING
from typing import Union

if TYPE_CHECKING:
    from src.tools import ColorfulConsole
    from rich.console import Console

__all__ = ["choose"]


def choose(
        title: str,
        options: tuple | list,
        console: Union["ColorfulConsole", "Console"],
        separate=None) -> str:
    screen = f"{title}:\n"
    row = 0
    for i, j in enumerate(options, start=1):
        screen += f"{i: >2d}. {j}\n"
        if separate and row in separate:
            screen += f"{'=' * 25}\n"
        row += 1
    return console.input(screen)
