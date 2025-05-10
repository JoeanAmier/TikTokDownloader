from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from rich.console import Console

    from src.tools import ColorfulConsole

__all__ = ["choose"]


def choose(
    title: str,
    options: tuple | list,
    console: Union["ColorfulConsole", "Console"],
    separate=None,
) -> str:
    screen = f"{title}:\n"
    for i, j in enumerate(options, start=1):
        screen += f"{i: >2d}. {j}\n"
        if separate and i in separate:
            screen += f"{'=' * 32}\n"
    return console.input(screen)
