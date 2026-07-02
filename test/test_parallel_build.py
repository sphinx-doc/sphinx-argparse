"""Regression test for parallel reads (see issue with merge_domaindata).

Sphinx only performs a parallel *read* when there are more than 5 source
documents and ``parallel > 1`` (see ``Builder.read`` in sphinx/builders/__init__.py).
The test root therefore needs at least 6 documents with ``argparse``
directives so that reading is actually split across worker processes and
``ArgParseDomain.merge_domaindata`` is exercised.
"""

import pytest

from sphinxarg.ext import ArgParseDomain


@pytest.mark.sphinx('dummy', testroot='parallel-build', parallel=2)
def test_parallel_read_merges_domain_data(app):
    # Building must not raise NotImplementedError / KeyError from
    # sphinx.util.parallel when merging results from worker processes.
    app.build()
    assert app._warning.getvalue() == ''

    domain = app.env.domains[ArgParseDomain.name]
    full_commands = {entry[0] for entry in domain.get_objects()}
    expected = {f'page{i}-command' for i in range(1, 7)}
    assert full_commands == expected

    # Each command should only be merged in once, from the worker that read it.
    assert len(list(domain.get_objects())) == len(expected)
