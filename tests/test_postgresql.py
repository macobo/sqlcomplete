import pytest

queries = [
    # Keyword completion
    ('SELEC', ['SELECT']),
    ('sElEc', ['SELECT']),
    ('SELECT', []),
    ('select * fro', ['FROM']),
    ('select * from table a', ['AS']),
    ('select * from table order by attr as', ['ASC']),
    ('select column from table o', ['ORDER', 'OFFSET']),
    ('in', ['INSERT']),
    # recursion
    ('select * from (s', ['SELECT']),
    ('select * from (select * from table) a', ['AS']),
    # variable matching
    ('select col', ['column']),
    ('select * from tab', ['table1', 'table2'])
]


@pytest.fixture(params=queries)
def query(request):
    return request.param


@pytest.fixture
def autocomplete():
    from sqlcomplete.postgresql import Completer
    completer = Completer()

    completer.set('table_name', ['table1', 'table2', 'fancytable'])
    completer.set('column_name', ['column', 'intcolumn'])
    return completer.autocomplete


def test_autocomplete(query, autocomplete):
    q, expected = query
    assert autocomplete(q) == expected
