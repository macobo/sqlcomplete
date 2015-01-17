from .language.tokens import Variable

class Evaluator(object):
    " Evaluate variables "

    def __init__(self, graphs=None, variables=None):
        self.graphs = graphs if graphs else {}
        self.variables = variables if variables else {}

    def is_subtree(self, variable):
        return variable.name in self.graphs

    def get_subtree(self, variable):
        if isinstance(variable, Variable):
            name = variable.name
        else:
            name = variable
        return self.graphs[name][0]

    def get(self, variable, partial=None):
        """ Return either a subtree (Node object) or a list of potential matches
            for variable using variables passed to class.

            If match was not found, returns empty list """
        if self.is_subtree(variable):
            return self.get_subtree(variable)
        matches = self.variables.get(variable.name, [])
        if partial is not None:
            matches = [match for match in matches if match.startswith(partial)]
        return matches
