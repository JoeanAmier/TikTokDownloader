"""
emoji.tokenizer
~~~~~~~~~~~~~~~

Components for detecting and tokenizing emoji in strings.

"""

from typing import List, NamedTuple, Dict, Union, Iterator, Any
from emoji import unicode_codes


__all__ = [
    'EmojiMatch',
    'EmojiMatchZWJ',
    'EmojiMatchZWJNonRGI',
    'Token',
    'tokenize',
    'filter_tokens',
]

_ZWJ = '\u200d'
_SEARCH_TREE: Dict[str, Any] = {}


class EmojiMatch:
    """
    Represents a match of a "recommended for general interchange" (RGI)
    emoji in a string.
    """

    __slots__ = ('emoji', 'start', 'end', 'data')

    def __init__(
        self, emoji: str, start: int, end: int, data: Union[Dict[str, Any], None]
    ):
        self.emoji = emoji
        """The emoji substring"""

        self.start = start
        """The start index of the match in the string"""

        self.end = end
        """The end index of the match in the string"""

        self.data = data
        """The entry from :data:`EMOJI_DATA` for this emoji or ``None`` if the emoji is non-RGI"""

    def data_copy(self) -> Dict[str, Any]:
        """
        Returns a copy of the data from :data:`EMOJI_DATA` for this match
        with the additional keys ``match_start`` and ``match_end``.
        """
        if self.data:
            emj_data = self.data.copy()
            emj_data['match_start'] = self.start
            emj_data['match_end'] = self.end
            return emj_data
        else:
            return {'match_start': self.start, 'match_end': self.end}

    def is_zwj(self) -> bool:
        """
        Checks if this is a ZWJ-emoji.

        :returns: True if this is a ZWJ-emoji, False otherwise
        """

        return _ZWJ in self.emoji

    def split(self) -> Union['EmojiMatchZWJ', 'EmojiMatch']:
        """
        Splits a ZWJ-emoji into its constituents.

        :returns: An :class:`EmojiMatchZWJ` containing the "sub-emoji" if this is a ZWJ-emoji, otherwise self
        """

        if self.is_zwj():
            return EmojiMatchZWJ(self)
        else:
            return self

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.emoji}, {self.start}:{self.end})'


class EmojiMatchZWJ(EmojiMatch):
    """
    Represents a match of multiple emoji in a string that were joined by
    zero-width-joiners (ZWJ/``\\u200D``)."""

    __slots__ = ('emojis',)

    def __init__(self, match: EmojiMatch):
        super().__init__(match.emoji, match.start, match.end, match.data)

        self.emojis: List[EmojiMatch] = []
        """List of sub emoji as EmojiMatch objects"""

        i = match.start
        for e in match.emoji.split(_ZWJ):
            m = EmojiMatch(e, i, i + len(e), unicode_codes.EMOJI_DATA.get(e, None))
            self.emojis.append(m)
            i += len(e) + 1

    def join(self) -> str:
        """
        Joins a ZWJ-emoji into a string
        """

        return _ZWJ.join(e.emoji for e in self.emojis)

    def is_zwj(self) -> bool:
        return True

    def split(self) -> 'EmojiMatchZWJ':
        return self

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.join()}, {self.start}:{self.end})'


class EmojiMatchZWJNonRGI(EmojiMatchZWJ):
    """
    Represents a match of multiple emoji in a string that were joined by
    zero-width-joiners (ZWJ/``\\u200D``). This class is only used for emoji
    that are not "recommended for general interchange" (non-RGI) by Unicode.org.
    The data property of this class is always None.
    """

    def __init__(self, first_emoji_match: EmojiMatch, second_emoji_match: EmojiMatch):
        self.emojis = [first_emoji_match, second_emoji_match]
        """List of sub emoji as EmojiMatch objects"""

        self._update()

    def _update(self):
        self.emoji = _ZWJ.join(e.emoji for e in self.emojis)
        self.start = self.emojis[0].start
        self.end = self.emojis[-1].end
        self.data = None

    def _add(self, next_emoji_match: EmojiMatch):
        self.emojis.append(next_emoji_match)
        self._update()


class Token(NamedTuple):
    """
    A named tuple containing the matched string and its :class:`EmojiMatch` object if it is an emoji
    or a single character that is not a unicode emoji.
    """

    chars: str
    value: Union[str, EmojiMatch]


def tokenize(string: str, keep_zwj: bool) -> Iterator[Token]:
    """
    Finds unicode emoji in a string. Yields all normal characters as a named
    tuple :class:`Token` ``(char, char)`` and all emoji as :class:`Token` ``(chars, EmojiMatch)``.

    :param string: String contains unicode characters. MUST BE UNICODE.
    :param keep_zwj: Should ZWJ-characters (``\\u200D``) that join non-RGI emoji be
        skipped or should be yielded as normal characters
    :return: An iterable of tuples :class:`Token` ``(char, char)`` or :class:`Token` ``(chars, EmojiMatch)``
    """

    tree = get_search_tree()
    EMOJI_DATA = unicode_codes.EMOJI_DATA
    # result: [ Token(oldsubstring0, EmojiMatch), Token(char1, char1), ... ]
    result: List[Token] = []
    i = 0
    length = len(string)
    ignore: List[
        int
    ] = []  # index of chars in string that are skipped, i.e. the ZWJ-char in non-RGI-ZWJ-sequences
    while i < length:
        consumed = False
        char = string[i]
        if i in ignore:
            i += 1
            if char == _ZWJ and keep_zwj:
                result.append(Token(char, char))
            continue

        elif char in tree:
            j = i + 1
            sub_tree = tree[char]
            while j < length and string[j] in sub_tree:
                if j in ignore:
                    break
                sub_tree = sub_tree[string[j]]
                j += 1
            if 'data' in sub_tree:
                emj_data = sub_tree['data']
                code_points = string[i:j]

                # We cannot yield the result here, we need to defer
                # the call until we are sure that the emoji is finished
                # i.e. we're not inside an ongoing ZWJ-sequence
                match_obj = EmojiMatch(code_points, i, j, emj_data)

                i = j - 1
                consumed = True
                result.append(Token(code_points, match_obj))

        elif (
            char == _ZWJ
            and result
            and result[-1].chars in EMOJI_DATA
            and i > 0
            and string[i - 1] in tree
        ):
            # the current char is ZWJ and the last match was an emoji
            ignore.append(i)
            if (
                EMOJI_DATA[result[-1].chars]['status']
                == unicode_codes.STATUS['component']
            ):
                # last match was a component, it could be ZWJ+EMOJI+COMPONENT
                # or ZWJ+COMPONENT
                i = i - sum(len(t.chars) for t in result[-2:])
                if string[i] == _ZWJ:
                    # It's ZWJ+COMPONENT, move one back
                    i += 1
                    del result[-1]
                else:
                    # It's ZWJ+EMOJI+COMPONENT, move two back
                    del result[-2:]
            else:
                # last match result[-1] was a normal emoji, move cursor
                # before the emoji
                i = i - len(result[-1].chars)
                del result[-1]
            continue

        elif result:
            yield from result
            result = []

        if not consumed and char != '\ufe0e' and char != '\ufe0f':
            result.append(Token(char, char))
        i += 1

    yield from result


def filter_tokens(
    matches: Iterator[Token], emoji_only: bool, join_emoji: bool
) -> Iterator[Token]:
    """
    Filters the output of `tokenize()`

    :param matches: An iterable of tuples of the form ``(match_str, result)``
        where ``result`` is either an EmojiMatch or a string.
    :param emoji_only: If True, only EmojiMatch are returned in the output.
        If False all characters are returned
    :param join_emoji: If True, multiple EmojiMatch are merged into
        a single :class:`EmojiMatchZWJNonRGI` if they are separated only by a ZWJ.

    :return: An iterable of tuples :class:`Token` ``(char, char)``,
        :class:`Token` ``(chars, EmojiMatch)`` or :class:`Token` ``(chars, EmojiMatchZWJNonRGI)``
    """

    if not join_emoji and not emoji_only:
        yield from matches
        return

    if not join_emoji:
        for token in matches:
            if token.chars != _ZWJ:
                yield token
        return

    # Combine multiple EmojiMatch that are separated by ZWJs into
    # a single EmojiMatchZWJNonRGI
    previous_is_emoji = False
    previous_is_zwj = False
    pre_previous_is_emoji = False
    accumulator: List[Token] = []
    for token in matches:
        pre_previous_is_emoji = previous_is_emoji
        if previous_is_emoji and token.value == _ZWJ:
            previous_is_zwj = True
        elif isinstance(token.value, EmojiMatch):
            if pre_previous_is_emoji and previous_is_zwj:
                if isinstance(accumulator[-1].value, EmojiMatchZWJNonRGI):
                    accumulator[-1].value._add(token.value)  # pyright: ignore [reportPrivateUsage]
                    accumulator[-1] = Token(
                        accumulator[-1].chars + _ZWJ + token.chars,
                        accumulator[-1].value,
                    )
                else:
                    prev = accumulator.pop()
                    assert isinstance(prev.value, EmojiMatch)
                    accumulator.append(
                        Token(
                            prev.chars + _ZWJ + token.chars,
                            EmojiMatchZWJNonRGI(prev.value, token.value),
                        )
                    )
            else:
                accumulator.append(token)
            previous_is_emoji = True
            previous_is_zwj = False
        else:
            # Other character, not an emoji
            previous_is_emoji = False
            previous_is_zwj = False
            yield from accumulator
            if not emoji_only:
                yield token
            accumulator = []
    yield from accumulator


def get_search_tree() -> Dict[str, Any]:
    """
    Generate a search tree for demojize().
    Example of a search tree::

        EMOJI_DATA =
        {'a': {'en': ':Apple:'},
        'b': {'en': ':Bus:'},
        'ba': {'en': ':Bat:'},
        'band': {'en': ':Beatles:'},
        'bandit': {'en': ':Outlaw:'},
        'bank': {'en': ':BankOfEngland:'},
        'bb': {'en': ':BB-gun:'},
        'c': {'en': ':Car:'}}

        _SEARCH_TREE =
        {'a': {'data': {'en': ':Apple:'}},
        'b': {'a': {'data': {'en': ':Bat:'},
                    'n': {'d': {'data': {'en': ':Beatles:'},
                                'i': {'t': {'data': {'en': ':Outlaw:'}}}},
                        'k': {'data': {'en': ':BankOfEngland:'}}}},
            'b': {'data': {'en': ':BB-gun:'}},
            'data': {'en': ':Bus:'}},
        'c': {'data': {'en': ':Car:'}}}

                   _SEARCH_TREE
                 /     |        ⧵
               /       |          ⧵
            a          b             c
            |        / |  ⧵          |
            |       /  |    ⧵        |
        :Apple:   ba  :Bus:  bb     :Car:
                 /  ⧵         |
                /    ⧵        |
              :Bat:    ban     :BB-gun:
                     /     ⧵
                    /       ⧵
                 band       bank
                /   ⧵         |
               /     ⧵        |
            bandi :Beatles:  :BankOfEngland:
               |
            bandit
               |
           :Outlaw:


    """
    if not _SEARCH_TREE:
        for emj in unicode_codes.EMOJI_DATA:
            sub_tree = _SEARCH_TREE
            lastidx = len(emj) - 1
            for i, char in enumerate(emj):
                if char not in sub_tree:
                    sub_tree[char] = {}
                sub_tree = sub_tree[char]
                if i == lastidx:
                    sub_tree['data'] = unicode_codes.EMOJI_DATA[emj]
    return _SEARCH_TREE
