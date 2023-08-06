"""NanamiLang Fn Handler"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from copy import deepcopy

from nanamilang import datatypes
from nanamilang.spec import Spec


class Fn:
    """NanamiLang Fn Handler"""

    _token_class = None
    _function_body_token_or_form: list
    _environment: dict = None
    _recursive_evaluate_function = None
    _function_name: str = None
    _function_parameters: list = None
    _number_of_function_params: int = None

    def __init__(self,
                 token_class,
                 function_body_tof: list,
                 environment: dict,
                 recursive_evaluate_function,
                 function_name: str,
                 function_parameters: list) -> None:
        """NanamiLang Fn Handler, initialize a new instance"""

        self._environment = deepcopy(environment)
        self._function_name = function_name
        self._recursive_evaluate_function = recursive_evaluate_function
        self._token_class = token_class
        self._function_parameters = function_parameters
        self._number_of_function_params = len(self._function_parameters)

        self._function_body_token_or_form = deepcopy(function_body_tof) \
            if isinstance(function_body_tof, list)\
            else [token_class(token_class.Identifier, 'identity'), deepcopy(function_body_tof)]

    def env(self) -> dict:
        """NanamiLang Fn Handler, self._environment getter"""

        return self._environment

    def generate_meta__forms(self) -> list:
        """NanamiLang Fn Handler, generate function meta data :: forms"""

        return [f'({self._function_name} {" ".join([n for (n, _) in self._function_parameters])})']

    def handle(self, args: tuple) -> datatypes.Base:
        """NanamiLang Fn Handler, handle function evaluation"""

        Spec.validate(
            self._function_name, args, [[Spec.ArityIs, self._number_of_function_params]]
        )

        for (left, right), arg in zip(self._function_parameters, args):
            self._environment.update(
                zip(right, arg.items())
                if isinstance(arg, datatypes.Vector) and isinstance(right, list) else {left: arg}
            )

        return self._recursive_evaluate_function(self._environment, self._function_body_token_or_form)
