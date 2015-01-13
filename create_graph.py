from graphviz import Digraph
dot = Digraph(comment="postgresql", format='svg')
from sqlcomplete.language.graphs.postgresql import graph
from sqlcomplete.language.creator import walk

for node in walk(graph):
    s = ""
    if node.value:
        s = str(node.value)
    if node.tag:
        if s: s += "\n"
        s = s + node.tag
    dot.node(str(id(node)), s)

for node in walk(graph):
    for child in node.children:
        dot.edge(str(id(node)), str(id(child)))

dot.render('postgresql', 'graphs', cleanup=True)
