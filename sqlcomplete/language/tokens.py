from collections import namedtuple

# ALL
Keyword = namedtuple('Keyword', 'name')

# column_name
Variable = namedtuple('Variable', 'name')

# [ something something ]
Optional = namedtuple('Optional', 'thing')

# { a | b | c }
# Each thing is a list
class Either(namedtuple('Either', 'things')):
    @staticmethod
    def consume_multiple(tokens):
        from .parser import consume_single
        result = []
        while tokens and tokens[0] != '|':
            result.append(consume_single(tokens))
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

# Silly python 3 hack - comparing to None has been removed, so we need a class
# that we can compare to the classes here and be less than any of them
EmptyToken = namedtuple('_EmptyToken', '')
