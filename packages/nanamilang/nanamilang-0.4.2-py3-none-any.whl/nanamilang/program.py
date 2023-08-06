"""NanamiLang Program Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

import time
from typing import List, Dict

from nanamilang.ast import AST
from nanamilang.formatter import Formatter
from nanamilang.shortcuts import ASSERT_COLLECTION_IS_NOT_EMPTY
from nanamilang.shortcuts import ASSERT_IS_INSTANCE_OF
from nanamilang.token import Token
from nanamilang.tokenizer import Tokenizer


class Program:
    """
    NanamiLang Program

    from nanamilang import program

    source = '(+ 2 2 (* 2 2))'
    program: program.Program = program.Program(str(source))
    program.format() # => "(+ 2 2 (* 2 2))"
    program.ast() # => get encapsulated AST instance
    program.tokenized() # => collection of a Token instances

    results = program.evaluate() # => ((<IntegerNumber>: 8, ...),)
    """

    _ast: AST
    _source: str
    _formatter = Formatter
    _tokenized: List[Token]
    _measurements: Dict[str, float] = {}

    def __init__(self, source: str) -> None:
        """
        Initialize a new NanamiLang Program instance

        :param source: your NanamiLang program source code
        """

        ASSERT_IS_INSTANCE_OF(source, str)
        ASSERT_COLLECTION_IS_NOT_EMPTY(source)

        self._source = source
        __tokenize_start__ = time.perf_counter()
        self._tokenized = Tokenizer(self._source).tokenize()
        __tokenize_delta__ = time.perf_counter() - __tokenize_start__
        __make_wood_start__ = time.perf_counter()
        self._ast = AST(self._tokenized)
        __make_wood_delta__ = time.perf_counter() - __make_wood_start__
        self._formatter = Formatter(self._tokenized)
        self._measurements = {
            '[Tree]': __make_wood_delta__, '[Parse]': __tokenize_delta__,
        }

    def ast(self) -> AST:
        """NanamiLang Program, self._ast getter"""

        return self._ast

    def tokenized(self) -> List[Token]:
        """NanamiLang Program, self._tokenized getter"""

        return self._tokenized

    def measurements(self) -> Dict[str, float]:
        """NanamiLang Program, self._measurements getter"""

        return self._measurements

    def format(self) -> str:
        """NanamiLang Program, call self._formatter.format() to format source"""

        return self._formatter.format()

    def evaluate(self) -> tuple:
        """NanamiLang Program, call self._ast.evaluate() to evaluate your program"""

        __evaluate_start__ = time.perf_counter()
        results = self._ast.evaluate()
        __evaluate_delta__ = time.perf_counter() - __evaluate_start__
        self._measurements.update({'[Evaluation]': __evaluate_delta__})
        return results

        # Measure [Evaluation] time and store measurement in self._measurements dictionary
        # Return all evaluated trees of the self.ast().wood() to Program.evaluate() caller
