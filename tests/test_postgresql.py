import pytest

variables = {
    'table_name': ['table1', 'table2', 'fancytable'],
    'column_name': ['column', 'intcolumn']
}

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
    ('insert into table1 (column) def', ['DEFAULT']),
    ('insert into table1 valu', ['VALUES']),
    ('insert into table1 s', ['SELECT']),
    ('insert into table1 select * from fan', ['fancytable']),
    ('insert into table1 select * from fancytable ret', ['RETURNING']),

    # ALTER TABLE
    ('alt', ['ALTER']),
    ('alter table t', ['table1', 'table2']),
    ('alter table table1 enable r', ['REPLICA', 'RULE']),
]


@pytest.fixture(params=queries)
def query(request):
    return request.param


@pytest.fixture
def autocomplete():
    from sqlcomplete.postgresql import Completer
    completer = Completer()

    for key, values in variables.items():
        completer.set(key, values)
    return completer.autocomplete


def test_autocomplete(query, autocomplete):
    q, expected = query
    assert autocomplete(q) == expected
