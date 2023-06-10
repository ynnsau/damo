# SPDX-License-Identifier: GPL-2.0

"""
Show status of DAMON.
"""

import _damon
import _damon_args

import damo_stat_kdamonds

def set_argparser(parser):
    parser.add_argument('target', choices=['kdamonds'],
            help='what status to show')
    parser.add_argument('--detail', action='store_true', default=False,
            help='show detailed status')
    parser.add_argument('--json', action='store_true', default=False,
            help='print output in json format')
    parser.add_argument('--raw', action='store_true', default=False,
            help='print raw numbers')
    _damon_args.set_common_argparser(parser)
    return parser

def main(args=None):
    if not args:
        parser = set_argparser(parser)
        args = parser.parse_args()

    _damon.ensure_root_and_initialized(args)

    if args.target == 'kdamonds':
        if not args.detail:
            damo_stat_kdamonds.update_pr_kdamonds_summary(args.json, args.raw)
        else:
            damo_stat_kdamonds.update_pr_kdamonds(args.json, args.raw)

if __name__ == '__main__':
    main()
