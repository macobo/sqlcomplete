import pytest
from sqlcomplete.evaluator import Evaluator
from sqlcomplete.language import Node, Literal, Variable


@pytest.fixture
def evaluator():
    graph1 = Node(Literal('abc'))
    graph2 = Node(Variable('bcd'))

    return Evaluator(
        graphs={
            "1": graph1,
            "tricky": graph2
        },
        variables={
            "foo": ['beta', 'bets', 'zoo'],
            "tricky": ['mickey']
        }
    )


def test_evaluator_subtrees(evaluator):
    assert evaluator.is_subtree('1')
    assert evaluator.is_subtree(Variable('1'))
    assert evaluator.is_subtree('tricky')
    assert not evaluator.is_subtree('foo')

    assert evaluator.get_subtree('1').value == Literal('abc')
    assert evaluator.get_subtree(Variable('1')).value == Literal('abc')
    assert evaluator.get_subtree('tricky').value == Variable('bcd')

    with pytest.raises(Exception):
        evaluator.get_subtree('doesn\'t exist')


def test_evaluator_variables(evaluator):
    assert evaluator.get_matches('foo') == ['beta', 'bets', 'zoo']
    assert evaluator.get_matches('foo', 'be') == ['beta', 'bets']
    assert evaluator.get_matches('tricky') == ['mickey']
    assert evaluator.get_matches('doesnt exist') == []
