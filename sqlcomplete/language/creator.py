from .graph import transform_syntax_list
from .tokens import Keyword
from collections import defaultdict


def create_graph(language_definition):
    """ Take in a stringified language definition and return the unified
    language graph. 

    Language definition starts from definition `statements`. """

    from .lexer import preprocess
    definitions = preprocess(language_definition)
    graphs = dict((key, transform_syntax_list(value)) for key, value in definitions.items())
    keywords = keyword_map(graphs)

    for definition, subgraph in graphs.items():
        for node in keywords[definition]:
            replace_node(node, subgraph)

    return graphs['statements']


def walk(node, visited=None):
    visited = visited if visited else set()

    visited.add(id(node))
    yield node

    for child in node.children:
        if id(child) not in visited:
            for _node in walk(child, visited):
                yield _node


def replace(node_list, before_node, new_node):
    for i, node in enumerate(node_list):
        if node is before_node:
            node_list[i] = new_node


def replace_node(node, subgraph):
    " Replace a node within a graph with a new subgraph "
    source, sink = subgraph
    for parent in node.parents:
        replace(parent._children, node, source)
    for child in node.children:
        replace(child._parents, node, sink)


def keyword_map(graphs):
    " Create a list of name -> [nodes...] for each keyword in graphs"
    result = defaultdict(list)
    for graph in graphs:
        for node in walk(graph):
            if isinstance(node.value, Keyword):
                result[node.value.name].append(node)
    return result
