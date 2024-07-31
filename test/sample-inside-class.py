import argparse


desc = 'Test parsing of Argparse instances inside classes'

class Foo:
    parser = argparse.ArgumentParser(prog=f'{__name__}-foo',
                                     description=desc)
    parser.add_argument('--foo-arg1', help='foo-arg1 help')
    parser.add_argument('--foo-arg2', help='foo-arg2 help')


    class Bar:
        parser = argparse.ArgumentParser(prog=f'{__name__}-foo-bar',
                                         description=desc)
        parser.add_argument('--foo-bar-arg1', help='foo-bar-arg1 help')
        parser.add_argument('--foo-bar-arg2', help='foo-bar-arg2 help')
