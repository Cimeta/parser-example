import logging
import re
from pathlib import Path

from common import setup_logger, get_encrypted_value
from parser import get_tags, get_messages

_log = logging.getLogger(__name__)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Tg channel data parser."
    )

    parser.add_argument(
        "-hash", "--api_hash",
        required=False,
        help="API Hash.",
    )

    parser.add_argument(
        "-id", "--api_id",
        required=False,
        help="API ID.",
    )

    parser.add_argument(
        "-c", "--channel_name",
        required=False,
        help="Group name to parse.",
    )

    parser.add_argument(
        "--debug",
        action='store_true',
        help="Run program in debug mode.",
    )

    subparsers = parser.add_subparsers(required=True)

    parser_messages = subparsers.add_parser('messages')
    parser_messages.set_defaults(func=messages)
    parser_messages.add_argument(
        "-t", "--tags",
        default=None,
        help='Put tag names in double quotes ("tag") separated with commas ("tag1,tag2,tag3")',
    )
    parser_messages.add_argument(
        "-s", "--start",
        default=None,
        type=date_type,
        help='Date from which messages should be processed. Date format dd/mm/yyyy.',
    )
    parser_messages.add_argument(
        "-e", "--end",
        default=None,
        type=date_type,
        help='End date to which messages should be processed. Date format dd/mm/yyyy.',
    )

    parser_tags = subparsers.add_parser('tags')
    parser_tags.set_defaults(func=tags)

    args = parser.parse_args()

    here = Path(__file__).parents[2].resolve()
    log_file = here / "parser_log_file.log"

    level = 'INFO'
    if args.debug:
        level = 'DEBUG'

    setup_logger(log_file=log_file, level=level)
    _log.debug('Log file - %s', log_file)

    args.api_hash = get_arg_values(args.api_hash, 'API_HASH')
    args.api_id = get_arg_values(args.api_id, 'API_ID')
    args.channel_name = get_arg_values(args.channel_name, 'CHANNEL_NAME')

    try:
        _log.debug('Start parsing')
        args.func(args)
    except Exception:
        _log.exception('Unhandled exception occur')
        raise


def date_type(arg):
    pattern = r'\d\d?/\d\d?/\d\d\d\d'
    if not bool(re.match(pattern, arg)):
        raise ValueError(f'Incorrect date format for {arg}, should be dd/mm/yyyy')
    return arg


def get_arg_values(arg: str, variable_name: str) -> str:
    if arg is None:
        arg = get_encrypted_value(variable_name)
    if arg is None:
        raise ValueError(f'Cannot define arg {variable_name}')
    return arg


def tags(args):
    _log.debug('Start tag extraction')
    get_tags(channel_name=args.channel_name, api_id=int(args.api_id), api_hash=args.api_hash)
    _log.debug('Tag extraction finished')


def messages(args):
    _log.debug('Start message extraction')
    get_messages(tags=args.tags,
                 start=args.start,
                 end=args.end,
                 api_id=args.api_id,
                 api_hash=args.api_hash,
                 channel_name=args.channel_name)
    _log.debug('Message extraction finished')


if __name__ == "__main__":
    main()
