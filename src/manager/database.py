from typing import TYPE_CHECKING

from aiosqlite import connect

if TYPE_CHECKING:
    from src.config import Parameter

__all__ = ["Database"]


class Database:
    __FILE = "TikTokDownloader.db"

    def __init__(self, parameter: "Parameter"):
        self.file = parameter.cache.joinpath(self.__FILE)
        self.database = None
        self.cursor = None

    async def __connect_database(self):
        self.database = await connect(self.file)
        self.cursor = await self.database.cursor()
        await self.__create_table()
        await self.__write_default_config()
        await self.database.commit()

    async def __create_table(self):
        await self.database.execute(
            """CREATE TABLE IF NOT EXISTS config_data (
            NAME TEXT PRIMARY KEY,
            VALUE INTEGER NOT NULL CHECK(VALUE IN (0, 1))
            );""")
        await self.database.execute("CREATE TABLE IF NOT EXISTS download_data (ID TEXT PRIMARY KEY);")
        await self.database.execute("""CREATE TABLE IF NOT EXISTS mapping_data (
        ID TEXT PRIMARY KEY,
        NAME TEXT NOT NULL,
        MARK TEXT NOT NULL
        );""")

    async def __write_default_config(self):
        await self.database.execute("""INSERT OR IGNORE INTO config_data (NAME, VALUE)
                            VALUES ('Update', 1),
                            ('Record', 1),
                            ('Log', 0),
                            ('Disclaimer', 0);""")

    async def read_config_data(self):
        await self.cursor.execute("SELECT * FROM config_data")
        return await self.cursor.fetchall()

    async def update_mapping_data(self, id_: str, name: str, mark: str):
        await self.database.execute("REPLACE INTO mapping_data (ID, NAME, MARK) VALUES (?,?,?)", (id_, name, mark))
        await self.database.commit()

    async def read_mapping_data(self, id_: str):
        await self.cursor.execute("SELECT * FROM mapping_data WHERE ID=?", (id_,))
        return await self.cursor.fetchone()

    async def write_download_data(self, ids: list[str]):
        await self.database.execute(f"INSERT OR IGNORE INTO download_data (ID) VALUES ({', '.join('?' for _ in ids)})",
                                    tuple(ids))
        await self.database.commit()

    async def delete_download_data(self, ids: list | tuple | str):
        if not ids:
            return
        if isinstance(ids, str):
            ids = [ids]
        [await self.__delete_download_data(i) for i in ids]
        await self.database.commit()

    async def __delete_download_data(self, id_: str):
        await self.cursor.execute("SELECT COUNT(ID) FROM download_data WHERE ID=?", (id_,))
        if self.cursor.fetchone()[0]:
            await self.database.execute("DELETE FROM download_data WHERE ID=?", (id_,))

    async def __aenter__(self):
        await self.__connect_database()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.cursor.close()
        await self.database.close()
