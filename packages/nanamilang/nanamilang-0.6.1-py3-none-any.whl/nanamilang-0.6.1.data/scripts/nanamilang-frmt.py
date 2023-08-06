#!python

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

"""NanamiLang Format"""

import argparse
import os
import sys

from nanamilang.program import Program
from nanamilang import __version_string__, __project_license__


def main():
    """NanamiLang Format Main function"""

    parser = argparse.ArgumentParser('NanamiLang Formatter')
    parser.add_argument('program',
                        help='Path to source code', nargs='?', default='/dev/stdin')
    parser.add_argument('--license',
                        help='Show license of NanamiLang', action='store_true', default=False)
    parser.add_argument('--version',
                        help='Show version of NanamiLang', action='store_true', default=False)
    args = parser.parse_args()

    if args.version:
        print('NanamiLang', __version_string__)
        sys.exit(0)

    if args.license:
        print('License is', __project_license__)
        sys.exit(0)

    assert args.program
    assert os.path.exists(args.program)

    with open(args.program, encoding='utf-8') as r:
        inp = r.read()

    assert inp, 'A program source code could not be an empty string'

    print(Program(inp).format(), end='')

    return 0

    # Return exit code to system and exit NanamiLang Formatter script after formatting a source


if __name__ == "__main__":
    sys.exit(main())
