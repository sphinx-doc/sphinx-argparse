"""Test the HTML builder and check output against XPath."""

import posixpath

import pytest
from sphinx.ext.intersphinx import INVENTORY_FILENAME
from sphinx.util.inventory import Inventory, InventoryFile

from .conftest import check_xpath, flat_dict


@pytest.mark.parametrize(
    "fname,expect",
    flat_dict(
        {
            'index.html': [
                (".//h1", 'Sample'),
                (".//h1", 'blah-blah', False),
                (".//div[@class='highlight']//span", 'usage'),
                (".//h2", 'Positional Arguments'),
                (".//section[@id='sample-directive-opts-positional-arguments']", ''),
                (".//section/span[@id='positional-arguments']", ''),
                (".//section[@id='sample-directive-opts-positional-arguments']/dl/dt[1]/kbd", 'foo2 metavar'),
                (".//section[@id='sample-directive-opts-named-arguments']", ''),
                (".//section/span[@id='named-arguments']", ''),
                (".//section[@id='sample-directive-opts-named-arguments']/dl/dt[1]/kbd", '--foo'),
                (".//section[@id='sample-directive-opts-bar-options']", ''),
                (".//section[@id='sample-directive-opts-bar-options']/dl/dt[1]/kbd", '--bar'),
                (".//section[@id='link-check']/p[1]/a[@href='#sample-directive-opts-A']", ''),
            ],
            'subcommand-a.html': [
                (".//h1", 'Sample', False),
                (".//h1", 'Command A'),
                (".//div[@class='highlight']//span", 'usage'),
                (".//h2", 'Positional Arguments'),
                (".//section[@id='sample-directive-opts-A-positional-arguments']", ''),
                (".//section/span[@id='positional-arguments']", ''),
                (".//section[@id='sample-directive-opts-A-positional-arguments']/dl/dt[1]/kbd", 'baz'),
            ],
        }
    ),
)
@pytest.mark.sphinx('html', testroot='default-html')
def test_default_html(app, cached_etree_parse, fname, expect):
    app.build()
    print(app.outdir / fname)
    check_xpath(cached_etree_parse(app.outdir / fname), fname, *expect)


@pytest.mark.sphinx('html', testroot='default-html')
def test_index_is_optional(app, cached_etree_parse):
    app.build()
    index_file = app.outdir / "index.html"
    assert index_file.exists() is True  # Confirm that the build occurred.

    command_index_file = app.outdir / "commands-index.html"
    assert command_index_file.exists() is False


@pytest.mark.sphinx('html', testroot='default-html')
def test_object_inventory(app, cached_etree_parse):
    app.build()
    inventory_file = app.outdir / INVENTORY_FILENAME
    assert inventory_file.exists() is True

    with inventory_file.open('rb') as f:
        inv: Inventory = InventoryFile.load(f, 'test/path', posixpath.join)

    assert 'sample-directive-opts' in inv.get('commands:command')
    assert 'test/path/index.html#sample-directive-opts' == inv['commands:command']['sample-directive-opts'][2]

    assert 'sample-directive-opts A' in inv.get('commands:command')
    assert 'test/path/subcommand-a.html#sample-directive-opts-A' == inv['commands:command']['sample-directive-opts A'][2]

    assert 'sample-directive-opts B' in inv.get('commands:command')
    assert 'test/path/index.html#sample-directive-opts-B' == inv['commands:command']['sample-directive-opts B'][2]
