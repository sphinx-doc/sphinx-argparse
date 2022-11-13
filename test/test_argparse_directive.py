import pytest


@pytest.mark.sphinx('html', testroot='argparse-directive')
def test_bad_idxgroups(app, status, warning):
    app.build()
    assert 'failed to parse idxgroups as a list' in warning.getvalue()
