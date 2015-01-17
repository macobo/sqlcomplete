import pytest

queries = [
    ('SELEC', ['SELECT']),
    ('sElEc', ['SELECT']),
    ('SELECT', []),
    ('select * fro', ['FROM']),
    ('select * from table a', ['AS']),
    ('select * from table order by attr as', ['ASC']),
    ('select column from table o', ['ORDER', 'OFFSET']),
    ('in', ['INSERT']),
    ('select * from (s', ['SELECT']),
    ('select * from (select * from table) a', ['AS'])
]


@pytest.fixture(params=queries)
def query(request):
    return request.param


def test_autocomplete(query):
    from sqlcomplete.postgresql import autocomplete
    q, expected = query
    assert autocomplete(q) == expected
