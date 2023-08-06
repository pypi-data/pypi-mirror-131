"""NanamiLang BuiltinMacros and BuiltinFunctions classes"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

import functools
import time
from functools import reduce
from typing import List

from nanamilang import fn, datatypes
from nanamilang.shortcuts import get
from nanamilang.shortcuts import (
    ASSERT_COLL_LENGTH_IS_EVEN,
    ASSERT_DICT_CONTAINS_KEY, NML_M_ASSERT_FORM_IS_A_VECTOR
)
from nanamilang.shortcuts import randstr, plain2partitioned
from nanamilang.spec import Spec


def meta(data: dict):
    """
    NanamiLang, apply meta data to a function
    'name': fn or macro LISP name
    'type': 'macro' or 'function'
    'forms': possible fn or macro possible forms
    'docstring': what fn or macro actually does?
    May contain 'hidden' (do not show in completions)
    May contain 'spec' attribute, but its not required

    :param data: a function meta data Python dictionary
    """

    def wrapped(_fn):
        @functools.wraps(_fn)
        def function(*args, **kwargs):
            spec = data.get('spec')
            if spec:
                if data.get('type') == 'macro':
                    Spec.validate(data.get('name'), args[1], spec)
                else:
                    Spec.validate(data.get('name'), args[0], spec)

            return _fn(*args, **kwargs)

        # TODO: maybe also implement spec linting

        ASSERT_DICT_CONTAINS_KEY('name', data, 'function meta data must contain a name')
        ASSERT_DICT_CONTAINS_KEY('type', data, 'function meta data must contain a type')
        ASSERT_DICT_CONTAINS_KEY('forms', data, 'function meta data must contain a forms')
        ASSERT_DICT_CONTAINS_KEY('docstring', data, 'function meta data must contain a docstring')

        function.meta = data

        return function

    return wrapped


class LetUnableAssignToError(Exception):
    """
    NanamiLang Let Error
    Unable assign to error
    """

    _target = None

    def __init__(self, to, *args):
        """NanamiLang LetUnableAssignToError"""

        self._target = to

        super(LetUnableAssignToError).__init__(*args)

    def __str__(self):
        """NanamiLang LetUnableAssignToError"""

        return f'let: unable to assign to {self._target}'


class LetDestructuringError(Exception):
    """
    NanamiLang Let Error

    """

    _reason: str = None
    Reason_LeftSideIsNotAVector: str = 'left side needs to be a Vector'
    Reason_RightSideIsNotAVector: str = 'right side needs to be a Vector'
    Reason_LeftAndRightLensUnequal: str = 'left and right sides lengths are unequal'

    def __init__(self, reason, *args):
        """NanamiLang LetDestructuringError"""

        self._reason = reason

        super(LetDestructuringError).__init__(*args)

    def __str__(self):
        """NanamiLang LetUnableAssignToError"""

        return f'let: an error has been occurred while destructuring: {self._reason}'


class BuiltinMacros:
    """NanamiLang Builtin Macros"""

    cached = {}

    ########################################################################################################

    @staticmethod
    def resolve(mc_name: str) -> dict:
        """Resolve macro by its name"""

        if fun := BuiltinMacros.cached.get(mc_name, {}):
            return fun
        for macro in BuiltinMacros.functions():
            if macro.meta.get('name') == mc_name:
                resolved: dict = {'macro_name': mc_name,
                                  'macro_reference': macro}
                BuiltinMacros.cached.update({mc_name: resolved})
                return resolved
        return {}

    @staticmethod
    def names() -> list:
        """Return LISP names"""

        return [_.meta.get('name') for _ in BuiltinMacros.functions()]

    @staticmethod
    def functions() -> list:
        """Return all _macro functions"""

        attrib_names = filter(lambda _: '_macro' in _, BuiltinMacros().__dir__())

        return list(map(lambda n: getattr(BuiltinMacros, n, None), attrib_names))

    ########################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': '->',
           'type': 'macro',
           'forms': ['(-> form1 form2 ... formN)'],
           'docstring': 'Allows to write code as pipeline'})
    def first_threading_macro(token_cls, tree_slice: list, *_) -> list:
        """
        Builtin '->' macro implementation

        :param tree_slice: slice of encountered tree
        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        if len(tree_slice) > 1:

            for idx, tof in enumerate(tree_slice):
                if len(tree_slice) - 1 != idx:
                    if not isinstance(tof, list):
                        tof = [token_cls(token_cls.Identifier, 'identity'),
                               tof]
                    next_tof = tree_slice[idx + 1]
                    if not isinstance(next_tof, list):
                        tree_slice[idx + 1] = [next_tof, tof]
                    else:
                        tree_slice[idx + 1].insert(1, tof)

            return tree_slice[-1]

        return [token_cls(token_cls.Identifier, 'identity'), tree_slice[-1]]

    ########################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': '->>',
           'type': 'macro',
           'forms': ['(->> form1 form2 ... formN)'],
           'docstring': 'Allows to write code as pipeline'})
    def last_threading_macro(token_cls, tree_slice: list, *_) -> list:
        """
        Builtin '->>' macro implementation

        :param tree_slice: slice of encountered tree
        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        if len(tree_slice) > 1:

            for idx, tof in enumerate(tree_slice):
                if len(tree_slice) - 1 != idx:
                    if not isinstance(tof, list):
                        tof = [token_cls(token_cls.Identifier, 'identity'),
                               tof]
                    next_tof = tree_slice[idx + 1]
                    if not isinstance(next_tof, list):
                        tree_slice[idx + 1] = [next_tof, tof]
                    else:
                        tree_slice[idx + 1].append(tof)

            return tree_slice[-1]

        return [token_cls(token_cls.Identifier, 'identity'), tree_slice[-1]]

    ########################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': 'measure',
           'type': 'macro',
           'forms': ['(measure ...)'],
           'docstring': 'Measure a form evaluation time'})
    def measure_macro(token_cls, tree_slice: list, env: dict, eval_function) -> list:
        """
        Builtin 'measure' macro implementation

        :param tree_slice: slice of encountered tree
        :param env: current environment during evaluation
        :param eval_function: reference to recursive eval function
        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        started = time.perf_counter()

        eval_function(env, tree_slice)

        finished = time.perf_counter()

        return [token_cls(token_cls.Identifier, 'identity'),
                token_cls(token_cls.String, f'Took {finished - started:.5f} seconds')]

    ########################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 3]],
           'name': 'if',
           'type': 'macro',
           'forms': ['(if cond true-branch else-branch)'],
           'docstring': 'Returns true/else depending on cond'})
    def if_macro(token_cls, tree_slice: list, env: dict, eval_function) -> list:
        """
        Builtin 'if' macro implementation

        :param tree_slice: slice of encountered tree
        :param env: current environment during evaluation
        :param eval_function: reference to recursive eval function
        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        cond, true_branch, else_branch = tree_slice

        if not isinstance(cond, list):
            cond = [token_cls(token_cls.Identifier, 'identity'), cond]
        if not isinstance(true_branch, list):
            true_branch = [token_cls(token_cls.Identifier, 'identity'), true_branch]
        if not isinstance(else_branch, list):
            else_branch = [token_cls(token_cls.Identifier, 'identity'), else_branch]

        return true_branch if eval_function(env, cond).truthy() is True else else_branch

    ########################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityEven]],
           'name': 'cond',
           'type': 'macro',
           'forms': ['(cond cond1 expr1 ... condN exprN)'],
           'docstring': 'Allows you to describe your cond-expr pairs'})
    def cond_macro(token_cls, tree_slice: list, env: dict, eval_function) -> list:
        """
        Builtin 'cond' macro implementation

        :param tree_slice: slice of encountered tree
        :param env: current environment during evaluation
        :param eval_function: reference to recursive eval function
        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        for [cond, expr] in plain2partitioned(tree_slice):
            if eval_function(env,
                             cond
                             if isinstance(cond, list)
                             else [token_cls(token_cls.Identifier, 'identity'),
                                   cond]).truthy():
                return expr \
                    if isinstance(expr, list) \
                    else [token_cls(token_cls.Identifier, 'identity'), expr]
        return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Nil, 'nil')]

    ########################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': 'comment',
           'type': 'macro',
           'forms': ['(comment ...)'],
           'docstring': 'Allows you to replace entire form with a Nil'})
    def comment_macro(token_cls, *_) -> list:
        """
        Builtin 'comment' macro implementation

        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Nil, 'nil')]

    ########################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': 'and',
           'type': 'macro',
           'forms': ['(and cond1 cond2 ... condN)'],
           'docstring': 'Returns true if empty form, compares truths'})
    def and_macro(token_cls, tree_slice: list, env: dict, eval_function) -> list:
        """
        Builtin 'and' macro implementation

        :param tree_slice: slice of encountered tree
        :param env: current environment during evaluation
        :param eval_function: reference to recursive eval function
        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        if not tree_slice:
            return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Boolean, True)]

        for condition in tree_slice:
            if not isinstance(condition, list):
                condition = [token_cls(token_cls.Identifier, 'identity'), condition]
            if not eval_function(env, condition).truthy():
                return condition

        last = tree_slice[-1]
        return last if isinstance(last, list) else [token_cls(token_cls.Identifier, 'identity'), last]

    ########################################################################################################

    @staticmethod
    @meta({'spec': ((Spec.ArityAtLeastOne,),),
           'name': 'or',
           'type': 'macro',
           'forms': ['(or cond1 cond2 ... condN)'],
           'docstring': 'Returns a nil if empty form, compares truths'})
    def or_macro(token_cls, tree_slice: list, env: dict, eval_function) -> list:
        """
        Builtin 'or' macro implementation

        :param tree_slice: slice of encountered tree
        :param env: current environment during evaluation
        :param eval_function: reference to recursive eval function
        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        if not tree_slice:
            return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Nil, 'nil')]

        for condition in tree_slice:
            if not isinstance(condition, list):
                condition = [token_cls(token_cls.Identifier, 'identity'), condition]
            if eval_function(env, condition).truthy():
                return condition

        last = tree_slice[-1]
        return last if isinstance(last, list) else [token_cls(token_cls.Identifier, 'identity'), last]

    ########################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityVariants, [2, 3]]],
           'name': 'fn',
           'type': 'macro',
           'forms': ['(fn [n ...] f)',
                     '(fn name [n ...] f)'],
           'docstring': 'Allows to define anonymous function, maybe named'})
    def fn_macro(token_cls, tree_slice: list, env: dict, eval_function) -> list:
        """
        Builtin 'fn' macro implementation

        :param tree_slice: slice of encountered tree
        :param env: current environment during evaluation
        :param eval_function: reference to recursive eval function
        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        name_token, parameters_form, body_token_or_form = [None] * 3

        if len(tree_slice) == 2:
            parameters_form, body_token_or_form = tree_slice
        elif len(tree_slice) == 3:
            name_token, parameters_form, body_token_or_form = tree_slice
            assert not isinstance(name_token, list), 'fn: name needs to be a token, not a form'
            assert name_token.type() == token_cls.Identifier, 'fn: name needs to be Identifier'

        NML_M_ASSERT_FORM_IS_A_VECTOR(parameters_form, 'fn: parameters form needs to be a Vector')

        parameters = []
        for tof in parameters_form[1:]:
            if isinstance(tof, list):
                right = []
                for x in tof[1:]:
                    assert x.type() == token_cls.Identifier, (
                        'fn: form element needs to be an Identifier'
                    )
                    right.append(x.dt().origin())
                parameters.append((f'v{randstr()}', right))
            else:
                assert tof.type() == token_cls.Identifier, (
                    'fn: each element needs to be an Identifier'
                )
                parameters.append((tof.dt().origin(), None))

        name = name_token.dt().origin() if name_token else randstr()

        fni = fn.Fn(env, name, eval_function, token_cls, parameters, body_token_or_form)

        # Pylint will not be happy, but we can use lambda here and don't have any problems with it
        handle = lambda args: fni.handle(tuple(args))

        handle.meta = {
            'name': name, 'docstring': '',
            'type': 'function', 'forms': fni.generate_meta__forms()
        }

        payload = {name: datatypes.Function({'function_name': name,
                                             'function_reference': handle})}

        # Update local env, so eval_function() will later know about function
        env.update(payload)
        fni.env().update(payload)

        return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Identifier, name)]

    ########################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2]],
           'name': 'let',
           'type': 'macro',
           'forms': ['(let [b1 v1 ...] b1)'],
           'docstring': 'Allows to define local bindings and access them later'})
    def let_macro(token_cls, tree_slice: list, env: dict, eval_function) -> list:
        """
        Builtin 'let' macro implementation

        :param tree_slice: slice of encountered tree
        :param env: current environment during evaluation
        :param eval_function: reference to recursive eval function
        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        bindings_form, body_form = tree_slice

        but_first = bindings_form[1:]

        ASSERT_COLL_LENGTH_IS_EVEN(but_first,
                                   'let: bindings form must be even')

        for [key_token_or_form, value_token_or_form] in plain2partitioned(but_first):
            evaluated_value = eval_function(
                env,
                value_token_or_form
                if isinstance(value_token_or_form, list)
                else [token_cls(token_cls.Identifier, 'identity'), value_token_or_form])
            if isinstance(key_token_or_form, token_cls) and key_token_or_form.type() == token_cls.Identifier:
                env[key_token_or_form.dt().origin()] = evaluated_value
            elif isinstance(key_token_or_form, list):
                if not key_token_or_form[0].dt().origin() == 'make-vector':
                    raise LetDestructuringError(LetDestructuringError.Reason_LeftSideIsNotAVector)
                if not isinstance(evaluated_value, datatypes.Vector):
                    raise LetDestructuringError(LetDestructuringError.Reason_RightSideIsNotAVector)
                if not len(key_token_or_form[1:]) == len(evaluated_value.reference()):
                    raise LetDestructuringError(LetDestructuringError.Reason_LeftAndRightLensUnequal)
                for from_left, from_right in zip(key_token_or_form[1:], evaluated_value.reference()):
                    if isinstance(from_left, token_cls) and from_left.type() == token_cls.Identifier:
                        env[from_left.dt().origin()] = from_right
                    else:
                        raise LetUnableAssignToError(from_right)
            else:
                raise LetUnableAssignToError(key_token_or_form)

        return body_form if isinstance(body_form, list) else [token_cls(token_cls.Identifier, 'identity'), body_form]

    #################################################################################################################


class BuiltinFunctions:
    """NanamiLang Builtin Functions"""

    #################################################################################################################

    @staticmethod
    def install(fn_meta: dict, fn_callback) -> bool:
        """
        Allow others to install own functions.
        For example: let the REPL install (exit) function

        :param fn_meta: required function meta information
        :param fn_callback: installed function callback reference
        """

        reference_key = f'{fn_meta.get("name")}_func'
        maybe_existing = getattr(BuiltinFunctions, reference_key, None)
        if maybe_existing:
            delattr(BuiltinFunctions, reference_key)

        setattr(BuiltinFunctions, reference_key, fn_callback)
        getattr(BuiltinFunctions, reference_key, None).meta = fn_meta
        return bool(getattr(BuiltinFunctions, reference_key, None).meta == fn_meta)

    #################################################################################################################

    cached = {}

    @staticmethod
    def resolve(fn_name: str) -> dict:
        """Resolve function by its name"""

        if fun := BuiltinMacros.cached.get(fn_name, {}):
            return fun
        for func in BuiltinFunctions.functions():
            if func.meta.get('name') == fn_name:
                resolved: dict = {'function_name': fn_name,
                                  'function_reference': func}
                BuiltinFunctions.cached.update({fn_name: resolved})
                return resolved
        return {}

    @staticmethod
    def names() -> list:
        """Return LISP names"""

        return [_.meta.get('name') for _ in BuiltinFunctions.functions()]

    @staticmethod
    def functions() -> list:
        """Return all _func functions"""

        attrib_names = filter(lambda _: '_func' in _, BuiltinFunctions().__dir__())

        return list(map(lambda n: getattr(BuiltinFunctions, n, None), attrib_names))

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1]],
           'name': 'identity',
           'type': 'function',
           'forms': ['(identity something)'],
           'docstring': 'Returns something as it is'})
    def identity_func(args: List[datatypes.Base]) -> datatypes.Base:
        """
        Builtin 'identity' function implementation

        :param args: incoming 'identity' function arguments
        :return: datatypes.Base

        """

        return args[0]
        # Function is required for internal purposes and can be used elsewhere

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1],
                    [Spec.EachArgumentTypeIs, datatypes.Collection]],
           'name': 'count',
           'type': 'function',
           'forms': ['(count collection)'],
           'docstring': 'Returns passed collection elements count'})
    def count_func(args: List[datatypes.Collection]) -> datatypes.IntegerNumber:
        """
        Builtin 'count' function implementation

        :param args: incoming 'count' function arguments
        :return: datatypes.IntegerNumber

        TODO: this function could be moved to 'stdlib.nml'
        """

        return args[0].count()
        # Since complex data structures use IntegerNumber to represent int value

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1],
                    [Spec.EachArgumentTypeIs, datatypes.Collection]],
           'name': 'empty?',
           'type': 'function',
           'forms': ['(empty? collection)'],
           'docstring': 'Whether passed collection is empty or not'})
    def empty_func(args: List[datatypes.Collection]) -> datatypes.Boolean:
        """
        Builtin 'empty?' function implementation

        :param args: incoming 'empty?' function arguments
        :return: datatypes.Boolean

        TODO: this function could be moved to 'stdlib.nml'
        """

        return args[0].empty()
        # Since complex data structures use Boolean to represent boolean value

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.ArgumentsTypeChainVariants, [(datatypes.HashSet, datatypes.Base),
                                                       (datatypes.Vector, datatypes.IntegerNumber),
                                                       (datatypes.HashMap, datatypes.Base),
                                                       (datatypes.NException, datatypes.Keyword)]]],
           'name': 'get',
           'type': 'function',
           'forms': ['(get collection by)'],
           'docstring': 'Returns collection element by key, index or element'})
    def get_func(args: List[datatypes.Base]) -> datatypes.Base:
        """
        Builtin 'get' function implementation

        :param args: incoming 'get' function arguments
        :return: datatypes.Base

        TODO: this function could be moved to 'stdlib.nml'
        """

        collection: datatypes.Collection
        by: datatypes.Base

        collection, by = args

        return collection.get(by)
        # Let the Collection.get() handle 'get' operation depending on collection type and 'by' argument

    #################################################################################################################

    @staticmethod
    @meta({'spec': None,
           'name': 'make-hashset',
           'type': 'function',
           'forms': ['(make-hashset e1 e2 ... eX)'],
           'docstring': 'Creates a HashSet data structure'})
    def make_set_func(args: List[datatypes.Base]) -> datatypes.HashSet:
        """
        Builtin 'make-hashset' function implementation

        :param args: incoming 'make-hashset' function arguments
        :return: datatypes.HashSet
        """

        return datatypes.HashSet(tuple(args))
        # Let the Collection.__init__() handle set structure construction

    #################################################################################################################

    @staticmethod
    @meta({'spec': None,
           'name': 'make-vector',
           'type': 'function',
           'forms': ['(make-vector e1 e2 ... eX)'],
           'docstring': 'Creates a Vector data structure'})
    def make_vector_func(args: List[datatypes.Base]) -> datatypes.Vector:
        """
        Builtin 'make-vector' function implementation

        :param args: incoming 'make-vector' function arguments
        :return: datatypes.Vector
        """

        return datatypes.Vector(tuple(args))
        # Let the Collection.__init__() handle vector structure construction

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityEven]],
           'name': 'make-hashmap',
           'type': 'function',
           'forms': ['(make-hashmap k1 v2 ... kX vX)'],
           'docstring': 'Creates a HashMap data structure'})
    def make_hashmap_func(args: List[datatypes.Base]) -> datatypes.HashMap:
        """
        Builtin 'make-hashmap' function implementation

        :param args: incoming 'make-hashmap' function arguments
        :return: datatypes.HashMap
        """

        return datatypes.HashMap(tuple(args))
        # Let the Collection.__init__() handle hashmap structure construction

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1]],
           'name': 'type',
           'type': 'function',
           'forms': ['(type something)'],
           'docstring': 'Returns something type name'})
    def type_func(args: List[datatypes.Base]) -> datatypes.String:
        """
        Builtin 'type' function implementation

        :param args: incoming 'type' function arguments
        :return: datatypes.String

        TODO: this function could be moved to 'stdlib.nml'
        """

        return datatypes.String(args[0].name)
        # Since base data types can not use String, cast it manually

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': 'odd?',
           'type': 'function',
           'forms': ['(odd? number)'],
           'docstring': 'Whether passed number is odd or not?'})
    def odd_func(args: List[datatypes.Numeric]) -> datatypes.Boolean:
        """
        Builtin 'odd?' function implementation

        :param args: incoming 'empty?' function arguments
        :return: datatypes.Boolean

        TODO: this function could be moved to 'stdlib.nml'
        """

        return datatypes.Boolean(args[0].odd())
        # Since base data types can not use Boolean, cast it manually

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': 'even?',
           'type': 'function',
           'forms': ['(even? number)'],
           'docstring': 'Whether passed number is even or not?'})
    def even_func(args: List[datatypes.Numeric]) -> datatypes.Boolean:
        """
        Builtin 'even?' function implementation

        :param args: incoming 'empty?' function arguments
        :return: datatypes.Boolean

        TODO: this function could be moved to 'stdlib.nml'
        """

        return datatypes.Boolean(args[0].even())
        # Since base data types can not use Boolean, cast it manually

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1]],
           'name': 'not',
           'type': 'function',
           'forms': ['(not something)'],
           'docstring': 'Returns something truth inverted'})
    def not_func(args: List[datatypes.Base]) -> datatypes.Boolean:
        """
        Builtin 'not' function implementation

        :param args: incoming 'not' function arguments
        :return: datatypes.String
        """

        return datatypes.Boolean(not args[0].truthy())
        # Since base data types can not use Boolean, cast it manually

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': '=',
           'type': 'function',
           'forms': ['(= s1 s2 ... sX)'],
           'docstring': 'Returns false once current != next'})
    def eq_func(args: List[datatypes.Base]) -> datatypes.Boolean:
        """
        Builtin '=' function implementation

        :param args: incoming '=' function arguments
        :return: datatypes.Boolean
        """

        _ne = False
        for idx, curr in enumerate(args):
            _next = get(args, idx + 1, None)
            if not _next:
                break
            _ne = curr.hashed() == _next.hashed()
            if not _ne:
                break

        return datatypes.Boolean(_ne)  # once _ne == False, exit function

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '<',
           'type': 'function',
           'forms': ['(< n1 n2 ... nX)'],
           'docstring': 'Returns false once current > than next'})
    def less_than_func(
            args: List[datatypes.Numeric]) -> datatypes.Boolean:
        """
        Builtin '<' function implementation

        :param args: incoming '<' function arguments
        :return: datatypes.Boolean
        """

        _lt = False
        for idx, curr in enumerate(args):
            _next = get(args, idx + 1, None)
            if not _next:
                break
            _lt = curr.reference() < _next.reference()
            if not _lt:
                break

        return datatypes.Boolean(_lt)  # once _lt == False, exit function

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '>',
           'type': 'function',
           'forms': ['(> n1 n2 ... nX)'],
           'docstring': 'Returns false once current < than next'})
    def greater_than_func(
            args: List[datatypes.Numeric]) -> datatypes.Boolean:
        """
        Builtin '>' function implementation

        :param args: incoming '>' function arguments
        :return: datatypes.Boolean
        """

        _gt = False
        for idx, curr in enumerate(args):
            _next = get(args, idx + 1, None)
            if not _next:
                break
            _gt = curr.reference() > _next.reference()
            if not _gt:
                break

        return datatypes.Boolean(_gt)  # once _gt == False, exit function

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '<=',
           'type': 'function',
           'forms': ['(<= n1 n2 ... nX)'],
           'docstring': 'Returns false once current >= than next'})
    def less_than_eq_func(
            args: List[datatypes.Numeric]) -> datatypes.Boolean:
        """
        Builtin '<=' function implementation

        :param args: incoming '>=' function arguments
        :return: datatypes.Boolean
        """

        _lte = False
        for idx, curr in enumerate(args):
            _next = get(args, idx + 1, None)
            if not _next:
                break
            _lte = curr.reference() <= _next.reference()
            if not _lte:
                break

        return datatypes.Boolean(_lte)  # once _lte == False, exit function

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '>=',
           'type': 'function',
           'forms': ['(>= n1 n2 ... nX)'],
           'docstring': 'Returns false once current <= than next'})
    def greater_than_eq_func(
            args: List[datatypes.Numeric]) -> datatypes.Boolean:
        """
        Builtin '>=' function implementation

        :param args: incoming '>=' function arguments
        :return: datatypes.Boolean
        """

        _gte = False
        for idx, curr in enumerate(args):
            _next = get(args, idx + 1, None)
            if not _next:
                break
            _gte = curr.reference() >= _next.reference()
            if not _gte:
                break

        return datatypes.Boolean(_gte)  # once _gte == False, exit function

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1],
                    [Spec.EachArgumentTypeIs, datatypes.String]],
           'name': 'find-mc',
           'type': 'function',
           'forms': ['(find-mc mc-name)'],
           'docstring': 'Returns a Macro by its own LISP name'})
    def find_mc_func(args: List[datatypes.String]
                     ) -> datatypes.Macro or datatypes.Nil:
        """
        Builtin 'find-mc' function implementation

        :param args: incoming 'find-mc' function arguments
        :return: datatypes.Macro or datatypes.Nil
        """

        resolved = BuiltinMacros.resolve(args[0].reference())

        return datatypes.Macro(resolved) if resolved else datatypes.Nil('nil')

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1],
                    [Spec.EachArgumentTypeIs, datatypes.String]],
           'name': 'find-fn',
           'type': 'function',
           'forms': ['(find-fn fn-name)'],
           'docstring': 'Returns a Function by its own LISP name'})
    def find_fn_func(args: List[datatypes.String]
                     ) -> datatypes.Function or datatypes.Nil:
        """
        Builtin 'find-fn' function implementation

        :param args: incoming 'find-fn' function arguments
        :return: datatypes.Function or datatypes.Nil
        """

        resolved = BuiltinFunctions.resolve(args[0].reference())

        return datatypes.Function(resolved) if resolved else datatypes.Nil('nil')

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.ArgumentsTypeChainVariants,
                     [[datatypes.IntegerNumber, datatypes.Base]]]],
           'name': 'repeat',
           'type': 'function',
           'forms': ['(repeat times something)'],
           'docstring': 'Something repeated as many times as specified'})
    def repeat_func(args: List[datatypes.Base]) -> datatypes.Base:
        """
        Builtin 'repeat' function implementation

        :param args: incoming 'repeat' function arguments
        :return: datatypes.Base
        """

        return datatypes.Vector(tuple(args[0] for _ in range(args[0].reference())))

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': 'inc',
           'type': 'function',
           'forms': ['(inc number)'],
           'docstring': 'Returns incremented number'})
    def inc_func(args: List[datatypes.Numeric]) -> datatypes.Numeric:
        """
        Builtin 'inc' function implementation

        :param args: incoming 'inc' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber

        TODO: this function could be moved to 'stdlib.nml'
        """

        number = args[0]

        return datatypes.IntegerNumber(number.reference() + 1) if \
            isinstance(number, datatypes.IntegerNumber) else datatypes.FloatNumber(number.reference() + 1)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': 'dec',
           'type': 'function',
           'forms': ['(dec number)'],
           'docstring': 'Returns decremented number'})
    def dec_func(args: List[datatypes.Numeric]) -> datatypes.Numeric:
        """
        Builtin 'dec' function implementation

        :param args: incoming 'dec' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber

        TODO: this function could be moved to 'stdlib.nml'
        """

        number = args[0]

        return datatypes.IntegerNumber(number.reference() - 1) if \
            isinstance(number, datatypes.IntegerNumber) else datatypes.FloatNumber(number.reference() - 1)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1],
                    [Spec.EachArgumentTypeIs, datatypes.Callable]],
           'name': 'doc',
           'type': 'function',
           'forms': ['(doc callable)'],
           'docstring': 'Allows you to lookup for a callable doc'})
    def doc_func(args: List[datatypes.Callable]) -> datatypes.HashMap:
        """
        Builtin 'doc' function implementation

        :param args: incoming 'doc' function arguments
        :return: datatypes.HashMap
        """

        callable_ = args[0]

        t = callable_.reference().meta.get('type')

        return datatypes.HashMap(
            (datatypes.Keyword('forms'),
             datatypes.Vector(
                 tuple(datatypes.String(_) for _ in callable_.reference().meta.get('forms'))),
             datatypes.Keyword('macro?'), datatypes.Boolean(t == 'macro'),
             datatypes.Keyword('function?'), datatypes.Boolean(t == 'function'),
             datatypes.Keyword('docstring'), datatypes.String(callable_.reference().meta.get('docstring'))))

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '+',
           'type': 'function',
           'forms': ['(+ n1 n2 ... nX)'],
           'docstring': 'Applies "+" operation to passed numbers'})
    def add_func(args: List[datatypes.Numeric]) -> datatypes.Numeric:
        """
        Builtin '+' function implementation

        :param args: incoming '+' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ + x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '-',
           'type': 'function',
           'forms': ['(- n1 n2 ... nX)'],
           'docstring': 'Applies "-" operation to passed numbers'})
    def sub_func(args: List[datatypes.Numeric]) -> datatypes.Numeric:
        """
        Builtin '-' function implementation

        :param args: incoming '-' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ - x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '*',
           'type': 'function',
           'forms': ['(* n1 n2 ... nX)'],
           'docstring': 'Applies "*" operation to passed numbers'})
    def mul_func(args: List[datatypes.Numeric]) -> datatypes.Numeric:
        """
        Builtin '*' function implementation

        :param args: incoming '*' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ * x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '/',
           'type': 'function',
           'forms': ['(/ n1 n2 ... nX)'],
           'docstring': 'Applies "/" operation to passed numbers'})
    def divide_func(args: List[datatypes.Numeric]) -> datatypes.Numeric:
        """
        Builtin '/' function implementation

        :param args: incoming '/' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ / x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': 'mod',
           'type': 'function',
           'forms': ['(mod n1 n2 ... nX)'],
           'docstring': 'Applies "mod" operation to passed numbers'})
    def modulo_func(args: List[datatypes.Numeric]) -> datatypes.Numeric:
        """
        Builtin 'mod' function implementation

        :param args: incoming 'mod' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ % x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.ArgumentsTypeChainVariants, [[datatypes.Function, datatypes.Collection],
                                                       [datatypes.Keyword, datatypes.Collection]]]],
           'name': 'map',
           'type': 'function',
           'forms': ['(map function collection)'],
           'docstring': 'Allows to map collection elements with the passed function'})
    def map_func(args: List[datatypes.Base]) -> datatypes.Vector:
        """
        Builtin 'map' function implementation

        :param args: incoming 'map' function arguments
        :return: datatypes.Vector
        """

        function: datatypes.Function or datatypes.Keyword
        collection: datatypes.Collection

        function, collection = args

        if isinstance(function, datatypes.Keyword):
            k = function
            function = datatypes.Function(
                {'function_name': randstr(),
                 'function_reference': lambda _a_: BuiltinFunctions.get_func(_a_ + [k])})

        return datatypes.Vector(tuple(map(lambda element: function.reference()([element]), collection.items())))

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.ArgumentsTypeChainVariants, [[datatypes.Function, datatypes.Collection],
                                                       [datatypes.Keyword, datatypes.Collection]]]],
           'name': 'filter',
           'type': 'function',
           'forms': ['(filter function collection)'],
           'docstring': 'Allows to filter collection elements with the passed function'})
    def filter_func(args: List[datatypes.Base]) -> datatypes.Vector:
        """
        Builtin 'filter' function implementation

        :param args: incoming 'filter' function arguments
        :return: datatypes.Vector
        """

        function: datatypes.Function or datatypes.Keyword
        coll: datatypes.Collection

        function, coll = args

        if isinstance(function, datatypes.Keyword):
            k = function
            function = datatypes.Function(
                {'function_name': randstr(),
                 'function_reference': lambda _a_: BuiltinFunctions.get_func(_a_ + [k])})

        return datatypes.Vector(tuple(filter(lambda elem: function.reference()([elem]).truthy(), coll.items())))

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.ArgumentsTypeChainVariants, [[datatypes.Base, datatypes.Vector]]]],
           'name': 'py',
           'type': 'function',
           'forms': ['(py instance attr-path)'],
           'docstring': 'Allows to access data-type instance attribute by the passed path'})
    def py_func(args: List[datatypes.Base]) -> datatypes.Base:
        """
        Builtin 'py' function implementation

        :param args: incoming 'py' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        path: datatypes.Vector
        instance, path = args

        final = reduce(lambda e, n: getattr(e, n, None), [instance] + [_.reference() for _ in path.items()])

        if final is None:
            return datatypes.Nil('nil')

        python3_type_to_nanamilang_one = {
            int: datatypes.IntegerNumber, float: datatypes.FloatNumber,
            str: datatypes.String, bool: datatypes.Boolean
        }

        if not type(final) in python3_type_to_nanamilang_one:
            # Assume final is either method or function (but could be wrong)
            def wrapper(function_or_meth):

                # Not every function/method contain __qualname__
                qna = getattr(function_or_meth, '__qualname__', None)

                # Only if function/method contain __qualname__, check
                collection_method = qna.split('.')[0] in ['HashSet', 'Vector', 'HashMap'] if qna else False

                def closed(_args):
                    # Collections methods should return NanamiLang Data Type !
                    if collection_method:
                        return final(*_args)
                    # Expect other methods/functions to return Python 3 results
                    res = final(*_args)
                    return datatypes.Nil('nil') \
                        if res is None else python3_type_to_nanamilang_one.get(type(res))(res)

                return closed
            return datatypes.Function({'function_name': final.__name__, 'function_reference': wrapper(final)})

        return python3_type_to_nanamilang_one.get(type(final))(final) if final is not None else datatypes.Nil('nil')

    #################################################################################################################
