from sqlcomplete.language.creator import *


def get_node_names(graph):
    seen = set()
    for node in walk(graph):
        if node.value:
            assert node.value.name not in seen
            seen.add(node.value.name)
    return seen


def test_simple_language():
    lang = """\
statements are
    A B
    C D
"""
    (source, sink), _ = create_graph(lang)
    assert get_node_names(source) == set('ABCD')


def test_recursive_language():
    lang = """\
statements are
    simple
    complex

simple is
    A B

complex is
    COMPLEX
"""
    (source, sink), evaluator = create_graph(lang)
    assert get_node_names(source) == set(['simple', 'complex'])
    assert get_node_names(evaluator.get_subtree('simple')) == set(['A', 'B'])
    assert get_node_names(evaluator.get_subtree('complex')) == set(['COMPLEX'])
