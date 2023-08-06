"""NanamiLang Callable Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from .base import Base


class Callable(Base):
    """NanamiLang Callable Data Type Class"""

    name = 'Callable'
    _expected_type = dict
    _python_reference: dict

    def origin(self) -> str:
        """NanamiLang Callable, origin() method implementation"""

        return self.format()
