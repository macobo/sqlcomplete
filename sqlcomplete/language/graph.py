# from functools import total_ordering

# Sadly not present under py2.6
# @total_ordering
class Node(object):
    NoMatch = 0
    PartialMatch = 1
    FullMatch = 2

    def __init__(self, value, children=None, tag=None):
        from .tokens import Keyword, Variable, Literal
        assert type(value) in [Keyword, Variable, Literal, tuple]
        self.value = value
        # TODO: allow weights for the children???
        self._children = []
        self._parents = []
        for child in children or []:
            self.add_child(child)
        self.tag = tag

    @property
    def children(self):
        return tuple(self._children)

    @property
    def parents(self):
        return tuple(self._parents)

    @property
    def key(self):
        "Key for this node, used for hashing and establishing ordering."
        return (self.value, self.children)

    def is_sink(self):
        " Is this node the lowermost node in its subgraph? "
        return len(self.children) == 0

    def add_child(self, node):
        self._children.append(node)
        node.add_parent(self)

    def add_parent(self, node):
        self._parents.append(node)

    # Matching
    def match(self, word):
        assert not isinstance(self, EmptyNode)
        return self.value.match(word)

    def possible_values(self, word):
        assert not isinstance(self, EmptyNode)
        return self.value.possible_values(word)

    # Make the node type hashable
    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key

    # @recursive_repr()
    def __repr__(self):
        format_ = "Node({value})"
        if self.tag:
            format_ = "Node({value}, tag={tag})"
        return format_.format(value=self.value, tag=self.tag)

# Used for groupings
#
# An Optional is represented as an Empty -> content -> Empty, where the first
# Empty points to the second.
#
# An Either is represented by Empty -> content_nodes -> Empty, where the first
# content has a edge to each of the content nodes and each of the content nodes
# point to the last Empty.

class EmptyNode(Node):

    def __init__(self, *args, **kw):
        Node.__init__(self, tuple(), *args, **kw)

    def __repr__(self):
        format_ = "Node()"
        if self.tag:
            format_ = "Node(tag={tag})"
        return format_.format(tag=self.tag)

# TODO: merge two graphs


def create_subgraph(syntax_element):
    """ Takes as an argument an Keyword, Variable, Optional, Either or Manytimes
        and returns the root and leaf of the subgraph. """
    from .tokens import Keyword, Variable, Literal, Either, Optional, ManyTimes

    if type(syntax_element) in [Keyword, Variable, Literal]:
        # TODO: parse the Variable somehow?
        node = Node(syntax_element)
        return node, node
    elif isinstance(syntax_element, Optional):
        sub_node_start, sub_node_end = transform_syntax_list(syntax_element.things, empty_end=False)
        end = EmptyNode([])
        start = EmptyNode([sub_node_start, end], tag="Opt")
        sub_node_end.add_child(end)
        end.tag = 'optional.end'
        return start, end
    elif isinstance(syntax_element, Either):
        start, end = EmptyNode(tag="Either"), EmptyNode()
        for child in syntax_element.things:
            # nope - this should be something like parse_syntax_list!
            sub_start, sub_end = transform_syntax_list(child, root_node=start, empty_end=False)
            sub_end.add_child(end)
        return start, end
    else:
        # Make the subgraph end point to the start, requiring a comma in between!
        # if not isinstance(syntax_element, ManyTimes): from IPython import embed; embed()
        assert isinstance(syntax_element, ManyTimes), type(syntax_element)
        sub_node_start, sub_node_end = create_subgraph(syntax_element.thing)

        comma_node = Node(Literal(','))  # TODO: replace with a node matching ','
        sub_node_end.add_child(comma_node)
        comma_node.add_child(sub_node_start)
        return sub_node_start, sub_node_end


def transform_syntax_list(syntax_list, root_node=None, empty_end=True):
    """ Transform a tuple of syntax elements to a language graph.
        Returns the root and end node of the created graph """
    iterator = iter(syntax_list)
    if root_node is None:
        element = next(iterator)
        root_node, end_node = create_subgraph(element)
    else:
        end_node = root_node

    for element in iterator:
        start, new_end = create_subgraph(element)
        end_node.add_child(start)
        end_node = new_end
    # Recursion matching logic assumes that a tree starts and ends with
    # empty nodes
    if empty_end and not isinstance(end_node, EmptyNode):
        node = EmptyNode()
        end_node.add_child(node)
        end_node = node
    return root_node, end_node
