import pytest
from sqlcomplete.language import *
from sqlcomplete.autocompleter import *


@pytest.fixture
def language():
    lang = """\
statements are
    ABC keyword BCD
    [ optional ] AKEYWORD subgraph END
    BAZ


subgraph is
    FOOBAR"""

    return create_graph(lang)


@pytest.fixture
def root(language):
    return language[0][0]


@pytest.fixture
def evaluator(language):
    return language[1]


def node_values(frontier):
    return [active_node(path).value for path, _, _ in frontier]


def test_start_frontier(root):
    assert isinstance(root, EmptyNode)
    path, stack, full_match = start_frontier(root)[0]
    assert active_node(path) is root
    assert stack == []


def test_children_of(root):
    front = start_frontier(root)
    next_front = children_of(front)
    assert set(node_values(next_front)) == set([
        Keyword('ABC'),
        Variable('optional'),
        Keyword('AKEYWORD'),
        Keyword('BAZ')])


def test_next_frontier(root, evaluator):
    front = start_frontier(root)
    second_front = list(next_frontier('', front, evaluator))
    assert set(node_values(second_front)) == set([
        Keyword('ABC'),
        Variable('optional'),
        Keyword('AKEYWORD'),
        Keyword('BAZ')])

    second_front_2 = list(next_frontier('A', front, evaluator))

    assert set(node_values(second_front_2)) == set([
        Keyword('ABC'),
        Variable('optional'),
        Keyword('AKEYWORD')])

    assert not second_front_2[0][2]

    akweyword_front = list(next_frontier('AKEYWORD', front, evaluator))

    assert set(node_values(akweyword_front)) == set([
        Variable('optional'),
        Keyword('AKEYWORD')])

    assert second_front_2[1][2]  # was a full match
    return akweyword_front


def test_next_frontier_recursive(root, evaluator):
    front = test_next_frontier(root, evaluator)
    recursive_front = list(next_frontier('FOOBAR', front, evaluator))
    assert len(recursive_front) == 1
    path, stack, match = recursive_front[0]
    assert active_node(path).value == Keyword('FOOBAR')
    assert len(stack) == 1 and stack[0].value == Variable('subgraph')

    return recursive_front


def test_next_frontier_recursion_pop(root, evaluator):
    front = test_next_frontier_recursive(root, evaluator)
    popped_front = list(next_frontier('', front, evaluator))
    assert len(popped_front) == 1
    path, stack, match = popped_front[0]

    assert len(stack) == 0
    assert active_node(path).value == Keyword('END')
