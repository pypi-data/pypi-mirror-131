#!python

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

"""NanamiLang REPL"""

import argparse
import atexit
import os
import readline
import sys
import time

import nanamilang.datatypes
import nanamilang.formatter
from nanamilang.builtin import BuiltinFunctions, BuiltinMacros
from nanamilang import program, __version_string__, __author__, __project_license__

history_file_path = os.path.join(
    os.path.expanduser("~"), ".nanamilang_history")
try:
    readline.set_history_length(1000)
    readline.read_history_file(history_file_path)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, history_file_path)

readline.parse_and_bind("tab: complete")
readline.parse_and_bind('set blink-matching-paren on')

repl_exit_function_names: list = ['exit!', 'bye!', 'exit', 'bye', 'quit', 'quit!']
builtin_names = BuiltinFunctions.names() + BuiltinMacros.names() + repl_exit_function_names


def complete(t: str, s: int):
    """NanamiLang REPL complete() function for GNU readline"""
    return ([name for name in builtin_names if name.startswith(t)] + [None]).__getitem__(s)


readline.set_completer(complete)


def print_highlighted_error(ne, indent) -> None:
    """
    NanamiLang REPL, highlight invalid token in src
    (one line src only)
    """

    c = ne.position()[1]

    an_indentation = ' ' * (c - 2 + indent)
    print(an_indentation, '^\n\b', an_indentation, ne.format())


def check_whether_user_wants_to_exit(p: program.Program) -> None:
    """
    1. p.tokenized() contains only ONE token:
    2. that token is a type() of Token.Identifier
    3. that token dt().origin() equals to something from 'valid'

    :param p: current program instance initialized after user input
    """

    if len(p.tokenized()) == 1:
        first = p.tokenized()[0]
        if first.type() == 'Identifier':
            if first.dt().origin() in repl_exit_function_names:
                name = first.dt().origin()
                print(f'Type ({name}) or press "Control+D" or "Control+C" to exit REPL')


def main():
    """NanamiLang REPL Main function"""

    parser = argparse.ArgumentParser('NanamiLang REPL')
    parser.add_argument('--no-greeting',
                        help='Greeting can be disabled',
                        action='store_true', default=False)
    parser.add_argument('--include-traceback',
                        help='Include exception traceback',
                        action='store_true', default=False)
    parser.add_argument('--show-measurements',
                        help='In addition to (measure...)',
                        action='store_true', default=False)
    parser.add_argument('--license',
                        help='Show license of NanamiLang',
                        action='store_true', default=False)
    parser.add_argument('--version',
                        help='Show version of NanamiLang',
                        action='store_true', default=False)

    args = parser.parse_args()

    # GNU GPL v2 may require these options

    if args.version:
        print('NanamiLang', __version_string__)
        sys.exit(0)

    if args.license:
        print('License is', __project_license__)
        sys.exit(0)

    # Collect Python 3 version into single string
    p_ver = '.'.join([str(sys.version_info.major),
                      str(sys.version_info.minor),
                      str(sys.version_info.micro)])

    # First of all, good boys always should start with the greeting
    print('NanamiLang', __version_string__, 'by', __author__, 'on Python', p_ver)
    if not args.no_greeting:
        print('History path is:', history_file_path)
        print('Type (doc function-or-macro) to see function-or-macro documentation')
        print('Type (exit!), (bye!), press "Control+D" or "Control+C" to exit REPL')

    # Since nanamilang.builtin.BuiltinFunctions provides install() method,
    # we can install functions to help the user to exit NanamiLang REPL in easy way!
    for _ in repl_exit_function_names:
        BuiltinFunctions.install(
            {
                'name': _, 'type': 'function',
                'sample': '(exit!)', 'docstring': 'Exit NanamiLang REPL'
            },
            lambda _: sys.exit(0)
        )

    # Here, we finally can start the main loop, hooray!
    while True:
        try:
            # Fist, let the user to enter something they want
            src = input("USER> ")
            __repl_got_input__ = time.perf_counter()
            # Skip program evaluation in case of the empty input
            if not src:
                continue
            p = program.Program(src)
            # Show tips in case user want to exit NanamiLang REPL script
            check_whether_user_wants_to_exit(p)
            # Call program.evaluate() to evaluate user's program source code
            results = p.evaluate()
            # Iterate through results, if some of them - NException, handle it
            for (dt, _) in results:
                if isinstance(dt, nanamilang.datatypes.NException):
                    if not args.include_traceback:
                        print(dt.format())
                    else:
                        print('\n\b', dt.format(include_traceback=args.include_traceback))
                else:
                    print(dt.format())
            # If '--show-measurements' has been passed, show all the available measurements
            if args.show_measurements:
                stats = {'[REPL]': time.perf_counter() - __repl_got_input__}
                # Sadly, we do not count dictionary update operation
                stats.update(p.measurements())
                # Also we don't count: iterating, unpacking, rounding, formatting, printing
                print(*[f'{stat} took {took:.5f} seconds.' for stat, took in stats.items()])
        except (EOFError, KeyboardInterrupt):
            print("Bye for now!")
            break

    return 0

    # Return 0 to system and exit NanamiLang REPL script after playing around with NanamiLang


if __name__ == "__main__":
    main()
