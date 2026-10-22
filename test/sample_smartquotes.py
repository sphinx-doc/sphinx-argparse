import argparse


def get_parser():
    parser = argparse.ArgumentParser(
        prog='sample-smartquotes',
        description='Read --input and write the result to --output.',
        epilog=(
            '--verbose can be repeated. Quotes "like these", a dash -- like this -- '
            'and east--west keep their typography.'
        ),
    )
    parser.add_argument(
        'mode',
        choices=['copy', 'move'],
        help='What to do with the --input file.',
    )
    parser.add_argument('--input', help='Source file; see also --output.')
    parser.add_argument(
        '--output',
        help='Target file. Markup such as ``--mode`` is left as it is.',
    )
    parser.add_argument(
        '--level',
        choices=['low', 'high'],
        help='Verbosity, with no option mentioned.',
    )
    parser.add_argument('--verbose', action='store_true', help='Say more.')

    subparsers = parser.add_subparsers(dest='command')
    run = subparsers.add_parser('run', help='Run it, honouring --input.')
    run.add_argument('--fast', action='store_true', help='Skip checks; implies --quiet.')

    return parser
