from graphviz import Digraph
from .language import Node
from .language.creator import walk, keyword_map


def add_graph(dot, graph):
    for node in walk(graph):
        s = ""
        if node.value:
            s = str(node.value)
        if node.tag:
            if s:
                s += "\n"
            s = s + node.tag
        dot.node(str(id(node)), s)

    for node in walk(graph):
        for child in node.children:
            dot.edge(str(id(node)), str(id(child)))


def render_subgraphs(name, subgraphs):
    if isinstance(subgraphs, Node):
        subgraphs = {'graph': subgraphs}
    dot = Digraph(comment=name, format='svg')
    # kwmap = keyword_map(subgraphs.values())
    for key in sorted(subgraphs):
        add_graph(dot, subgraphs[key])
    dot.render(name, 'graphs', cleanup=True)


if __name__ == "__main__":
    from .postgresql import evaluator
    render_subgraphs('postgresql', evaluator.graphs)

    # for name, (subgraph_start, subgraph_end) in subgraphs.items():
    #     for node in kwmap[name]:
    #         dot.edge(str(id(node)), str(id(subgraph_start)), style="dotted")
    #         dot.edge(str(id(subgraph_end)), str(id(node)), style="dotted")
