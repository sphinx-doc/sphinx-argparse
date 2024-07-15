"""Test the HTML builder with sphinx-argparse conf options and check output against XPath."""

import pytest

from test.utils.xpath import check_xpath


@pytest.mark.parametrize(
    ('fname', 'expect'),
    [
        ('index.html', ('.//h1', 'Sample')),
        ('index.html', ('.//h2', 'Sub-commands')),
        ('index.html', ('.//h3', 'sample-directive-opts A')),  # By default, just "A".
        ('index.html', ('.//h3', 'sample-directive-opts B')),
    ],
)
@pytest.mark.sphinx(
    'html',
    testroot='conf-opts-html',
    confoverrides={
        'sphinx_argparse_conf': {
            'full_subcommand_name': True,
        }
    },
)
def test_full_subcomand_name_html(app, cached_etree_parse, fname, expect):
    app.build()
    print(app.outdir / fname)
    check_xpath(cached_etree_parse(app.outdir / fname), fname, *expect)
