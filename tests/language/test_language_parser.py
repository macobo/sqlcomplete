# Tests for the language parser
import pytest
from sqlcomplete.language.parser import *


def test_parse_keywords():
    assert parse('SELECT FROM') == (Keyword('SELECT'), Keyword('FROM'))
    assert parse('*') == (Keyword('*'),)
    assert parse('SELECT ( WORD ) FROM') == (
        Keyword('SELECT'),
        Keyword('('),
        Keyword('WORD'),
        Keyword(')'),
        Keyword('FROM'))


def test_parse_variables():
    assert parse('SELECT thing FROM')[1] == Variable('thing')


def test_parse_optional():
    assert parse('SELECT [ ALL B ]') == (
        Keyword('SELECT'),
        Optional((Keyword('ALL'), Keyword('B'))))
    assert parse('[ A ]') == (Optional((Keyword('A'),)), )


def test_parse_either():
    assert parse('SELECT { A B | C | D }') == (
        Keyword('SELECT'),
        Either((
            (Keyword('A'), Keyword('B')),
            (Keyword('C'),),
            (Keyword('D'),))))


def test_parse_many_times():
    assert parse('SELECT [, ...]') == (ManyTimes(Keyword('SELECT')),)


def test_parse_nested_complex():
    result = parse('''\
SELECT [ ALL | DISTINCT [ ON ( expression [, ...] ) ] ]
    { * | expression [ [ AS ] output_name ] } [, ...]''')

    assert len(result) == 3
    assert result[0] == Keyword('SELECT')
    assert result[1] == Optional((
        Either((Keyword('ALL'), Keyword('DISTINCT'))),
        Optional((
            Keyword('ON'),
            Keyword('('),
            ManyTimes(Variable('expression')),
            Keyword(')')))
    ))
    assert result[2] == ManyTimes(Either((
        (Keyword('*'),),
        (Variable('expression'),
            Optional((
                Optional((Keyword('AS'),)),
                Variable('output_name')))))))


@pytest.mark.xfail
def test_compress_sequencial_keywords():
    assert parse('SELECT ALL vars IS A') == (
        Keyword('SELECT ALL'),
        Variable('vars'),
        Keyword('IS A'))
