"""Test the HTML builder with sphinx-argparse conf options and check output against XPath."""

import pytest

from .conftest import check_xpath, flat_dict


@pytest.mark.parametrize(
    "fname,expect",
    flat_dict(
        {
            'index.html': [
                (".//h1", 'Sample'),
                (".//h2", 'Sub-commands'),
                (".//h3", 'sample-directive-opts A'),  # By default, just "A".
                (".//h3", 'sample-directive-opts B'),
            ],
        }
    ),
)
@pytest.mark.sphinx(
    'html',
    testroot='conf-opts-html',
    confoverrides={
        'sphinx_argparse_conf': {
            "full_subcommand_name": True,
        }
    },
)
def test_full_subcomand_name_html(app, cached_etree_parse, fname, expect):
    app.build()
    print(app.outdir / fname)
    check_xpath(cached_etree_parse(app.outdir / fname), fname, *expect)
