import pytest

queries = [
    ('SELEC', ['SELECT']),
    ('sElEc', ['SELECT']),
    ('SELECT', []),
    ('select * fro', ['FROM']),
    ('select * from table order by attr a', ['ASC']),
    ('select column from table o', ['ORDER', 'OFFSET']),
    ('in', ['INSERT'])
]


@pytest.fixture(params=queries)
def query(request):
    return request.param

def test_autocomplete(query):
    from sqlcomplete.language.graphs.postgresql import autocomplete
    q, expected = query
    assert autocomplete(q) == expected
