import pytest

queries = [
    # SELECT
    # Keyword completion
    ('SELEC', ['SELECT']),
    ('sElEc', ['SELECT']),
    ('SELECT', []),
    ('select * f', ['FROM']),
    ('select * fro', ['FROM']),
    ('select * from table a', ['AS']),
    ('select * from table order by attr as', ['ASC']),
    ('select column from table o', ['ORDER', 'OFFSET']),
    # recursion
    ('select * from (s', ['SELECT']),
    ('select * from (select * from table) a', ['AS']),
    ('select * from (select * from t', ['table1', 'table2']),
    # variable matching
    ('select col', ['column']),
    ('select * from tab', ['table1', 'table2']),

    # INSERT
    # Keyword completion
    ('in', ['INSERT']),
    # variable matching
    ('insert into t', ['table1', 'table2']),
    ('insert into table1 (c', ['column']),
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
