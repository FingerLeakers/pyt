import argparse
import os
from datetime import datetime


default_blackbox_mapping_file = os.path.join(
    os.path.dirname(__file__),
    'vulnerability_definitions',
    'blackbox_mapping.json'
)


default_trigger_word_file = os.path.join(
    os.path.dirname(__file__),
    'vulnerability_definitions',
    'all_trigger_words.pyt'
)


def valid_date(s):
    date_format = "%Y-%m-%d"
    try:
        return datetime.strptime(s, date_format).date()
    except ValueError:
        msg = "Not a valid date: '{0}'. Format: {1}".format(s, date_format)
        raise argparse.ArgumentTypeError(msg)


def _add_required_group(parser):
    required_group = parser.add_argument_group('required arguments')
    required_group.add_argument(
        '-f', '--filepath',
        help='Path to the file that should be analysed.',
        type=str
    )
    required_group.add_argument(
        '-r', '--root-directory',
        help='Add project root, this is important when the entry '
             'file is not at the root of the project.',
        type=str,
        metavar='DIR_TO_ANALYZE'
    )


def _add_optional_group(parser):
    optional_group = parser.add_argument_group('optional arguments')

    optional_group.add_argument(
        '-a', '--adaptor',
        help='Choose a web framework adaptor: '
             'Flask(Default), Django, Every or Pylons',
        type=str
    )
    optional_group.add_argument(
        '-b', '--baseline',
        help='Path of a baseline report to compare against '
             '(only JSON-formatted files are accepted)',
        type=str,
        default=False,
        metavar='BASELINE_JSON_FILE',
    )
    optional_group.add_argument(
        '-j', '--json',
        help='Prints JSON instead of report.',
        action='store_true',
        default=False
    )
    optional_group.add_argument(
        '-m', '--blackbox-mapping-file',
        help='Input blackbox mapping file.',
        type=str,
        default=default_blackbox_mapping_file
    )
    optional_group.add_argument(
        '-t', '--trigger-word-file',
        help='Input file with a list of sources and sinks',
        type=str,
        default=default_trigger_word_file
    )


def _add_print_group(parser):
    print_group = parser.add_mutually_exclusive_group()
    print_group.add_argument(
        '-trim', '--trim-reassigned-in',
        help='Trims the reassigned list to the vulnerability chain.',
        action='store_true',
        default=True
    )
    print_group.add_argument(
        '-i', '--interactive',
        help='Will ask you about each vulnerability chain and blackbox nodes.',
        action='store_true',
        default=False
    )


def _check_required_and_mutually_exclusive_args(parser, args):
    if args.filepath is None and args.git_repos is None:
        parser.error('one of the arguments -f/--filepath -gr/--git-repos is required')
    if args.filepath and args.git_repos:
        parser.error('argument -f/--filepath: not allowed with argument -gr/--git-repos')
    if args.trim_reassigned_in and args.interactive:
        parser.error('argument -i/--interactive: not allowed with argument -trim/--trim-reassigned-in')


def parse_args(args):
    if len(args) == 0:
        args.append('-h')
    parser = argparse.ArgumentParser(prog='python -m pyt')
    parser._action_groups.pop()
    _add_required_group(parser)
    _add_optional_group(parser)
    _add_print_group(parser)

    args = parser.parse_args(args)
    _check_required_and_mutually_exclusive_args(
        parser,
        args
    )
    return args