from os.path import join, dirname, abspath
from sqlcomplete.language.creator import create_graph

definition_path = join(dirname(dirname(abspath(__file__))), 'definition', 'postgresql')

with open(definition_path) as f:
    language = f.read()

(graph, sink), evaluator = create_graph(language)
from sqlcomplete.autocompleter import *
from sqlcomplete.autocompleter import autocomplete as complete


def autocomplete(query):
    return complete(query, graph, evaluator)
