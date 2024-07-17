import argparse


def get_parser():
    parser = argparse.ArgumentParser(
        prog='sample-directive-special',
        description='Support SphinxArgParse HTML testing (with defaults)',
    )

    parser.add_argument(
        '--some-int',
        help='Regular scalar input with default value',
        default=420,
        type=int,
    )
    parser.add_argument(
        '--some-text',
        help='Scalar text input',
        default='*.rst _txt_ **strong** *italic* ``code``',
    )
    parser.add_argument(
        '--list-text',
        help='List input for some bits of text',
        default=['*.rst', '_txt_', '**strong**', '*italic*', '``code``'],
        nargs='+',
    )
    parser.add_argument(
        '--some-text-empty-default',
        help='Scalar text input',
        default='',
    )

    return parser
