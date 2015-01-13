from os.path import join, dirname, abspath
from sqlcomplete.language.lexer import preprocess
from sqlcomplete.language.graph import transform_syntax_list, EmptyNode, mark_graph
__all__ = ['graph', 'autocomplete']

definition_path = join(dirname(dirname(abspath(__file__))), 'definition', 'postgresql')

with open(definition_path) as f:
    language = f.read()

parsed = preprocess(language)
graph, root = transform_syntax_list(parsed['select_statement'][0], root_node=EmptyNode())
mark_graph(graph)

from sqlcomplete.parse import *
from sqlcomplete.parse import autocomplete as complete


def autocomplete(query):
    return complete(query, graph)
