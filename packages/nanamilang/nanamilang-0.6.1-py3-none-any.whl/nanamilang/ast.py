"""NanamiLang AST CLass"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from functools import wraps
from typing import List

from nanamilang import datatypes
from nanamilang.builtin import BuiltinFunctions
from nanamilang.shortcuts import ASSERT_COLLECTION_IS_NOT_EMPTY
from nanamilang.shortcuts import ASSERT_EVERY_COLLECTION_ITEM_IS_INSTANCE_OF
from nanamilang.shortcuts import ASSERT_IS_INSTANCE_OF
from nanamilang.token import Token


def handle(exceptions: tuple):
    """
    NanamiLang AST, handle exceptions:
    1. If exception has been suddenly raised
    2. Try to determine position where it happened
    3. Create & return datatypes.MException instance

    :param exceptions: tuple of exceptions to handle
    """

    def wrapped(_fn):
        @wraps(_fn)
        def function(*args, **kwargs):
            try:
                return _fn(*args, **kwargs)
            except exceptions as exception:
                # At least __try__ to
                # determine error occurrence position
                # First, lets make it in a cheapest way ever
                position = getattr(exception, '_position', None)
                # Non-custom exception obviously don't contain
                # _position, so as we working with s-expressions,
                # assume that exception occurred at the f/m call.
                if not position:
                    tree: list = args[1]
                    maybe_token: Token = tree[0]
                    if isinstance(maybe_token, Token):
                        position = maybe_token.position()
                # We tried so hard ... but position still is None
                if not position:
                    position = (1, 1)
                # Guessing position - fucking hell, to be honest..
                return datatypes.NException((exception, position))

        return function

    return wrapped


class ASTBuildInvalidInput(Exception):
    """
    NML AST Build Error: Invalid input
    """

    def __str__(self):
        """NanamiLang ASTBuildInvalidInput"""

        # Do not scare AST._create() please :(
        return 'Something wrong with the input'


class ASTBuildInvalidToken(Exception):
    """
    NML AST Build Error: Invalid token
    """

    _token: Token
    _position: tuple

    def __str__(self):
        """NanamiLang ASTBuildInvalidToken"""

        return self._token.reason()

    def __init__(self, token: Token, *args):
        """NanamiLang ASTBuildInvalidToken"""

        self._token = token
        self._position = token.position()

        super(ASTBuildInvalidToken).__init__(*args)


class ASTEvalIsNotAFunctionDataType(Exception):
    """
    NML AST Eval Error: Not a function data type
    """

    _name: str
    _position: tuple

    def __init__(self, token: Token, *args):
        """NanamiLang ASTEvalIsNotAFunctionDataType"""

        self._name = token.dt().format()
        self._position = token.position()

        super(ASTEvalIsNotAFunctionDataType).__init__(*args)

    def __str__(self):
        """NanamiLang ASTEvalIsNotAFunctionDataType"""

        return f'"{self._name}" is not a Function Data Type'


class ASTEvalNotFoundInThisContent(Exception):
    """
    NML AST Eval Error: Not found in this content
    """

    _name: str
    _position: tuple

    def __init__(self, token: Token, *args):
        """NanamiLang ASTEvalNotFoundInThisContent"""

        self._name = token.dt().origin()
        self._position = token.position()

        super(ASTEvalNotFoundInThisContent).__init__(*args)

    def __str__(self):
        """NanamiLang ASTEvalNotFoundInThisContent"""

        return f'"{self._name}" was not found in this context'


class AST:
    """
    NanamiLang AST (abstract syntax tree)

    Usage:
    ```
    from nanamilang.ast import AST
    from nanamilang.tokenizer import Tokenizer
    t: Tokenizer = Tokenizer('(+ 2 2 (* 2 2))')
    tokenized = t.tokenize() # => tokenize input string
    ast: AST = AST(tokenized) # => create new AST instance
    <... AST.__init__() method will create wood automatically ...>
    results = program.evaluate() # => ((<IntegerNumber>: 8, ...),)
    ```
    """

    _tokenized: List[Token] = None
    _wood: List[List[Token] or Token] = None

    def __init__(self, tokenized: List[Token]) -> None:
        """
        Initialize a new NanamiLang AST instance

        :param tokenized: collection of Token instances
        """

        ASSERT_IS_INSTANCE_OF(tokenized, list)
        ASSERT_COLLECTION_IS_NOT_EMPTY(tokenized)
        ASSERT_EVERY_COLLECTION_ITEM_IS_INSTANCE_OF(tokenized, Token)

        self._tokenized = tokenized
        # In case something wrong with the tree, return '(identity nexception)'
        # And instead of passing internal exception, spawn our own ASTInvalidTree
        # and steal traceback object instance from the caught exception :)
        try:
            self._wood = self._create()
        except (Exception,) as _:
            self._wood = [
                [Token(Token.Identifier, 'identity'),
                 Token(Token.NException,
                       (ASTBuildInvalidInput().with_traceback(_.__traceback__), (1, 1)))]
            ]

    def wood(self) -> list:
        """Nanamilang AST, self._wood getter"""

        return self._wood

    def _create(self) -> list:
        """NanamiLang AST, create an actual wood of trees"""

        # Initially was written by @buzzer13 (https://gitlab.com/buzzer13)

        items = []
        stack = [items]

        for token in self._tokenized:

            if token.type() == Token.ListBegin:

                wired = []
                stack[-1].append(wired)
                stack.append(wired)

            elif token.type() == Token.ListEnd:

                stack.pop()

            elif token.type() == Token.Invalid:

                # Propagate Invalid token as a NException
                return [
                    [Token(Token.Identifier, 'identity'),
                     Token(Token.NException,
                           (ASTBuildInvalidToken(token), token.position()))]
                ]

            else:

                stack[-1].append(token)

        return [i
                if isinstance(i, list)
                else [Token(Token.Identifier, 'identity'), i] for i in items]

    def evaluate(self) -> tuple:
        """NanamiLang AST, recursively evaluate wood"""

        @handle((Exception,))
        def recursive(environment: dict, tree: List[Token]) -> datatypes.Base:
            if not tree:
                return datatypes.Nil('nil')
            args: List[datatypes.Base] = []
            identifier: List[Token] or Token
            rest: List[Token or List[Token]]
            identifier, *rest = tree
            # If identifier is a Macro, handle it ...
            if isinstance(identifier, Token):
                if isinstance(identifier.dt(), datatypes.Macro):
                    return recursive(
                        environment,
                        identifier.dt().reference()(Token, rest, environment, recursive))
            # Start collecting arguments for a Function call ...
            for part in rest:
                if isinstance(part, Token):
                    # If token is Identifier, try to handle bindings ...
                    if part.type() == part.Identifier:
                        defined = environment.get(part.dt().origin())
                        # If token was initially marked as an Undefined ...
                        # check whether it has been defined somewhere above ...
                        if isinstance(part.dt(), datatypes.Undefined):
                            if not defined:
                                raise ASTEvalNotFoundInThisContent(part)
                        args.append(defined if defined is not None else part.dt())
                        # If token was NOT initially marked as an Undefined
                        # add its bundled data type to arg list, add a 'defined' otherwise
                    else:
                        args.append(part.dt())
                    # If it is something different from Identifier, add its bundled datatype
                else:
                    # Since we use handle() decorator, it can return
                    # an NException data type instance, so handle it ..
                    result_or_nexception = recursive(environment, part)
                    if isinstance(result_or_nexception, datatypes.NException):
                        return result_or_nexception
                    # Don't add NException to args, return it instead (exception-propagation)
                    args.append(result_or_nexception)
                    # If nothing critical happened -> append a 'result_or_nexception' to args
            # Finally, we almost ready to handle a Function call
            if isinstance(identifier, list):
                # Since we use handle() decorator, it can return
                # an NException data type instance, so handle it ..
                result_or_nexception = recursive(environment, identifier)
                if isinstance(result_or_nexception, datatypes.NException):
                    return result_or_nexception
                # Do not call NException reference, return it instead (exception-propagation)
                if isinstance(result_or_nexception, datatypes.Function):
                    return result_or_nexception.reference()(args)
                if isinstance(result_or_nexception, datatypes.Keyword):
                    return BuiltinFunctions.get_func(args + [result_or_nexception])
                raise ASTEvalIsNotAFunctionDataType(identifier[0])
                # If nothing critical happened -> call 'result_or_exception'.reference(args).
            if identifier.type() == identifier.Keyword:
                return BuiltinFunctions.get_func(args + [identifier.dt()])
            if identifier.type() == identifier.Identifier:
                defined = environment.get(identifier.dt().origin())
                if isinstance(identifier.dt(), datatypes.Undefined):
                    if not defined:
                        raise ASTEvalNotFoundInThisContent(identifier)
                    return defined.reference()(args)
                dt = defined or identifier.dt()
                if isinstance(dt, datatypes.Function):
                    return dt.reference()(args)
                if isinstance(dt, datatypes.Keyword):
                    return BuiltinFunctions.get_func(args + [dt])
            raise ASTEvalIsNotAFunctionDataType(identifier)
            # If user tries to call Keyword or a Function, handle it, otherwise raise Exception

        return tuple((recursive({}, _tree), _tree) for _tree in self.wood())
        # Iterate through wood of trees, collect results, and return them to AST.evaluate(...) caller
