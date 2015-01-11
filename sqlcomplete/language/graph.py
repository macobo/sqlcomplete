from .tokens import *


class Node(object):

    def __init__(self, node_value, children=[]):
        assert type(node_value) in [Keyword, Variable, type(None)]
        self.node_value = node_value
        # TODO: allow weights for the childs
        self._children = children

    @property
    def children(self):
        return tuple(self._children)

    def add_child(self, node):
        self._children.append(node)

    def matches_syntax_type(self, thing):
        if type(self.node_value) != type(thing):
            return False
        compare = ['name', 'thing', 'things']
        return all(getattr(self.node_value, t) == getattr(thing, t) for t in compare)

    # Make the node type hashable
    def __hash__(self):
        return hash((self.node_value, self.children))

    # Define ordering (for sorting children for faster merges)
    # The exact ordering is not important, it just has to be consistent
    def __cmp__(self, other):
        if type(self.node_value) != type(other.node_value):
            return cmp(str(type(self.node_value)), str(type(other.node_value)))
        if len(self.children) != len(other.children):
            return cmp(len(self.children), len(other.children))
        for a, b in zip(self.children, other.children):
            compared = cmp(a, b)
            if compared:
                return compared
        return 0

# Used for groupings
#
# An Optional is represented as an Empty -> content -> Empty, where the first
# Empty points to the second.
#
# An Either is represented by Empty -> content_nodes -> Empty, where the first
# content has a edge to each of the content nodes and each of the content nodes
# point to the last Empty.


class EmptyNode(Node):

    def __init__(self, children=[]):
        Node.__init__(self, None, children)

# TODO: merge two trees
def create_subtree(syntax_element):
    """ Takes as an argument an Keyword, Variable, Optional, Either or Manytimes
        and returns the root and leaf of the subtree. """

    if isinstance(syntax_element, Keyword) or isinstance(syntax_element, Variable):
        # TODO: parse the Variable somehow?
        node = Node(syntax_element)
        return node, node
    elif isinstance(syntax_element, Optional):
        sub_node_start, sub_node_end = create_subtree(syntax_element.thing)
        start = EmptyNode([sub_node_start])
        end = EmptyNode([sub_node_end])
        return start, end
    elif isinstance(syntax_element, Either):
        start, end = EmptyNode(), EmptyNode()
        for child in syntax_element.things:
            # nope - this should be something like parse_syntax_list!
            sub_start, sub_end = create_subtree(child)
            start.add_child(sub_start)
            sub_end.add_child(end)
        return start, end
    else:
        # Make the subtree end point to the start, requiring a comma in between!
        assert isinstance(syntax_element, ManyTimes)
        sub_node_start, sub_node_end = create_subtree(syntax_element.thing)

        comma_node = EmptyNode()  # TODO: replace with a node matching ','
        sub_node_end.add_child(comma_node)
        comma_node.add_child(sub_node_start)
        return sub_node_start, sub_node_end


def transform_syntax_list(syntax_list, root_node=None):
    """ Transform a list of syntax elements to a language tree.
        Returns the root and end node of the created tree """
    iterator = iter(syntax_list)
    if root_node is None:
        root_node, end_node = create_subtree(next(iterator))
    else:
        end_node = root_node

    for element in iterator:
        start, new_end = create_subtree(element)
        end_node.add_child(start)
        end_node = new_end
    return root_node, end_node
