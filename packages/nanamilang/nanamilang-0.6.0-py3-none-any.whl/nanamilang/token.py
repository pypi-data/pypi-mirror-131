"""NanamiLang Token Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from typing import List

from nanamilang import datatypes
from nanamilang.builtin import (
    BuiltinFunctions, BuiltinMacros
)
from nanamilang.shortcuts import (
    ASSERT_COLL_CONTAINS_ELEMENT,
    ASSERT_IS_INSTANCE_OF, ASSERT_COLLECTION_IS_NOT_EMPTY
)


class Token:
    """NanamiLang Token"""

    _type: str = None
    _valid: bool = True
    _reason: str = None
    _raw_symbol: str = None
    _position_msg: str = ''
    _position: tuple = (1, 1)
    _dt_instance: datatypes.Base = None

    Invalid: str = 'Invalid'
    ListBegin: str = 'ListBegin'
    ListEnd: str = 'ListEnd'
    Identifier: str = 'Identifier'
    Nil: str = datatypes.Nil.name
    Boolean: str = datatypes.Boolean.name
    String: str = datatypes.String.name
    Date: str = datatypes.Date.name
    FloatNumber: str = datatypes.FloatNumber.name
    IntegerNumber: str = datatypes.IntegerNumber.name
    Keyword: str = datatypes.Keyword.name
    NException: str = datatypes.NException.name

    data_types: List[str] = datatypes.DataType.simple + [Identifier]

    _valid_types: List[str] = [Invalid, ListBegin, ListEnd] + data_types

    def __init__(self,
                 _type: str, _value=None,
                 _valid: bool = True, _reason: str = None,
                 _position: tuple = None, _raw_symbol: str = None) -> None:
        """
        Initialize a new NanamiLang Token instance

        On __init__, will try to initialize respective DataType instance.

        :param _type: must be a Token.<something>
        :param _value: must be a type of a "_type"
        :param _valid: whether Token is valid or not
        :param _reason: reason why token is invalid?
        :param _position: source position of a symbol
        :param _raw_symbol: this must be a raw symbol
        """

        # If _valid has been passed
        if _valid is not None:
            ASSERT_IS_INSTANCE_OF(_valid, bool)
            self._valid = _valid
        # If _reason has been passed
        if _reason is not None:
            ASSERT_IS_INSTANCE_OF(_reason, str)
            ASSERT_COLLECTION_IS_NOT_EMPTY(_reason)
            self._reason = _reason
        # If _position has been passed
        if _position is not None:
            ASSERT_IS_INSTANCE_OF(_position, tuple)
            self._position = _position
            self._position_msg = ':'.join(map(str, _position))
        # If _raw_symbol has been passed
        if _raw_symbol is not None:
            ASSERT_IS_INSTANCE_OF(_raw_symbol, str)
            ASSERT_COLLECTION_IS_NOT_EMPTY(_raw_symbol)
            self._raw_symbol = _raw_symbol
        # _type must be a type of str && could not be an empty string
        ASSERT_IS_INSTANCE_OF(_type, str)
        ASSERT_COLLECTION_IS_NOT_EMPTY(_type)
        # _type could not be something different from self._valid_types
        ASSERT_COLL_CONTAINS_ELEMENT(_type, self._valid_types)
        self._type = _type
        # try to initialize self._dt_instance if _type is the data type
        if _type in self.data_types:
            if _type != Token.Identifier:
                self._dt_instance = (
                    datatypes.DataType.resolve(_type)(_value)
                )
            else:
                resolved_mc = BuiltinMacros.resolve(_value)
                resolved_fn = BuiltinFunctions.resolve(_value)
                if resolved_mc:
                    self._dt_instance = datatypes.Macro(resolved_mc)
                elif resolved_fn:
                    self._dt_instance = datatypes.Function(resolved_fn)
                else:
                    self._dt_instance = datatypes.Undefined(_value)
                # If neither Function or Macro, then mark it as Undefined

    def type(self) -> str:
        """NanamiLang Token, self._type getter"""

        return self._type

    def reason(self) -> str:
        """NanamiLang Token, self._reason getter"""

        return self._reason

    def position(self) -> tuple:
        """NanamiLang Token, self._position getter"""

        return self._position

    def dt(self) -> datatypes.Base:
        """NanamiLang Token, self._dt_instance getter"""

        return self._dt_instance

    def __repr__(self) -> str:
        """NanamiLang Token, _repr__() method implementation"""

        return self.__str__()

    def __str__(self) -> str:
        """NanamiLang Token, __str__() method implementation"""

        if self._valid:
            if self._dt_instance is not None:
                return f'<{self._type}>: {self._dt_instance.format()}'
            return f'<{self._type}>'
        return f'Invalid token at <input:{self._position_msg}>. Reason: {self._reason}'
