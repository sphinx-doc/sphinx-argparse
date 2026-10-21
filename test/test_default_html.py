"""Test the HTML builder and check output against XPath."""

import posixpath
from typing import Any

import pytest
from sphinx.util.inventory import InventoryFile

from test.utils.xpath import check_xpath


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
                (".//section[@id='sample-directive-opts-positional-arguments']", ''),
                (".//section/span[@id='get_parser-positional-arguments']", ''),
                (
                    ".//section[@id='sample-directive-opts-positional-arguments']/dl/dt[1]/kbd",
                    'foo2 metavar',
                ),
                (".//section[@id='sample-directive-opts-named-arguments']", ''),
                (".//section/span[@id='get_parser-named-arguments']", ''),
                (
                    ".//section[@id='sample-directive-opts-named-arguments']/dl/dt[1]/kbd",
                    '--foo',
                ),
                (".//section[@id='sample-directive-opts-bar-options']", ''),
                (".//section/span[@id='get_parser-bar-options']", ''),
                (".//section[@id='sample-directive-opts-bar-options']/dl/dt[1]/kbd", '--bar'),
            ],
        ),
        (
            'subcommand-a.html',
            [
                ('.//h1', 'Sample', False),
                ('.//h1', 'Command A'),
                (".//div[@class='highlight']//span", 'usage'),
                ('.//h2', 'Positional Arguments'),
                (".//section[@id='sample-directive-opts-A-positional-arguments']", ''),
                (".//section/span[@id='get_parser-positional-arguments']", ''),
                (
                    ".//section[@id='sample-directive-opts-A-positional-arguments']/dl/dt[1]/kbd",
                    'baz',
                ),
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
        (
            'smartquotes.html',
            [
                ('.//h1', 'Smart quotes'),
                # Option mentions in the description, help, epilog and sub-command
                # help keep both hyphens instead of becoming an en dash (#100)...
                ('.//p/span', '--input'),
                ('.//p/span', '--output'),
                ('.//p/span', '--verbose'),
                ('.//p/span', '--quiet'),
                (".//*[contains(., '–input')]", None),
                (".//*[contains(., '–output')]", None),
                (".//*[contains(., '–verbose')]", None),
                (".//*[contains(., '–quiet')]", None),
                # ...inline literals are not wrapped a second time...
                ('.//p/code/span', '--mode'),
                ('.//p/code/span/span', None),
                # ...and the surrounding prose keeps its typography.
                (".//p[contains(., '“like these”')]", ''),
                (".//p[contains(., 'dash – like this –')]", ''),
                (".//p[contains(., 'east–west')]", ''),
                # Text written in the directive body is reST and is left alone.
                ('.//p', 'keeps typography – an en dash'),
            ],
        ),
        (
            'smartquotes-manpage.html',
            [
                ('.//h1', 'Smart quotes in manpage mode'),
                ('.//h2', 'Description'),
                ('.//section/p/span', '--input'),
                ('.//section/p/span', '--verbose'),
                ('.//dd/p/span', '--output'),
                (".//dd/p[contains(., 'honouring')]/span", '--input'),
                ('.//dd/p', 'Possible choices: copy, move'),
                # The sub-command usage line is command-line syntax throughout.
                ('.//dt/strong', r'run \[-h\] \[--fast\]'),
                (".//*[contains(., '–input')]", None),
                (".//*[contains(., '–output')]", None),
                (".//*[contains(., '–verbose')]", None),
                (".//*[contains(., '–fast')]", None),
                (".//p[contains(., '“like these”')]", ''),
                (".//p[contains(., 'east–west')]", ''),
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


@pytest.mark.sphinx('html', testroot='default-html')
def test_index_is_optional(app, cached_etree_parse):
    app.build()
    index_file = app.outdir / 'index.html'
    assert index_file.exists() is True  # Confirm that the build occurred.

    command_index_file = app.outdir / 'commands-index.html'
    assert command_index_file.exists() is False


def get_inv_command_uri(inv: dict[str, dict[str, Any]], field: str) -> str:
    command = inv['commands:command']
    value = command.get(field, None)
    assert value is not None
    if isinstance(value, tuple):
        return value[2]  # For Sphinx < 9.0.0, see #86

    return value.uri


@pytest.mark.sphinx('html', testroot='default-html')
def test_object_inventory(app, cached_etree_parse):
    app.build()
    inventory_file = app.outdir / 'objects.inv'
    assert inventory_file.exists() is True

    with inventory_file.open('rb') as f:
        inv = InventoryFile.load(f, 'test/path', posixpath.join)

    assert 'test/path/index.html#sample-directive-opts' == get_inv_command_uri(
        inv, 'sample-directive-opts'
    )

    assert 'test/path/subcommand-a.html#sample-directive-opts-A' == get_inv_command_uri(
        inv, 'sample-directive-opts A'
    )

    assert 'test/path/index.html#sample-directive-opts-B' == get_inv_command_uri(
        inv, 'sample-directive-opts B'
    )
