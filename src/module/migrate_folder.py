from shutil import move
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..config import Parameter


class MigrateFolder:
    def __init__(
        self,
        parameter: "Parameter",
    ):
        self.ROOT = parameter.ROOT
        self.root = parameter.root
        self.folder = parameter.folder_name

    def compatible(self):
        for i in (
            "Music",
            "Data",
            "Live",
        ):
            if (old := self.ROOT.parent.joinpath(i)).exists() and not (
                new_ := self.ROOT.joinpath(i)
            ).exists():
                move(old, new_)
        if self.ROOT != self.root:
            return
        if (old := self.ROOT.parent.joinpath(self.folder)).exists() and not (
            new_ := self.ROOT.joinpath(self.folder)
        ).exists():
            move(old, new_)
        folders = self.ROOT.parent.iterdir()
        for i in folders:
            if not i.is_dir():
                continue
            if len(i.name) > 10 and i.name[1:3] == "ID":
                move(i, self.ROOT.joinpath(i.name))
