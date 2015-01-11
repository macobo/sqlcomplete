Data types representing a language graph are specified in `graph.py`.

A language graph is a directed graph which can be travesed starting from a root
node while parsing a partial valid sql query.

# Matching using the graph
This graph can then be used to automatically complete the partial query, by
traversing the language graph up until reaching the last incomplete part in the
token and a corresponding node in the graph.

Children of that last node can then be prefix-matched to the incomplete partial
token and a suggestion can be made.

# Explanation of intent
Each node corresponds either to a keyword (e.g. SELECT, FROM), a variable (e.g.
) or None (representing an empty node).

Each node also has a number of children, representing possible next states for
a valid query.

# Construction

The tree is constructed using tokens gained from parsing the language
specification.

More specifically, each list of tokens (for each type of query) is transformed
to a corresponding tree recursively, each Keyword and Variable matching to a
single Node in the tree.

Different trees are then merged into a single one.

When transforming `Either`, `Option` or `ManyTimes`, subgraphs starting and 
ending with empty nodes are used:

* `Either` is transformed into a subgraph with an `Empty` node at the top and
  bottom with each `thing` being a child of the topmost `Empty` and all states
  end in the lower `Empty` node.

* `Option` is transformed into a subgraph `Empty -> thing -> Empty`, with the
  topmost `Empty` node also being connected to the lower one.

* `ManyTimes` transforms its contents into a subgraph as well, making its lowest
  node reference to a comma node which in turn references to the topmost node.


# Notes

The created language graph is recursive, as a variable might be an expression
and thereby refer to the root node of the graph.

While traversing the graph while parsing a query, it should not be possible to
end up at different nodes as this would complicate the 

# Ideas

Additional constraints may also be applied when writing the query, for example
offering only the tables/views in a SELECT query that have matching columns as
the ones specified.

Replace variables with references?