from graphviz import Digraph
dot = Digraph(comment="postgresql", format='svg')
from sqlcomplete.language.graphs.postgresql import evaluator
from sqlcomplete.language.creator import walk, keyword_map


subgraphs = evaluator.graphs
kwmap = keyword_map(subgraphs.values())

for key in sorted(subgraphs):
    graph = subgraphs[key][0]
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

# for name, (subgraph_start, subgraph_end) in subgraphs.items():
#     for node in kwmap[name]:
#         dot.edge(str(id(node)), str(id(subgraph_start)), style="dotted")
#         dot.edge(str(id(subgraph_end)), str(id(node)), style="dotted")

dot.render('postgresql', 'graphs', cleanup=True)
