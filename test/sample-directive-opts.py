import argparse


def get_parser():
    parser = argparse.ArgumentParser(
        prog='sample-directive-opts', description='Support SphinxArgParse HTML testing'
    )
    subparsers = parser.add_subparsers()
    parser_a = subparsers.add_parser('A', help='A subparser')
    parser_a.add_argument('baz', type=int, help='An integer')
    parser_b = subparsers.add_parser('B', help='B subparser')
    parser_b.add_argument('--barg', choices='XYZ', help='A list of choices')

    parser.add_argument('--foo', help='foo help')
    parser.add_argument('foo2', metavar='foo2 metavar', help='foo2 help')
    grp1 = parser.add_argument_group('bar options')
    grp1.add_argument('--bar', help='bar help')
    grp1.add_argument('quux', help='quux help')
    grp2 = parser.add_argument_group('bla options')
    grp2.add_argument('--blah', help='blah help')
    grp2.add_argument('sniggly', help='sniggly help')

    return parser
