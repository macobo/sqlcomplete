import re
import logging
from collections import deque
from .language.graph import Node, EmptyNode

_logger = logging.getLogger(__name__)


# Frontier - collection of Path, complete_match objects.

def active_node(path):
    return path[-1]

def children_of(active_frontier):
    Q = deque(active_frontier)
    visited = set(map(id, map(active_node, active_frontier)))
    while Q:
        path = Q.pop()
        node = active_node(path)
        _logger.debug("%r", path)
        for child in node.children:
            next_path = path + (child,)
            # print child, visited, child in visited, child.key
            if id(child) not in visited:
                visited.add(id(child))
                if isinstance(child, EmptyNode):
                    Q.appendleft(next_path)
                else:
                    yield next_path


def next_frontier(word, frontier, options):
    """ Takes as argument a current frontier and calculates the new one
        based on the input string.

        A frontier is a tuple of ([Nodes], boolean), where boolean 
        signifies if the word is a full match and last of nodes is not empty.
    """
    children = list(children_of(path for (path, complete) in frontier if complete))
    # print map(active_node, children)
    for path in children:
        node = active_node(path)
        match_type = node.match(word)
        if match_type != Node.NoMatch:
            yield path, match_type == Node.FullMatch


def autocomplete_frontier(word, frontier):
    for path, full_match in frontier:
        node = active_node(path)
        if not full_match:
            for suggestion in node.possible_values(word):
                yield suggestion

parse_pattern = re.compile('''\
\w+
| [(),*]''', re.UNICODE | re.X)


def parse_sql(query):
    # assumes the query has already been split into multiple pieces
    return tuple(parse_pattern.findall(query))


def start_frontier(language):
    return [((language,), True)]


def autocomplete(query, language_root):
    tokens = parse_sql(query)
    frontier = start_frontier(language_root)
    for token in tokens:
        _logger.debug("%r %r", token, frontier)
        frontier = list(next_frontier(token, frontier, {}))

    return list(autocomplete_frontier(tokens[-1], frontier))
