from .tokens import *
from functools import total_ordering
from .utils import recursive_repr


@total_ordering
class Node(object):
    NoMatch = 0
    PartialMatch = 1
    FullMatch = 2

    def __init__(self, node_value, children=None):
        # assert type(node_value) in [Keyword, Variable, type(None)]
        self.node_value = node_value
        # TODO: allow weights for the childs
        self._children = children if children else []

    @property
    def children(self):
        # TODO: make this sorted, memoized
        return tuple(self._children)

    def children_sorted(self):
        if not getattr(self, '_children_sorted', None):
            self._children_sorted = tuple(sorted(self._children))
        return self._children_sorted

    @property
    def key(self):
        "Key for this node, used for hashing and establishing ordering."
        return (self.node_value, self.children)

    def add_child(self, node):
        self._children_sorted = None
        self._children.append(node)

    def matches_syntax_type(self, thing):
        if type(self.node_value) != type(thing):
            return False
        compare = ['name', 'thing', 'things']
        return all(getattr(self.node_value, t) == getattr(thing, t) for t in compare)

    # Make the node type hashable
    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key

    @recursive_repr()
    def __repr__(self):
        return "Node(node_value=%r, children=%r)" % self.key

# Used for groupings
#
# An Optional is represented as an Empty -> content -> Empty, where the first
# Empty points to the second.
#
# An Either is represented by Empty -> content_nodes -> Empty, where the first
# content has a edge to each of the content nodes and each of the content nodes
# point to the last Empty.

class EmptyNode(Node):

    def __init__(self, children=None):
        Node.__init__(self, tuple(), children)

# TODO: merge two graphs


def create_subgraph(syntax_element):
    """ Takes as an argument an Keyword, Variable, Optional, Either or Manytimes
        and returns the root and leaf of the subgraph. """

    if isinstance(syntax_element, Keyword) or isinstance(syntax_element, Variable):
        # TODO: parse the Variable somehow?
        node = Node(syntax_element)
        return node, node
    elif isinstance(syntax_element, Optional):
        sub_node_start, sub_node_end = transform_syntax_list(syntax_element.things)
        end = EmptyNode([])
        start = EmptyNode([sub_node_start, end])
        sub_node_end.add_child(end)
        return start, end
    elif isinstance(syntax_element, Either):
        start, end = EmptyNode(), EmptyNode()
        for child in syntax_element.things:
            # nope - this should be something like parse_syntax_list!
            sub_start, sub_end = transform_syntax_list(child, root_node=start)
            sub_end.add_child(end)
        return start, end
    else:
        # Make the subgraph end point to the start, requiring a comma in between!
        assert isinstance(syntax_element, ManyTimes), type(syntax_element)
        sub_node_start, sub_node_end = create_subgraph(syntax_element.thing)

        comma_node = Node(Literal(','))  # TODO: replace with a node matching ','
        sub_node_end.add_child(comma_node)
        comma_node.add_child(sub_node_start)
        return sub_node_start, sub_node_end


def transform_syntax_list(syntax_list, root_node=None):
    """ Transform a list of syntax elements to a language graph.
        Returns the root and end node of the created graph """
    iterator = iter(syntax_list)
    if root_node is None:
        root_node, end_node = create_subgraph(next(iterator))
    else:
        end_node = root_node

    for element in iterator:
        start, new_end = create_subgraph(element)
        end_node.add_child(start)
        end_node = new_end
    return root_node, end_node
