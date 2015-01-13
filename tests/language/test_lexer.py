# Tests for the language lexer
import pytest
from sqlcomplete.language.lexer import *


def test_partitioning():
    language = """\
hello
world
    test 1 2
        3 4
        # comment
# anothercomment
        5 6
    5

test
"""
    assert partition(language) == [
        ('hello', []),
        ('world', [
            ('test 1 2', [('3 4', []), ('5 6', [])]),
            ('5', [])
        ]),
        ('test', [])
    ]
    assert rejoin_partitioned(('test 1 2', [('3 4', []), ('5 6', [])])) == (
        'test 1 2 3 4 5 6')


def test_lex_keywords():
    assert lex('SELECT FROM') == (Keyword('SELECT'), Keyword('FROM'))
    assert lex('*') == (Keyword('*'),)
    assert lex('SELECT ( WORD ) FROM') == (
        Keyword('SELECT'),
        Keyword('('),
        Keyword('WORD'),
        Keyword(')'),
        Keyword('FROM'))


def test_lex_variables():
    assert lex('SELECT thing FROM')[1] == Variable('thing')


def test_lex_optional():
    assert lex('SELECT [ ALL B ]') == (
        Keyword('SELECT'),
        Optional((Keyword('ALL'), Keyword('B'))))
    assert lex('[ A ]') == (Optional((Keyword('A'),)), )


def test_lex_either():
    assert lex('SELECT { A B | C | D }') == (
        Keyword('SELECT'),
        Either((
            (Keyword('A'), Keyword('B')),
            (Keyword('C'),),
            (Keyword('D'),))))

def test_lex_nested_either():
    assert lex('{ A | { B | C } }') == (
        Either((
            (Keyword('A'),),
            (Either((
                (Keyword('B'),),
                (Keyword('C'),))),),
            )),)


def test_casual_either():
    assert lex('A | B') == (Either(((Keyword('A'),), (Keyword('B'),))),)
    assert lex('A | B | C') == (
        Either((
            (Keyword('A'),),
            (Keyword('B'),),
            (Keyword('C'),))),)


def test_lex_many_times():
    assert lex('SELECT [, ...]') == (ManyTimes(Keyword('SELECT')),)


def test_lex_nested_complex():
    result = lex('''\
SELECT [ ALL | DISTINCT [ ON ( expression [, ...] ) ] ]
    { * | expression [ [ AS ] output_name ] } [, ...]''')

    assert len(result) == 3
    assert result[0] == Keyword('SELECT')
    assert result[1] == Optional((
        Either(((Keyword('ALL'),), (Keyword('DISTINCT'),))),
        Optional((
            Keyword('ON'),
            Literal('('),
            ManyTimes(Variable('expression')),
            Literal(')')))
    ))
    assert result[2] == ManyTimes(Either((
        (Keyword('*'),),
        (Variable('expression'),
            Optional((
                Optional((Keyword('AS'),)),
                Variable('output_name')))))))


@pytest.mark.xfail
def test_compress_sequencial_keywords():
    assert lex('SELECT ALL vars IS A') == (
        Keyword('SELECT ALL'),
        Variable('vars'),
        Keyword('IS A'))


def test_preprocess():
    language = """\
something is
    NUMBER | STATEMENT

others are
    THING
    REST
"""
    result = preprocess(language)
    assert result == {
        'something': (Either((
            (Keyword('NUMBER'),),
            (Keyword('STATEMENT'),))),),
        'others': (Either((
            (Keyword('THING'),),
            (Keyword('REST'),)
        )),)
    }
    assert result['something'] == lex('NUMBER | STATEMENT')
    assert result['others'] == (
        Either((lex('THING'), lex('REST'))),
    )
