"""
emoji.core
~~~~~~~~~~

Core components for emoji.

"""

import re
import unicodedata
import sys
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, Union

if sys.version_info < (3, 9):
    from typing_extensions import Literal, Match, TypedDict  # type: ignore
else:
    from typing import Literal, Match, TypedDict

from emoji import unicode_codes
from emoji.tokenizer import (
    Token,
    EmojiMatch,
    EmojiMatchZWJ,
    EmojiMatchZWJNonRGI,
    tokenize,
    filter_tokens,
)

__all__ = [
    'emojize',
    'demojize',
    'analyze',
    'config',
    'emoji_list',
    'distinct_emoji_list',
    'emoji_count',
    'replace_emoji',
    'is_emoji',
    'purely_emoji',
    'version',
    'Token',
    'EmojiMatch',
    'EmojiMatchZWJ',
    'EmojiMatchZWJNonRGI',
]

_DEFAULT_DELIMITER = ':'
# In Arabic language, the unicode character "\u0655" should be kept so we add it to the pattern below
_EMOJI_NAME_PATTERN = '\\w\\-&.’”“()!#*+,/«»\u0300\u0301\u0302\u0303\u0306\u0308\u030a\u0327\u064b\u064e\u064f\u0650\u0653\u0654\u3099\u30fb\u309a\u0655'


class _EmojiListReturn(TypedDict):
    emoji: str
    match_start: int
    match_end: int


class config:
    """Module-wide configuration"""

    demojize_keep_zwj = True
    """Change the behavior of :func:`emoji.demojize()` regarding
    zero-width-joiners (ZWJ/``\\u200D``) in emoji that are not
    "recommended for general interchange" (non-RGI).
    It has no effect on RGI emoji.

    For example this family emoji with different skin tones "👨‍👩🏿‍👧🏻‍👦🏾" contains four
    person emoji that are joined together by three ZWJ characters:
    ``👨\\u200D👩🏿\\u200D👧🏻\\u200D👦🏾``

    If ``True``, the zero-width-joiners will be kept and :func:`emoji.emojize()` can
    reverse the :func:`emoji.demojize()` operation:
    ``emoji.emojize(emoji.demojize(s)) == s``

    The example emoji would be converted to
    ``:man:\\u200d:woman_dark_skin_tone:\\u200d:girl_light_skin_tone:\\u200d:boy_medium-dark_skin_tone:``

    If ``False``, the zero-width-joiners will be removed and :func:`emoji.emojize()`
    can only reverse the individual emoji: ``emoji.emojize(emoji.demojize(s)) != s``

    The example emoji would be converted to
    ``:man::woman_dark_skin_tone::girl_light_skin_tone::boy_medium-dark_skin_tone:``
    """

    replace_emoji_keep_zwj = False
    """Change the behavior of :func:`emoji.replace_emoji()` regarding
    zero-width-joiners (ZWJ/``\\u200D``) in emoji that are not
    "recommended for general interchange" (non-RGI).
    It has no effect on RGI emoji.

    See :attr:`config.demojize_keep_zwj` for more information.
    """

    @staticmethod
    def load_language(language: Union[List[str], str, None] = None):
        """Load one or multiple languages into memory.
        If no language is specified, all languages will be loaded.

        This makes language data accessible in the :data:`EMOJI_DATA` dict.
        For example to access a French emoji name, first load French with

         ``emoji.config.load_language('fr')``

        and then access it with

         ``emoji.EMOJI_DATA['🏄']['fr']``

        Available languages are listed in :data:`LANGUAGES`"""

        languages = (
            [language]
            if isinstance(language, str)
            else language
            if language
            else unicode_codes.LANGUAGES
        )

        for lang in languages:
            unicode_codes.load_from_json(lang)


def emojize(
    string: str,
    delimiters: Tuple[str, str] = (_DEFAULT_DELIMITER, _DEFAULT_DELIMITER),
    variant: Optional[Literal['text_type', 'emoji_type']] = None,
    language: str = 'en',
    version: Optional[float] = None,
    handle_version: Optional[Union[str, Callable[[str, Dict[str, str]], str]]] = None,
) -> str:
    """
    Replace emoji names in a string with Unicode codes.
        >>> import emoji
        >>> print(emoji.emojize("Python is fun :thumbsup:", language='alias'))
        Python is fun 👍
        >>> print(emoji.emojize("Python is fun :thumbs_up:"))
        Python is fun 👍
        >>> print(emoji.emojize("Python is fun {thumbs_up}", delimiters = ("{", "}")))
        Python is fun 👍
        >>> print(emoji.emojize("Python is fun :red_heart:", variant="text_type"))
        Python is fun ❤
        >>> print(emoji.emojize("Python is fun :red_heart:", variant="emoji_type"))
        Python is fun ❤️ # red heart, not black heart

    :param string: String contains emoji names.
    :param delimiters: (optional) Use delimiters other than _DEFAULT_DELIMITER. Each delimiter
        should contain at least one character that is not part of a-zA-Z0-9 and ``_-&.()!?#*+,``.
        See ``emoji.core._EMOJI_NAME_PATTERN`` for the regular expression of unsafe characters.
    :param variant: (optional) Choose variation selector between "base"(None), VS-15 ("text_type") and VS-16 ("emoji_type")
    :param language: Choose language of emoji name: language code 'es', 'de', etc. or 'alias'
        to use English aliases
    :param version: (optional) Max version. If set to an Emoji Version,
        all emoji above this version will be ignored.
    :param handle_version: (optional) Replace the emoji above ``version``
        instead of ignoring it. handle_version can be either a string or a
        callable; If it is a callable, it's passed the Unicode emoji and the
        data dict from :data:`EMOJI_DATA` and must return a replacement string
        to be used::

            handle_version('\\U0001F6EB', {
                'en' : ':airplane_departure:',
                'status' : fully_qualified,
                'E' : 1,
                'alias' : [':flight_departure:'],
                'de': ':abflug:',
                'es': ':avión_despegando:',
                ...
            })

    :raises ValueError: if ``variant`` is neither None, 'text_type' or 'emoji_type'

    """

    unicode_codes.load_from_json(language)

    pattern = re.compile(
        '(%s[%s]+%s)'
        % (re.escape(delimiters[0]), _EMOJI_NAME_PATTERN, re.escape(delimiters[1]))
    )

    def replace(match: Match[str]) -> str:
        name = match.group(1)[len(delimiters[0]) : -len(delimiters[1])]
        emj = unicode_codes.get_emoji_by_name(
            _DEFAULT_DELIMITER
            + unicodedata.normalize('NFKC', name)
            + _DEFAULT_DELIMITER,
            language,
        )

        if emj is None:
            return match.group(1)

        if version is not None and unicode_codes.EMOJI_DATA[emj]['E'] > version:
            if callable(handle_version):
                emj_data = unicode_codes.EMOJI_DATA[emj].copy()
                emj_data['match_start'] = match.start()
                emj_data['match_end'] = match.end()
                return handle_version(emj, emj_data)

            elif handle_version is not None:
                return str(handle_version)
            else:
                return ''

        if variant is None or 'variant' not in unicode_codes.EMOJI_DATA[emj]:
            return emj

        if emj[-1] == '\ufe0e' or emj[-1] == '\ufe0f':
            # Remove an existing variant
            emj = emj[0:-1]
        if variant == 'text_type':
            return emj + '\ufe0e'
        elif variant == 'emoji_type':
            return emj + '\ufe0f'
        else:
            raise ValueError(
                "Parameter 'variant' must be either None, 'text_type' or 'emoji_type'"
            )

    return pattern.sub(replace, string)


def analyze(
    string: str, non_emoji: bool = False, join_emoji: bool = True
) -> Iterator[Token]:
    """
    Find unicode emoji in a string. Yield each emoji as a named tuple
    :class:`Token` ``(chars, EmojiMatch)`` or :class:`Token` ``(chars, EmojiMatchZWJNonRGI)``.
    If ``non_emoji`` is True, also yield all other characters as
    :class:`Token` ``(char, char)`` .

    :param string: String to analyze
    :param non_emoji: If True also yield all non-emoji characters as Token(char, char)
    :param join_emoji: If True, multiple EmojiMatch are merged into a single
        EmojiMatchZWJNonRGI if they are separated only by a ZWJ.
    """

    return filter_tokens(
        tokenize(string, keep_zwj=True), emoji_only=not non_emoji, join_emoji=join_emoji
    )


def demojize(
    string: str,
    delimiters: Tuple[str, str] = (_DEFAULT_DELIMITER, _DEFAULT_DELIMITER),
    language: str = 'en',
    version: Optional[float] = None,
    handle_version: Optional[Union[str, Callable[[str, Dict[str, str]], str]]] = None,
) -> str:
    """
    Replace Unicode emoji in a string with emoji shortcodes. Useful for storage.
        >>> import emoji
        >>> print(emoji.emojize("Python is fun :thumbs_up:"))
        Python is fun 👍
        >>> print(emoji.demojize("Python is fun 👍"))
        Python is fun :thumbs_up:
        >>> print(emoji.demojize("icode is tricky 😯", delimiters=("__", "__")))
        Unicode is tricky __hushed_face__

    :param string: String contains Unicode characters. MUST BE UNICODE.
    :param delimiters: (optional) User delimiters other than ``_DEFAULT_DELIMITER``
    :param language: Choose language of emoji name: language code 'es', 'de', etc. or 'alias'
        to use English aliases
    :param version: (optional) Max version. If set to an Emoji Version,
        all emoji above this version will be removed.
    :param handle_version: (optional) Replace the emoji above ``version``
        instead of removing it. handle_version can be either a string or a
        callable ``handle_version(emj: str, data: dict) -> str``; If it is
        a callable, it's passed the Unicode emoji and the data dict from
        :data:`EMOJI_DATA` and must return a replacement string  to be used.
        The passed data is in the form of::

            handle_version('\\U0001F6EB', {
                'en' : ':airplane_departure:',
                'status' : fully_qualified,
                'E' : 1,
                'alias' : [':flight_departure:'],
                'de': ':abflug:',
                'es': ':avión_despegando:',
                ...
            })

    """

    if language == 'alias':
        language = 'en'
        _use_aliases = True
    else:
        _use_aliases = False

    unicode_codes.load_from_json(language)

    def handle(emoji_match: EmojiMatch) -> str:
        assert emoji_match.data is not None
        if version is not None and emoji_match.data['E'] > version:
            if callable(handle_version):
                return handle_version(emoji_match.emoji, emoji_match.data_copy())
            elif handle_version is not None:
                return handle_version
            else:
                return ''
        elif language in emoji_match.data:
            if _use_aliases and 'alias' in emoji_match.data:
                return (
                    delimiters[0] + emoji_match.data['alias'][0][1:-1] + delimiters[1]
                )
            else:
                return delimiters[0] + emoji_match.data[language][1:-1] + delimiters[1]
        else:
            # The emoji exists, but it is not translated, so we keep the emoji
            return emoji_match.emoji

    matches = tokenize(string, keep_zwj=config.demojize_keep_zwj)
    return ''.join(
        str(handle(token.value)) if isinstance(token.value, EmojiMatch) else token.value
        for token in matches
    )


def replace_emoji(
    string: str,
    replace: Union[str, Callable[[str, Dict[str, str]], str]] = '',
    version: float = -1,
) -> str:
    """
    Replace Unicode emoji in a customizable string.

    :param string: String contains Unicode characters. MUST BE UNICODE.
    :param replace: (optional) replace can be either a string or a callable;
        If it is a callable, it's passed the Unicode emoji and the data dict from
        :data:`EMOJI_DATA` and must return a replacement string to be used.
        replace(str, dict) -> str
    :param version: (optional) Max version. If set to an Emoji Version,
        only emoji above this version will be replaced.
    """

    def handle(emoji_match: EmojiMatch) -> str:
        if version > -1:
            assert emoji_match.data is not None
            if emoji_match.data['E'] > version:
                if callable(replace):
                    return replace(emoji_match.emoji, emoji_match.data_copy())
                else:
                    return str(replace)
        elif callable(replace):
            return replace(emoji_match.emoji, emoji_match.data_copy())
        elif replace is not None:  # type: ignore
            return replace
        return emoji_match.emoji

    matches = tokenize(string, keep_zwj=config.replace_emoji_keep_zwj)
    if config.replace_emoji_keep_zwj:
        matches = filter_tokens(matches, emoji_only=False, join_emoji=True)
    return ''.join(
        str(handle(m.value)) if isinstance(m.value, EmojiMatch) else m.value
        for m in matches
    )


def emoji_list(string: str) -> List[_EmojiListReturn]:
    """
    Returns the location and emoji in list of dict format.
        >>> emoji.emoji_list("Hi, I am fine. 😁")
        [{'match_start': 15, 'match_end': 16, 'emoji': '😁'}]
    """

    return [
        {
            'match_start': m.value.start,
            'match_end': m.value.end,
            'emoji': m.value.emoji,
        }
        for m in tokenize(string, keep_zwj=False)
        if isinstance(m.value, EmojiMatch)
    ]


def distinct_emoji_list(string: str) -> List[str]:
    """Returns distinct list of emojis from the string."""
    distinct_list = list({e['emoji'] for e in emoji_list(string)})
    return distinct_list


def emoji_count(string: str, unique: bool = False) -> int:
    """
    Returns the count of emojis in a string.

    :param unique: (optional) True if count only unique emojis
    """
    if unique:
        return len(distinct_emoji_list(string))
    return len(emoji_list(string))


def is_emoji(string: str) -> bool:
    """
    Returns True if the string is a single emoji, and it is "recommended for
    general interchange" by Unicode.org.
    """
    return string in unicode_codes.EMOJI_DATA


def purely_emoji(string: str) -> bool:
    """
    Returns True if the string contains only emojis.
    This might not imply that `is_emoji` for all the characters, for example,
    if the string contains variation selectors.
    """
    return all(isinstance(m.value, EmojiMatch) for m in analyze(string, non_emoji=True))


def version(string: str) -> float:
    """
    Returns the Emoji Version of the emoji.

    See https://www.unicode.org/reports/tr51/#Versioning for more information.
        >>> emoji.version("😁")
        0.6
        >>> emoji.version(":butterfly:")
        3

    :param string: An emoji or a text containing an emoji
    :raises ValueError: if ``string`` does not contain an emoji
    """
    # Try dictionary lookup
    if string in unicode_codes.EMOJI_DATA:
        return unicode_codes.EMOJI_DATA[string]['E']

    # Try name lookup
    emj_code = unicode_codes.get_emoji_by_name(string, 'en')
    if emj_code and emj_code in unicode_codes.EMOJI_DATA:
        return unicode_codes.EMOJI_DATA[emj_code]['E']

    # Try to find first emoji in string
    version: List[float] = []

    def f(e: str, emoji_data: Dict[str, Any]) -> str:
        version.append(emoji_data['E'])
        return ''

    replace_emoji(string, replace=f, version=-1)
    if version:
        return version[0]
    emojize(string, language='alias', version=-1, handle_version=f)
    if version:
        return version[0]
    for lang_code in unicode_codes.LANGUAGES:
        emojize(string, language=lang_code, version=-1, handle_version=f)
        if version:
            return version[0]

    raise ValueError('No emoji found in string')
