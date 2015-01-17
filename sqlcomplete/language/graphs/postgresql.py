from os.path import join, dirname, abspath
from sqlcomplete.language.creator import create_graph
__all__ = ['graph', 'autocomplete', 'subgraphs']

definition_path = join(dirname(dirname(abspath(__file__))), 'definition', 'postgresql')

with open(definition_path) as f:
    language = f.read()

(graph, sink), subgraphs = create_graph(language)
from sqlcomplete.autocompleter import *
from sqlcomplete.autocompleter import autocomplete as complete
from sqlcomplete.evaluator import Evaluator

evaluator = Evaluator(graphs=subgraphs)


def autocomplete(query):
    return complete(query, graph, evaluator)
