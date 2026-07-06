import argparse


def get_parser():
    parser = argparse.ArgumentParser(
        prog='sample-directive-smartquotes',
        description='Pass input via --text or stdin.',
        epilog='Read the --text docs; see also --2fa and --dry_run.',
    )
    parser.add_argument(
        '--text',
        help='text to encode; combine with --output for files',
    )
    parser.add_argument(
        '--typography',
        help='typography still applies to \'single\' and "double" quotes, '
        'the east--west mid-word dash, and ranges like 10--20',
    )
    return parser
