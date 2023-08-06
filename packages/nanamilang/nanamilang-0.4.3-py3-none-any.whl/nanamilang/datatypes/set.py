"""NanamiLang Set Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from typing import ValuesView
from nanamilang import shortcuts
from .base import Base
from .collection import Collection


class Set(Collection):
    """NanamiLang Set Data Type Class"""

    name: str = 'Set'
    _expected_type = dict
    _default = {}
    _python_reference: dict
    purpose = 'Implements Set of NanamiLang Base data types'

    def _init__chance_to_process_and_override(self,
                                              reference) -> dict:
        """NanamiLang Set, process and override reference"""

        # Here we can complete initialization procedure

        return {element.hashed(): element for element in reference}

    def get(self, by: Base) -> Base:
        """NanamiLang Set, get() implementation"""

        shortcuts.ASSERT_IS_CHILD_OF(
            by,
            Base,
            message='Set.get() "by" must be Base derived'
        )

        return self.reference().get(by.hashed(), self._nil)

    def items(self) -> ValuesView:
        """NanamiLang Set, items() method implementation"""

        return self._python_reference.values()

    def format(self, **_) -> str:
        """NanamiLang Set, format() method implementation"""

        # There is no sense to iterate over elements when we just can return a '#{}'
        if not self._python_reference:
            return '#{}'
        return '#{' + f'{" ".join((v.format() for v in self.reference().values()))}' + '}'
