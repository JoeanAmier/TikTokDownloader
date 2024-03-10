from pathlib import Path
from re import sub
from sqlite3 import connect

from .sql import BaseSQLLogger

__all__ = ["SQLLogger"]


class SQLLogger(BaseSQLLogger):
    """SQLite 数据库保存数据"""

    def __init__(
            self,
            root: Path,
            db_name: str,
            title_line: tuple,
            title_type: tuple,
            field_keys: tuple,
            old=None,
            name="Solo_Download",
            *args,
            **kwargs, ):
        super().__init__(*args, **kwargs)
        self.db = None  # 数据库
        self.cursor = None  # 游标对象
        self.name = (old, name)  # 数据表名称
        self.file = db_name  # 数据库文件名称
        self.path = root.joinpath(self.file)
        self.title_line = title_line  # 数据表列名
        self.title_type = title_type  # 数据表数据类型
        self.field_keys = field_keys

    def __enter__(self):
        self.db = connect(self.path)
        self.cursor = self.db.cursor()
        self.update_sheet()
        self.create()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def create(self):
        create_sql = f"""CREATE TABLE IF NOT EXISTS {self.name} ({", ".join(
            [f"{i} {j}" for i, j in zip(self.title_line, self.title_type)])});"""
        self.cursor.execute(create_sql)
        self.db.commit()

    def save(self, data, *args, **kwargs):
        insert_sql = f"""REPLACE INTO {self.name} ({", ".join(self.title_line)}) VALUES ({
        ", ".join(["?" for _ in self.title_line])});"""
        self.cursor.execute(insert_sql, data)
        self.db.commit()

    def update_sheet(self):
        old_sheet, new_sheet = self.__clean_sheet_name(self.name)
        mark = new_sheet.split("_", 1)
        if not old_sheet or mark[-1] == old_sheet:
            self.name = new_sheet
            return
        mark[-1] = old_sheet
        old_sheet = "_".join(mark)
        if self.__check_sheet_exists(old_sheet):
            self.cursor.execute(self.UPDATE_SQL, (old_sheet, new_sheet))
            self.db.commit()
        self.name = new_sheet

    def __check_sheet_exists(self, sheet: str) -> bool:
        self.cursor.execute(self.CHECK_SQL, (sheet,))
        exists = self.cursor.fetchone()
        return exists[0] > 0

    def __clean_sheet_name(self, name: tuple) -> tuple:
        return self.__clean_characters(
            name[0]), self.__clean_characters(
            name[1])

    def __clean_characters(self, text: str | None) -> str | None:
        if isinstance(text, str):
            text = self.SHEET_NAME.sub("_", text)
            text = sub(r"_+", "_", text)
        return text
