from json import dump
from json import load
from pathlib import Path
from platform import system

from src.config import Settings

SETTING_ROOT = Path(__file__).parent.joinpath("settings.json")
ENCODE = "UTF-8-SIG" if system() == "Windows" else "UTF-8"


def update_params():
    with SETTING_ROOT.open("r+", encoding=ENCODE) as f:
        old_data = load(f)
        new_data = Settings.default | old_data
        dump(new_data, f, indent=4, ensure_ascii=False)
