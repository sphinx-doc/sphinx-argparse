"""Test HTML output the same way that Sphinx does in test_build_html.py."""

from pathlib import Path

import pytest
from docutils import nodes
from lxml import etree as lxmltree
from sphinx.testing.util import SphinxTestApp

pytest_plugins = 'sphinx.testing.fixtures'

etree_cache: dict[str, str] = {}


@pytest.fixture(scope='session')
def rootdir():
    return Path(__file__).parent.absolute() / 'roots'


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
            assert self.warnings == '', self.status
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
