from .language.tokens import Variable
from collections import defaultdict


def name(variable):
    return variable.name if isinstance(variable, Variable) else variable


class Evaluator(object):

    " Evaluate variables "

    def __init__(self, graphs=None, variables=None):
        self.graphs = graphs if graphs else {}
        self.variables = defaultdict(list)
        if variables:
            self.variables.update(variables)

    def set(self, key, values):
        self.variables[name(key)] = values

    def add(self, key, *values):
        self.variables[name(key)].extend(values)

    def is_subtree(self, variable):
        return name(variable) in self.graphs

    def get_subtree(self, variable):
        return self.graphs[name(variable)]

    def has_variable(self, variable):
        return self.variables[name(variable)] != []

    def get_matches(self, variable, partial=None):
        """ Return a list of potential matches for variable using possible values
            passed to the class during initialization.

            If match was not found, returns an empty list. """
        matches = self.variables[name(variable)]
        if partial is not None:
            matches = [match for match in matches if match.startswith(partial)]
        return matches
