"""NanamiLang NException Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

import os.path
from typing import Tuple

from nanamilang import shortcuts
from .base import Base
from .string import String
from .vector import Vector
from .hashmap import HashMap
from .keyword import Keyword
from .integernumber import IntegerNumber


class NException(Base):
    """NanamiLang NException Data Type Class"""

    _traceback: str = ''
    _exception: Exception
    _expected_type = HashMap
    name: str = 'NException'
    _position: tuple = (1, 1)
    _python_reference: HashMap
    purpose = 'Encapsulate Python 3 Exception'

    def __init__(self, reference: Tuple[Exception, tuple]) -> None:
        """Initialize a new NException instance"""

        self._exception, self._position = reference
        # remember _what_ the error has been occurred and __where__

        line_no, char_no = self._position
        # it may be useless and removed in future, but destruct pos

        self._position_message = f'input:{line_no}:{char_no}'
        # to show that fancy string displaying where error occurred

        reference = HashMap(
            (
                Keyword('message'),
                String(self._exception.__str__()),
                Keyword('name'),
                String(self._exception.__class__.__name__),
                # and store position that we can access it later
                Keyword('position'), Vector(
                    (IntegerNumber(line_no), IntegerNumber(char_no))
                ),
             ),
        )
        # turn reference into a nanamilang.datatypes.HashMap instance

        super().__init__(reference)
        # and then we can call Base.__init__() through Python super()

        _traceback_l = []
        _t = self._exception.__traceback__
        while _t is not None:
            _f = os.path.split(_t.tb_frame.f_code.co_filename)[1]
            _traceback_l.append(f'{_f}:{_t.tb_lineno}')
            _t = _t.tb_next
        self._traceback = ' -> '.join(_traceback_l) + '\n'
        # store self._traceback (cause it could be used in self.format())

    def position(self) -> tuple:
        """NanamiLang NException, self._position getter"""

        return self._position

    def exception(self) -> Exception:
        """NanamiLang NException, self,_exception getter"""

        return self._exception

    def get(self, key: Keyword) -> Base:
        """NanamiLang NException, get() method implementation"""

        # Tricky moment, I would say :D
        # Usually, nanamilang.builtin.BuiltinFunctions.get
        # should stop us from passing illegally typed 'key' ...
        # But user always can invoke this method directly, so check
        shortcuts.ASSERT_IS_INSTANCE_OF(key, Keyword)

        return self._python_reference.get(key)

    def hashed(self) -> int:
        """NanamiLang NException, hashed() method implementation"""

        # Override hashed() to return stored HashMap.hashed() value.
        return self._python_reference.hashed()

    def format(self, **kwargs) -> str:
        """NanamiLang NException, format() method implementation"""

        include_traceback = kwargs.get('include_traceback')
        _tb_included = f'\n{self._traceback}\n' if include_traceback else ''

        return f'<{self._position_message}>: '\
               f'<{self._python_reference.get(Keyword("name")).reference()}: '\
               f'{self._python_reference.get(Keyword("message")).reference()}>\n{_tb_included}'
