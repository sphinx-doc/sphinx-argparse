import pytest


@pytest.mark.sphinx('html', testroot='argparse-directive')
def test_bad_index_groups(app, status, warning):
    app.build()
    assert 'failed to parse index-groups as a list' in warning.getvalue()
