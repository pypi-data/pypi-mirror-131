"""NanamiLang Undefined Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from .base import Base


class Undefined(Base):
    """NanamiLang Undefined Data Type Class"""

    _hashed = hash('undefined')
    name: str = 'Undefined'
    _expected_type = str
    _python_reference: str
    purpose = 'To mark as an undefined at parse-time'

    def format(self, **kwargs) -> str:
        """NanamiLang Undefined, format() method implementation"""

        return 'undefined'

    def origin(self) -> str:
        """NanamiLang Undefined, origin() method implementation"""

        return self._python_reference

    def reference(self) -> None:
        """NanamiLang Undefined, reference() method implementation"""

        return None
