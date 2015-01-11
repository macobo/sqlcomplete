import re
from collections import deque
from .language.graph import Node, EmptyNode


def children_of(active_frontier):
    Q = deque(active_frontier)
    visited = set(active_frontier)
    while Q:
        node = Q.pop()
        if isinstance(node, EmptyNode):
            for child in node.children:
                if child not in visited:
                    visited.add(child)
                    Q.appendleft(child)
        else:
            yield node


def next_frontier(word, frontier, options):
    """ Takes as argument a current frontier and calculates the new one
        based on the input string.

        A frontier is a tuple of (NonEmptyNode, boolean), where boolean 
        signifies if the word is a full match. """
    children = children_of(node for (node, complete) in frontier if complete)
    for node in children:
        match_type = node.match(word)
        if match_type != Node.NoMatch:
            yield node, match_type == Node.FullMatch


def autocomplete_frontier(word, frontier):
    for node, full_match in frontier:
        if not full_match:
            for suggestion in node.possible_values(word):
                yield suggestion

parse_pattern = re.compile('''\
\w
| [(),*]''', re.UNICODE | re.X)


def parse_sql(query):
    # assumes the query has already been split into multiple pieces
    return tuple(parse_pattern.findall(query))


def start_frontier(language):
    return [(language, True)]


def autocomplete(query, language_root):
    tokens = parse_sql(query)
    frontier = start_frontier(language_root)
    frontier = list(next_frontier(query, frontier, {}))

    print [node.node_value for node, _ in frontier]
    from IPython import embed; embed()
    return list(autocomplete_frontier(tokens[-1], frontier))
