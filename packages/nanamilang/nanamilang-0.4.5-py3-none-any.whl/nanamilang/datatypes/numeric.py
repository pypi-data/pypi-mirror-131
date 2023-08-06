"""NanamiLang Numeric Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from .base import Base


class Numeric(Base):
    """NanamiLang Numeric Data Type Class"""

    name = 'Numeric'

    def even(self) -> bool:
        """NanamiLang Numeric, even?"""

        return self.reference() % 2 == 0

    def odd(self) -> bool:
        """NanamiLang Numeric, odd?"""

        return not self.reference() % 2 == 0

    def positive(self) -> bool:
        """NanamiLang Numeric, positive?"""

        return self.reference() > 0

    # Maybe, we will implement other numeric-specific methods later
