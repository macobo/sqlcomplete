# Tests for language graph construction from pieces from the parser
from sqlcomplete.language.graph import *
from sqlcomplete.language.lexer import *


def parse_to_subgraph(language):
    tokens = lex(language)
    assert len(tokens) == 1
    return create_subgraph(tokens[0])


def parse_language(language):
    tokens = lex(language)
    return transform_syntax_list(tokens, root_node=EmptyNode())


def test_graph_comparison():
    a = Node(Keyword('A'))
    assert a == Node(Keyword('A'))
    assert a != Node(Keyword('A'), (Node(Keyword('B')),))
    a.add_child(Node(Keyword('B')))
    assert a == Node(Keyword('A'), (Node(Keyword('B')),))


def test_keyword_subgraph():
    start, end = create_subgraph(Keyword('FOOBAR'))
    assert start == end
    assert start == Node(Keyword('FOOBAR'))

# TODO: variable subgraph where variable is defined?


def test_optional_subgraph():
    start, end = parse_to_subgraph('[ FOOBAR ]')

    assert isinstance(start, EmptyNode) and isinstance(end, EmptyNode)
    assert set(start.children) == set((end, Node(Keyword('FOOBAR'), children=(end,))))


def test_optional_subgraph_multiple():
    start, end = parse_to_subgraph('[ FOOBAR B ]')

    # Draw out the graph bottom-up
    end_node = EmptyNode()
    b_node = Node(Keyword('B'), (end_node,))
    foobar_node = Node(Keyword('FOOBAR'), (b_node,))
    root_node = EmptyNode((foobar_node, end_node))

    assert start == root_node


def test_either_subgraph():
    start, end = parse_to_subgraph('{ FOO | BAR BAZ | WOO }')

    assert isinstance(start, EmptyNode) and isinstance(end, EmptyNode)
    assert len(start.children) == 3

    assert start.children[0] == Node(Keyword('FOO'), children=(end,))
    assert start.children[1] == Node(
        Keyword('BAR'),
        children=(
            Node(Keyword('BAZ'),
                 children=(end,)),))
    assert start.children[2] == Node(Keyword('WOO'), children=(end,))


def test_parse_language():
    language = "SELECT [ ALL | DISTINCT [ ON ( expression [, ...] ) ] ]"
    graph = parse_language(language)


# def test_graph_marking():
#     a = EmptyNode()
#     b = EmptyNode(children=(a,))
#     graph = EmptyNode(children=(Node('something'), b))

#     mark_graph(graph)
#     assert a.mark == (2, 0)
#     assert b.mark == (1, 1)

#     assert len(set([a, b])) == 2
