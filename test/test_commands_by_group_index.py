import os
from pathlib import Path

import pytest

from sphinxarg.ext import CommandsByGroupIndex

from .conftest import check_xpath, flat_dict


@pytest.mark.parametrize(
    ('fname', 'expect'),
    flat_dict({
        'index.html': [
            (".//div[@role='navigation']//a[@class='reference internal']", 'Sample'),
            (".//div[@role='navigation']//a[@class='reference internal']", 'Command A'),
            (".//div[@role='navigation']//a[@class='reference internal']", 'Command B'),
            (
                ".//div[@role='navigation']//a[@class='reference internal']",
                'Commands by Group',
            ),
        ],
        'commands-by-group.html': [
            ('.//h1', 'Commands by Group'),
            ('.//tr/td[2]/strong', 'ham in a cone'),
            (
                ".//tr[td[2]/strong/text()='ham in a cone']/following-sibling::tr[1]/td[2]/a/code",  # NoQA: E501
                'sample-directive-opts',
            ),
            (
                ".//tr[td[2]/strong/text()='ham in a cone']/following-sibling::tr[2]/td[2]/a/code",  # NoQA: E501
                'sample-directive-opts B',
            ),
            ('.//tr/td[2]/strong', 'spam'),
            (
                ".//tr[td[2]/strong/text()='spam on a stick']/following-sibling::tr[1]/td[2]/a/code",  # NoQA: E501
                'sample-directive-opts',
            ),
            (
                ".//tr[td[2]/strong/text()='spam on a stick']/following-sibling::tr[2]/td[2]/a/code",  # NoQA: E501
                'sample-directive-opts A',
            ),
            (
                './/tr/td[2]/em',
                '(other)',
                False,
            ),  # Other does not have idxgroups set at all and is not present.
        ],
    }),
)
@pytest.mark.sphinx('html', testroot='command-by-group-index')
def test_commands_by_group_index_html(app, cached_etree_parse, fname, expect):
    app.build()
    check_xpath(cached_etree_parse(app.outdir / fname), fname, *expect)


@pytest.mark.parametrize(
    ('fname', 'expect'),
    flat_dict({
        'index.html': [
            (
                ".//div[@role='navigation']//a[@class='reference internal']",
                'Commands grouped by SomeName',
            ),
        ],
        'commands-groupedby-somename.html': [
            ('.//h1', 'Commands grouped by SomeName'),
            ('.//h1', 'Commands by Group', False),
        ],
    }),
)
@pytest.mark.sphinx(
    'html',
    testroot='command-by-group-index',
    confoverrides={
        'sphinx_argparse_conf': {
            'commands_by_group_index_title': 'Commands grouped by SomeName',
            'commands_by_group_index_file_suffix': 'groupedby-somename',
            'commands_by_group_index_in_toctree': True,
        }
    },
)
def test_by_group_index_overrides_html(app, cached_etree_parse, fname, expect):
    def update_toctree(app):
        indexfile = Path(app.srcdir) / 'index.rst'
        content = indexfile.read_text(encoding='utf8')
        # replace the toctree entry
        content = content.replace('commands-by-group', 'commands-groupedby-somename')
        indexfile.write_text(content)

    update_toctree(app)

    app.build(force_all=True)
    check_xpath(cached_etree_parse(app.outdir / fname), fname, *expect)


@pytest.mark.sphinx('html', testroot='command-by-group-index')
def test_by_group_index_overrides_files_html(app):
    assert os.path.exists(app.outdir / (CommandsByGroupIndex.name + '.html')) is False
    assert os.path.exists(app.outdir / 'commands-groupedby-somename.html') is True
