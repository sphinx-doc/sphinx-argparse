"""Test the HTML builder and check output against XPath."""

import re

import pytest


def check_xpath(etree, fname, path, check, be_found=True):
    nodes = list(etree.xpath(path))
    if check is None:
        assert nodes == [], f'found any nodes matching xpath {path!r} in file {fname}'
        return
    else:
        assert nodes != [], f'did not find any node matching xpath {path!r} in file {fname}'
    if callable(check):
        check(nodes)
    elif not check:
        # only check for node presence
        pass
    else:

        def get_text(node):
            if node.text is not None:
                # the node has only one text
                return node.text
            else:
                # the node has tags and text; gather texts just under the node
                return ''.join(n.tail or '' for n in node)

        rex = re.compile(check)
        if be_found:
            if any(rex.search(get_text(node)) for node in nodes):
                return
            msg = (
                f'{check!r} not found in any node matching path {path} in {fname}: '
                f'{[node.text for node in nodes]!r}'
            )
        else:
            if all(not rex.search(get_text(node)) for node in nodes):
                return
            msg = (
                f'Found {check!r} in a node matching path {path} in {fname}: '
                f'{[node.text for node in nodes]!r}'
            )

        raise AssertionError(msg)


@pytest.mark.parametrize(
    ('fname', 'expect_list'),
    [
        (
            'index.html',
            [
                ('.//h1', 'Sample'),
                ('.//h1', 'blah-blah', False),
                (".//div[@class='highlight']//span", 'usage'),
                ('.//h2', 'Positional Arguments'),
                (".//section[@id='get_parser-positional-arguments']", ''),
                (
                    ".//section[@id='get_parser-positional-arguments']/dl/dt[1]/kbd",
                    'foo2 metavar',
                ),
                (".//section[@id='get_parser-named-arguments']", ''),
                (".//section[@id='get_parser-named-arguments']/dl/dt[1]/kbd", '--foo'),
                (".//section[@id='get_parser-bar-options']", ''),
                (".//section[@id='get_parser-bar-options']/dl/dt[1]/kbd", '--bar'),
            ],
        ),
        (
            'subcommand-a.html',
            [
                ('.//h1', 'Sample', False),
                ('.//h1', 'Command A'),
                (".//div[@class='highlight']//span", 'usage'),
                ('.//h2', 'Positional Arguments'),
                (".//section[@id='get_parser-A-positional-arguments']", ''),
                (".//section[@id='get_parser-A-positional-arguments']/dl/dt[1]/kbd", 'baz'),
            ],
        ),
        (
            'special-characters.html',
            [
                ('.//h1', 'Sample', False),
                ('.//h1', 'Special Characters'),
                ('.//section/dl/dd/p', 'Default:'),
                ('.//section/dl/dd/p/code/span', '420'),
                ('.//section/dl/dd/p/code/span', "'*.rst"),
                ('.//section/dl/dd/p/code/span', r"\['\*.rst',"),
            ],
        ),
        (
            'default-suppressed.html',
            [
                ('.//h1', 'Sample', False),
                ('.//h1', 'Default suppressed'),
                ('.//h2', 'Named Arguments'),
                ('.//section/dl/dd/p', 'Default', False),
            ],
        ),
    ],
)
@pytest.mark.sphinx('html', testroot='default-html')
def test_default_html(app, cached_etree_parse, fname, expect_list):
    app.build()
    print(app.outdir / fname)
    for expect in expect_list:
        check_xpath(cached_etree_parse(app.outdir / fname), fname, *expect)
