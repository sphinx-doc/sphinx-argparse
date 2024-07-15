from argparse import ArgumentParser


def get_parser():
    parser = ArgumentParser(
        prog='sample-default-suppressed', description='Test suppression of version default'
    )
    parser.add_argument(
        '--version', help='print version number', action='version', version='1.2.3'
    )
    return parser
