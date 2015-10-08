"""
Command-line interface to gr1py
"""
from __future__ import print_function
from __future__ import absolute_import
import sys
import argparse
import pprint

from . import __version__
from .form import gr1c, util
from .tstruct import ts_from_expr
from .solve import get_winning_set, check_realizable


def main(args=None):
    parser = argparse.ArgumentParser(prog='gr1py')
    parser.add_argument('FILE', nargs='?',
                        help='input specification file; default format of gr1c')
    parser.add_argument('-V', action='store_true', dest='show_version',
                        help='print version number and exit')
    parser.add_argument('-r', action='store_true', dest='check_realizable',
                        help='check realizability (default action)')
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)

    if args.show_version:
        print('gr1py '+__version__)
        return 0

    if args.FILE is None:
        f = sys.stdin
    else:
        f = open(args.FILE, 'r')

    asd = gr1c.parse(f.read())
    if f is not sys.stdin:
        f.close()

    symtab, exprtab = util.gen_expr(asd)
    exprtab = util.fill_empty(exprtab)
    tsys = ts_from_expr(symtab, exprtab)

    if check_realizable(tsys, exprtab):
        print('Realizable.')
        return 0
    else:
        print('Not realizable.')
        return 3

    return 0
