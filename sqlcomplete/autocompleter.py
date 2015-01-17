import re
import logging
from collections import deque
from .language.graph import Node, EmptyNode
from .language.tokens import Variable

log = logging.getLogger(__name__)


# Frontier - collection of Path, complete_match objects.

def active_node(path):
    return path[-1]


def children_of(frontier):
    # assumes the first element of frontier is the path, rest is baggage to be
    # carried along
    Q = deque(frontier)
    visited = set(id(active_node(x[0])) for x in frontier)
    while Q:
        path, stack = Q.pop()
        node = active_node(path)
        # log.debug("%r", path)
        # log.info("%r - %r", node, node.children)
        for child in node.children:
            # log.info("%r %r %r", child, child.is_sink(), id(child) not in visited)
            next_path = path + (child,)
            if id(child) not in visited:
                visited.add(id(child))
                if isinstance(child, EmptyNode) and not child.is_sink():
                    Q.appendleft((next_path, stack))
                else:
                    yield next_path, stack


def next_frontier(word, frontier, evaluator):
    """ Takes as argument a current frontier and calculates the new one
        based on the input string.

        A frontier is a tuple of (path, stack, full_match).
            `path` - list of Nodes went through in graph (last one is active)
            `stack` - manually managed recursion stack for recursing into subgraphs
            `full_match` - if the match at this node was complete. If not, this 
                subgraph will not be visited further.
    """
    children = list(children_of((path, stack) for path, stack, complete in frontier if complete))

    _recursive_front = []
    for path, stack in children:
        # log.info("%r", path)
        node = path[-1]
        if isinstance(node.value, Variable) and evaluator.is_subtree(node.value):
            # if is a subtree, recurse into it!
            # assumes the subtree starts with an empty node!
            sub_root, _ = evaluator.get_subtree(node.value)
            # recurse here!
            _recursive_front.append((path + (sub_root,), stack+[node], True))
        elif node.is_sink():
            if len(stack) == 0:
                continue
            # pop from stack
            popped_node, popped_stack = stack[-1], stack[:-1]
            _recursive_front.append((path + (popped_node,), popped_stack, True))
        else:
            match_type = node.match(word)
            if match_type != Node.NoMatch:
                yield path, stack, match_type == Node.FullMatch

    # Have to recurse into/out of subgraphs. Unwind automatically
    if _recursive_front:
        for x in next_frontier(word, _recursive_front, evaluator):
            yield x


def autocomplete_frontier(word, frontier):
    for path, stack, full_match in frontier:
        node = active_node(path)
        if not full_match:
            for suggestion in node.possible_values(word):
                yield suggestion

parse_pattern = re.compile('''\
\w+
| [(),*]''', re.UNICODE | re.X)


def parse_sql(query):
    # assumes the query has already been split into multiple pieces
    return parse_pattern.findall(query)


def start_frontier(node):
    " (path, stack, full_match) "
    return [((node,), [], True)]


def _autocomplete(tokens, node, evaluator):
    frontier = start_frontier(node)

    while tokens and frontier:
        token = tokens[0]
        #from pprint import pformat
        #log.debug("-- %r --\n%s", token, pformat(frontier))
        frontier = list(next_frontier(token, frontier, evaluator))
        if not frontier:
            break
        tokens.pop(0)

    if tokens:
        return []
    return list(autocomplete_frontier(token, frontier))


def autocomplete(query, language_root, evaluator):
    """ Take an sql query and a language and offer potential autocompletions for
        the query. """
    tokens = parse_sql(query)
    return _autocomplete(tokens, language_root, evaluator)
