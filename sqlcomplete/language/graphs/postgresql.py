from os.path import join, dirname, abspath
from sqlcomplete.language.creator import create_graph
__all__ = ['graph', 'autocomplete']

definition_path = join(dirname(dirname(abspath(__file__))), 'definition', 'postgresql')

with open(definition_path) as f:
    language = f.read()

graph, sink = create_graph(language)
from sqlcomplete.parse import *
from sqlcomplete.parse import autocomplete as complete


def autocomplete(query):
    return complete(query, graph)
