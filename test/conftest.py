"""Test HTML output the same way that Sphinx does in test_build_html.py."""
import re
from itertools import chain, cycle
from pathlib import Path
from typing import Dict

import pytest
from docutils import nodes
from lxml import etree as lxmltree
from sphinx.testing.path import path as sphinx_path
from sphinx.testing.util import SphinxTestApp

pytest_plugins = "sphinx.testing.fixtures"

etree_cache: Dict[str, str] = {}


@pytest.fixture(scope='session')
def rootdir():
    return sphinx_path(__file__).parent.abspath() / 'roots'


class SphinxBuilder:
    def __init__(self, app: SphinxTestApp, src_path: Path):
        self.app = app
        self._src_path = src_path

    @property
    def src_path(self) -> Path:
        return self._src_path

    @property
    def out_path(self) -> Path:
        return Path(self.app.outdir)

    def build(self, assert_pass=True):
        self.app.build()
        if assert_pass:
            assert self.warnings == "", self.status
        return self

    @property
    def status(self):
        return self.app._status.getvalue()

    @property
    def warnings(self):
        return self.app._warning.getvalue()

    def get_doctree(self, docname: str, post_transforms: bool = False) -> nodes.document:
        assert self.app.env is not None
        doctree = self.app.env.get_doctree(docname)
        if post_transforms:
            self.app.env.apply_post_transforms(doctree, docname)
        return doctree


@pytest.fixture(scope='module')
def cached_etree_parse():
    def parse(fname):
        if fname in etree_cache:
            return etree_cache[fname]
        with (fname).open('r') as fp:
            data = fp.read().replace('\n', '')
            etree = lxmltree.HTML(data)
            etree_cache.clear()
            etree_cache[fname] = etree
            return etree

    yield parse
    etree_cache.clear()


def flat_dict(d):
    return chain.from_iterable([zip(cycle([fname]), values) for fname, values in d.items()])


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
        else:
            if all(not rex.search(get_text(node)) for node in nodes):
                return

        raise AssertionError(f'{check!r} not found in any node matching path {path} in {fname}: {[node.text for node in nodes]!r}')
