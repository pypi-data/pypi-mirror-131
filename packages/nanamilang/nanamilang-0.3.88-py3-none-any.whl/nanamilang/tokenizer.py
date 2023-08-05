"""NanamiLang Tokenizer Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

import datetime
import re
from typing import List

from nanamilang.shortcuts import (
    ASSERT_IS_INSTANCE_OF,
    ASSERT_COLLECTION_IS_NOT_EMPTY,
    UNTERMINATED_SYMBOL, UNTERMINATED_SYMBOL_AT_EOF
)
from nanamilang.token import Token


class Tokenizer:
    """NanamiLang Tokenizer"""

    _date_pattern: str = r'^\d{4}-\d{2}-\d{2}$'
    _float_number_pattern: str = r'^-?\d+\.\d+$'
    _integer_number_pattern: str = r'^-?\d+$'
    _identifier_name_pattern: str = r'^\D\S*$'
    _binary_number_pattern: str = r'^[0-1]{8}$'
    _boolean_valid_values: list = ['true', 'false']

    _literal_characters: List[str] = ['!', '?', '$', '%',
                                      '*', '/', '+', '-',
                                      '=', '>', '<', '_', '.']

    _pointer: int = -1
    _source_view: List[str] = None

    def __init__(self, source: str) -> None:
        """
        Initialize a new NanamiLang Tokenizer instance

        :param source: your NanamiLang program source code
        """

        ASSERT_IS_INSTANCE_OF(source, str)
        ASSERT_COLLECTION_IS_NOT_EMPTY(source)

        self._source_view = list(source)

        # For some reason I'm still doing this, maybe its useless... :(

    def tokenize(self) -> List[Token]:
        """NanamiLang Tokenizer, return a Token instances collection"""

        tokenized: List[Token] = []

        self._pointer = -1

        while self._has_next_symbol():
            tokenized = tokenized + self._get_next_token()

        return tokenized or [Token(Token.Nil, 'nil')]

        # In case there are no tokens to return, just return [Token.Nil]

    def _value_dispatched_or_invalid(self, value: str) -> Token:
        """NanamiLang Tokenizer, try to dispatch value with a pattern"""

        if re.match(self._date_pattern, value):
            return Token(Token.Date,
                         datetime.datetime.fromisoformat(value))
        if re.match(self._float_number_pattern, value):
            return Token(Token.FloatNumber, float(value))
        if re.match(self._binary_number_pattern, value):
            return Token(Token.IntegerNumber, int(value, base=2))
        if re.match(self._integer_number_pattern, value):
            return Token(Token.IntegerNumber, int(value))
        if value in self._boolean_valid_values:
            return Token(Token.Boolean, value == 'true')
        if value == 'nil':
            return Token(Token.Nil, value)
        if re.match(self._identifier_name_pattern, value):
            return Token(Token.Identifier, value)

        return self._invalid_token_with_current_symbol('Unable to tokenize value')

    def _invalid_token_with_current_symbol(self, reason: str) -> Token:
        """NanamiLang Tokenizer, shortcut for returning Token.Invalid"""

        return Token(Token.Invalid,
                     _valid=False,
                     _reason=reason, _position=self._pointer, _raw_symbol=self._curr_symbol())

    def _get_next_token(self) -> List[Token]:
        """NanamiLang Tokenizer, try to match next symbol with a pattern"""

        self._pointer += 1

        # Matching a Token.ListBegin
        if self._curr_symbol() == '(':
            return [Token(Token.ListBegin)]
        # Lets inject comments handling here...
        if self._curr_symbol() == ';':
            while self._has_next_symbol():
                self._pointer += 1
                if self._curr_symbol() == '\n':
                    if self._has_next_symbol():
                        return self._get_next_token()
            return []
        # Matching a Token.ListEnd
        if self._curr_symbol() == ')':
            return [Token(Token.ListEnd)]
        # Matching a Token.ListBegin and Token.Identifier (make-vector)
        if self._curr_symbol() == '[':
            return [Token(Token.ListBegin), Token(Token.Identifier, 'make-vector')]
        # Matching a Token.ListEnd
        if self._curr_symbol() == ']':
            return [Token(Token.ListEnd)]
        # Matching a Token.ListBegin and Token.Identifier (make-hashmap)
        if self._curr_symbol() == '{':
            return [Token(Token.ListBegin), Token(Token.Identifier, 'make-hashmap')]
        # Matching a Token.ListEnd
        if self._curr_symbol() == '}':
            return [Token(Token.ListEnd)]
        # Matching a Token.ListBegin, Token.Identifier (make-set, comment) |
        # Matching a Token.Date
        if self._curr_sym_is('#'):
            if self._has_next_symbol():
                if self._next_sym_is('_'):
                    self._pointer += 1
                    return [Token(Token.ListBegin), Token(Token.Identifier, 'comment')]
                if self._next_sym_is('{'):
                    self._pointer += 1
                    return [Token(Token.ListBegin), Token(Token.Identifier, 'make-set')]
                if len(self._source_view[self._pointer:]) >= 11:
                    return self._get_next_token()
                return [self._invalid_token_with_current_symbol(UNTERMINATED_SYMBOL('#'))]
            return [self._invalid_token_with_current_symbol(UNTERMINATED_SYMBOL_AT_EOF('#'))]
        # Matching a Token.Keyword
        if self._curr_sym_is(':'):
            if self._has_next_symbol():
                if not self._next_sym_in([' ', '\t', '\n']):
                    value: str = ''
                    while self._has_next_symbol():
                        if self._next_sym_is_a_lit_character():
                            self._pointer += 1
                            value += self._curr_symbol()
                        else:
                            break
                    return [Token(Token.Keyword, value)]
                return [self._invalid_token_with_current_symbol(UNTERMINATED_SYMBOL('"'))]
            return [self._invalid_token_with_current_symbol(UNTERMINATED_SYMBOL_AT_EOF(':'))]
        # Matching a Token.String
        if self._curr_sym_is('"'):
            if self._has_next_symbol():
                value: str = ''
                while self._has_next_symbol():
                    if not self._next_sym_is('"'):
                        self._pointer += 1
                        value += self._curr_symbol()
                    else:
                        break
                self._pointer += 1
                return [Token(Token.String, value)]
            return [self._invalid_token_with_current_symbol(UNTERMINATED_SYMBOL_AT_EOF('"'))]
        # elif branch for matching anything else
        if self._curr_sym_is_a_lit_character():
            value: str = self._curr_symbol()
            while self._has_next_symbol():
                if self._next_sym_is_a_lit_character():
                    self._pointer += 1
                    value += self._curr_symbol()
                else:
                    break
            return [self._value_dispatched_or_invalid(value)]
        # Skip the whitespace symbol in case the source code has next symbol
        if self._curr_symbol() == ' ':
            if self._has_next_symbol():
                return self._get_next_token()
            return []
        # Skip the tabulation symbol in case the source code has next symbol
        if self._curr_symbol() == '\t':
            if self._has_next_symbol():
                return self._get_next_token()
            return []
        # Skip the  new line  symbol in case the source code has next symbol
        if self._curr_symbol() == '\n':
            if self._has_next_symbol():
                return self._get_next_token()
            return []
        # If we do not know what the current character is, we return Token.Invalid
        return [self._invalid_token_with_current_symbol('Has encountered an unknown character')]

    def _next_symbol(self) -> str:
        """NanamiLang Tokenizer, return the source view next symbol"""

        return self._source_view[self._pointer + 1]

    def _curr_symbol(self) -> str:
        """NanamiLang Tokenizer, return the source view current symbol"""

        return self._source_view[self._pointer]

    def _has_next_symbol(self) -> bool:
        """NanamiLang Tokenizer, does the source view have a next symbol?"""

        return self._pointer + 1 < len(self._source_view)

    def _next_sym_in(self, collection: List[str]) -> bool:
        """NanamiLang Tokenizer, does the next source view symbol in...?"""

        return self._next_symbol() in collection

    def _curr_sym_in(self, collection: List[str]) -> bool:
        """NanamiLang Tokenizer, does the next source view in ...?"""

        return self._curr_symbol() in collection

    def _next_sym_is(self, sym: str) -> bool:
        """NanamiLang Tokenizer, does the next source view symbol equal to...?"""

        return self._next_symbol() == sym

    def _curr_sym_is(self, sym: str) -> bool:
        """NanamiLang Tokenizer, does the current source view symbol equal to...?"""

        return self._curr_symbol() == sym

    def _next_sym_matches_with(self, sym_pattern: str) -> bool:
        """NanamiLang Tokenizer, does the next source view symbol match with ...?"""

        return bool(re.match(sym_pattern, self._next_symbol()))

    def _curr_sym_matches_with(self, sym_pattern: str) -> bool:
        """NanamiLang Tokenizer, does the current source view symbol match with ...?"""

        return bool(re.match(sym_pattern, self._curr_symbol()))

    def _next_sym_is_a_lit_character(self) -> bool:
        """NanamiLang Tokenizer, is the next source view symbol a valid literal character?"""

        return self._next_sym_matches_with(r'[a-z0-9]') or self._next_sym_in(self._literal_characters)

    def _curr_sym_is_a_lit_character(self) -> bool:
        """NanamiLang Tokenizer, is the current source view symbol a valid literal character?"""

        return self._curr_sym_matches_with(r'[a-z0-9]') or self._curr_sym_in(self._literal_characters)
