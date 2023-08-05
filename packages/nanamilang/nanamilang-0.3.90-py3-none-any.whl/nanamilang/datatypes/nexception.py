"""NanamiLang NException Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

import traceback

from nanamilang import shortcuts
from .base import Base
from .string import String
from .hashmap import HashMap
from .keyword import Keyword
from .integernumber import IntegerNumber


class NException(Base):
    """NanamiLang NException Data Type Class"""

    name: str = 'NException'
    _expected_type = Exception
    _python_reference: HashMap
    _exception_instance: Exception
    purpose = 'Encapsulate Python 3 Exception'

    def __init__(self, reference: Exception) -> None:
        """Initialize a new NException instance"""

        super().__init__(reference)
        # and then override self._python_reference as we want

        self._exception_instance = reference
        # and also store originally passed exception instance

        self._python_reference = HashMap(
            (
                Keyword('message'), String(reference.__str__()),
                Keyword('name'), String(reference.__class__.__name__)
             ),
        )
        # turn self._python_reference into nanamilang.datatypes.HashMap

        self._to_return_for_reference_method_call = IntegerNumber(1)
        # this is what 'self.reference()' will return on its invocation

    def get(self, key: Keyword) -> Base:
        """NanamiLang NException, get() method implementation"""

        # Tricky moment, I would say :D
        # Usually, nanamilang.builtin.BuiltinFunctions.get
        # should stop us from passing illegally typed 'key' ...
        # But the user always can invoke this method directly, so check
        shortcuts.ASSERT_IS_INSTANCE_OF(key, Keyword)

        return self._python_reference.get(key)

    def hashed(self) -> int:
        """NanamiLang NException, hashed() method implementation"""

        # Override hashed() to return stored HashMap.hashed() value.
        return self._python_reference.hashed()

    def reference(self) -> IntegerNumber:
        """NanamiLang NException, reference() method implementation"""

        # Always return 1.
        # This is because of decision to be compatible with
        # 'nanamilang-eval.py' script that requires Program.evaluate()
        # to return nothing but datatypes.IntegerNumber.
        # Since throwing an Exception could be treated as an error, and
        # the common way to tell the system about program error on exit
        # is to return '1' value. But maybe its ridiculous behavior, idk.
        return self._to_return_for_reference_method_call

    def format(self, **kwargs) -> str:
        """NanamiLang NException, format() method implementation"""

        # I guess we do not allocate much memory here...

        _name = self._python_reference.get(Keyword('name')).reference()
        _message = self._python_reference.get(Keyword('message')).reference()

        traceback_str = '\n' + ''.join(traceback.format_tb(
            self._exception_instance.__traceback__)
        ) + '\n' if kwargs.get('showtraceback', False) else ''

        return f'Python 3 Exception has been occurred\n' \
               f'NanamiLang tried to catch it and encapsulate it in\n' \
               f'<nanamilang.datatypes.nexception.NException> class\n' \
               f'{traceback_str}Python 3 Exception info <{_name}> {_message}'
