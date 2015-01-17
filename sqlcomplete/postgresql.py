from os.path import join, dirname, abspath
from .language.creator import create_graph
from .autocompleter import autocomplete as complete

definition_path = join(dirname(abspath(__file__)), 'language', 'definition', 'postgresql')

with open(definition_path) as f:
    language = f.read()

(graph, sink), evaluator = create_graph(language)


def autocomplete(query):
    return complete(query, graph, evaluator)
