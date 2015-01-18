from os.path import join, dirname, abspath
from .language.creator import create_graph
from .autocompleter import autocomplete as complete

definition_path = join(dirname(abspath(__file__)), 'language', 'definition', 'postgresql')

with open(definition_path) as f:
    language = f.read()

class Completer(object):
    def __init__(self):
        (self.graph, self.sink), self.evaluator = create_graph(language)

    def set(self, key, value):
        self.evaluator.set(key, value)

    def autocomplete(self, query):
        return complete(query, self.graph, self.evaluator)
