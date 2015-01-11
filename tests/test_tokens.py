from sqlcomplete.language.tokens import *


def test_tokens_equal():
    a = Variable('x')
    b = Variable('y')
    assert a != b

    a = Either([Optional(Variable('a')), Keyword('SELECT')])
    b = Either([Optional(Variable('a')), Keyword('FROM')])
    assert a != b

    b.things[1] = Keyword('SELECT')
    assert a == b
