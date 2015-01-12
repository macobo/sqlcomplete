import pytest
from sqlcomplete.language.graphs.postgresql import autocomplete

queries = [
    ('SELEC', ['SELECT']),
    ('sElEc', ['SELECT']),
    ('select * fro', ['FROM'])
]


@pytest.fixture(params=queries)
def query(request):
    return request.param


def test_autocomplete(query):
    q, expected = query
    assert autocomplete(q) == expected
