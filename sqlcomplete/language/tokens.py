from collections import namedtuple
from .graph import Node

# ( ) ,
class Literal(namedtuple('Literal', 'thing')):
    def match(self, word):
        if self.thing == word:
            return Node.FullMatch
        elif self.thing.startswith(word):
            return Node.PartialMatch
        return Node.NoMatch

    def possible_values(self, word):
        return [self.thing] if self.match(word) != Node.NoMatch else []

# ALL, FROM, SELECT, *
class Keyword(namedtuple('Keyword', 'name')):
    def match(self, word):
        name, word = self.name.lower(), word.lower()
        if name == word:
            return Node.FullMatch
        elif name.startswith(word):
            return Node.PartialMatch
        return Node.NoMatch

    def possible_values(self, word):
        return [self.name] if self.match(word) != Node.NoMatch else []

    @staticmethod
    def read_joined(token, tokens):
        if not token.isupper():
            return Keyword(token)
        result = [token]
        while tokens and tokens[0].isupper():
            result.append(tokens.pop(0))
        return Keyword(name=" ".join(result))

# column_name
class Variable(namedtuple('Variable', 'name')):
    def match(self, word):
        return Node.FullMatch

    def possible_values(self, word):
        return []

# [ something something ]
Optional = namedtuple('Optional', 'things')

# { a | b | c }
# Each thing is a list
class Either(namedtuple('Either', 'things')):
    @staticmethod
    def consume_multiple(tokens):
        from .lexer import consume_single
        result = []
        while tokens and tokens[0] != '|':
            var = consume_single(tokens)
            if tokens and tokens[0] == '[,':
                tokens.pop(0)
                assert tokens.pop(0) == '...]'
                var = ManyTimes(var)
            result.append(var)
        assert len(result) > 0
        return tuple(result)

    @staticmethod
    def split_and_parse(tokens):
        things = [Either.consume_multiple(tokens)]
        while tokens:
            # print 'split_and_parse', things, tokens
            assert tokens.pop(0) == '|'
            things.append(Either.consume_multiple(tokens))
        return Either(tuple(things))

# something [, ...]
ManyTimes = namedtuple('ManyTimes', 'thing')
