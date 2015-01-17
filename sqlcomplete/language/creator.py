from .graph import transform_syntax_list, EmptyNode
from .tokens import Variable
from .lexer import preprocess
from sqlcomplete.evaluator import Evaluator
from collections import defaultdict


def create_graph(language_definition):
    """ Take in a stringified language definition and return the unified
    language graph. 

    Language definition starts from definition `statements`. """

    definitions = preprocess(language_definition)
    graphs = {}
    for key, value in definitions.items():
        graphs[key] = source, sink = transform_syntax_list(value, root_node=EmptyNode())
        source.tag = "source_{0}".format(key)
        sink.tag = "sink_{0}".format(key)
    # keywords = keyword_map(graphs.values())

    # for definition, subgraph in graphs.items():
    #     for node in keywords[definition]:
    #         replace_node(node, subgraph)

    # _fix_graph(graphs['statements'][0])
    return graphs['statements'], Evaluator(graphs=graphs)


def walk(node, visited=None):
    " Walk the graph starting from node, yielding all nodes. "
    visited = visited if visited else set()

    visited.add(id(node))
    yield node

    for child in node.children:
        if id(child) not in visited:
            for _node in walk(child, visited):
                yield _node


def _replace(node_list, before_node, new_node):
    for i, node in enumerate(node_list):
        if node is before_node:
            node_list[i] = new_node


def replace_node(node, subgraph, allow_self=True):
    " Replace a node within a graph with a new subgraph "
    source, sink = subgraph
    for parent in node.parents:
        source._parents.append(parent)
        _replace(parent._children, node, source)
    for child in node.children:
        sink._children.append(child)
        _replace(child._parents, node, sink)


def _fix_graph(graph):
    # TODO: make this work!
    for node in walk(graph):
        if isinstance(node, EmptyNode) and len(node.children) == 1:
            node_in_parents = any(node is p for p in node.parents)
            if node_in_parents:
                continue
            replace_node(node, (node.children[0], node.children[0]), False)


def keyword_map(graphs):
    " Create a list of name -> [nodes...] for each Variable in graphs"
    result = defaultdict(list)
    for source, sink in graphs:
        for node in walk(source):
            if isinstance(node.value, Variable):
                result[node.value.name].append(node)
    return result
