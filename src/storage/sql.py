from re import Pattern
from re import compile

from .text import BaseTextLogger

__all__ = ["BaseSQLLogger"]


class BaseSQLLogger(BaseTextLogger):
    SHEET_NAME: Pattern = compile(r"[^\u4e00-\u9fffa-zA-Z0-9_]")
    CHECK_SQL = "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?;"
    UPDATE_SQL = "ALTER TABLE ? RENAME TO ?;"
