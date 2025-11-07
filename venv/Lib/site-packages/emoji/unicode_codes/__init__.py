import sys
import importlib.resources
import json
from functools import lru_cache
from warnings import warn

from typing import Any, BinaryIO, Dict, List, Optional

from emoji.unicode_codes.data_dict import STATUS, LANGUAGES

__all__ = [
    'get_emoji_by_name',
    'load_from_json',
    'EMOJI_DATA',
    'STATUS',
    'LANGUAGES',
]

_DEFAULT_KEYS = ('en', 'alias', 'E', 'status')  # The keys in emoji.json

_loaded_keys: List[str] = list(
    _DEFAULT_KEYS
)  # Keep track of keys already loaded from json files to avoid loading them twice


@lru_cache(maxsize=4000)
def get_emoji_by_name(name: str, language: str) -> Optional[str]:
    """
    Find emoji by short-name in a specific language.
    Returns None if not found

    :param name: emoji short code e.g. ":banana:"
    :param language: language-code e.g. 'es', 'de', etc. or 'alias'
    """

    fully_qualified = STATUS['fully_qualified']

    if language == 'alias':
        for emj, data in EMOJI_DATA.items():
            if name in data.get('alias', []) and data['status'] <= fully_qualified:
                return emj
        language = 'en'

    for emj, data in EMOJI_DATA.items():
        if data.get(language) == name and data['status'] <= fully_qualified:
            return emj

    return None


class EmojiDataDict(Dict[str, Any]):
    """Replaces built-in-dict in the values of the EMOJI_DATA dict.
    Auto loads language data when accessing language data via
    key-access without prior loading of the language:
    e.g. EMOJI_DATA['👌']['fr'] will auto load French language and not throw
    a KeyError.
    Shows a deprecation warning explainging that `emoji.config.load_language()`
    should be used."""

    def __missing__(self, key: str) -> str:
        """Auto load language `key`, raises KeyError if language is no supported."""
        if key in LANGUAGES and key not in _loaded_keys:
            load_from_json(key)
            if key in self:
                warn(
                    f"""Use emoji.config.load_language('{key}') before accesing EMOJI_DATA[emj]['{key}'].
Accessing EMOJI_DATA[emj]['{key}'] without loading the language is deprecated.""",
                    DeprecationWarning,
                    stacklevel=3,
                )
                return self[key]  # type: ignore

        raise KeyError(key)


EMOJI_DATA: Dict[str, Dict[str, Any]]


def _open_file(name: str) -> BinaryIO:
    if sys.version_info >= (3, 9):
        return importlib.resources.files('emoji.unicode_codes').joinpath(name).open('rb')
    else:
        return importlib.resources.open_binary('emoji.unicode_codes', name)


def _load_default_from_json():
    global EMOJI_DATA
    global _loaded_keys

    with _open_file('emoji.json') as f:
        EMOJI_DATA = dict(json.load(f, object_pairs_hook=EmojiDataDict))  # type: ignore
    _loaded_keys = list(_DEFAULT_KEYS)


def load_from_json(key: str):
    """Load values from the file 'emoji_{key}.json' into EMOJI_DATA"""

    if key in _loaded_keys:
        return

    if key not in LANGUAGES:
        raise NotImplementedError('Language not supported', key)

    with _open_file(f'emoji_{key}.json') as f:
        for emj, value in json.load(f).items():
            EMOJI_DATA[emj][key] = value  # type: ignore

    _loaded_keys.append(key)


_load_default_from_json()
