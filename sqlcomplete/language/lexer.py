# Parser for the language definition
import logging
from .tokens import *

_logger = logging.getLogger(__name__)


def pop_until(tokens, end_token, start_token):
    result = []
    start_token_count = 1
    while True:
        token = tokens.pop(0)
        if token == start_token:
            start_token_count += 1
        elif token == end_token:
            start_token_count -= 1
            if start_token_count == 0:
                break
        result.append(token)
    return result


def consume_single(tokens):
    token = tokens.pop(0)
    # print '\tConsuming a single %r' % token
    if token == '[':
        subpart = lex(pop_until(tokens, ']', '['))
        return Optional(subpart)
    elif token == '{':
        sub_tokens = pop_until(tokens, '}', '{')
        # print '\t\t%s' % ' '.join(sub_tokens)
        return Either.split_and_parse(sub_tokens)
    if token in '*' or token.isupper():
        return Keyword(token)
    elif token in '()':
        return Literal(token)
    elif token.islower():
        return Variable(token)
    else:
        raise ValueError("Could not parse %r" % token)


def consume(tokens):
    var = consume_single(tokens)
    while tokens and tokens[0] == '|':
        tokens.pop(0)
        next_var = consume_single(tokens)
        if isinstance(var, Either):
            var = Either(var.things + ((next_var,),))
        else:
            var = Either(((var,), (next_var,)))
    if tokens and tokens[0] == '[,':
        tokens.pop(0)
        assert tokens.pop(0) == '...]'
        return ManyTimes(var)
    return var


def lex(expression):
    # TODO: replace lists with deque!
    if isinstance(expression, str):
        tokens = expression.split()
    else:
        tokens = expression
    result = []
    while tokens:
        # print "I", len(tokens), tokens[:5]
        result.append(consume(tokens))
    return tuple(result)


def indent_count(line):
    for i, char in enumerate(line):
        if char != ' ':
            return i
    return len(line)


def is_comment(line):
    line = line.strip()
    return not line or line[0] == '#'


def partition(language_definition):
    """ Partition a language definition into groups, removing lines that are
        comments and grouping stuff together by whitespace.

        For example, the following language definition:

        expression are
            START_TOKENS MIDDLE_TOKENS
                # comment
                NESTED_TOKENS END_TOKENS
            SECOND LINE

        Is transformed to:
        [(
            'expression are',
            [('START_TOKENS MIDDLE_TOKENS', [
                ('NESTED_TOKENS', []),
                ('END_TOKENS', [])]),
             ('SECOND LINE', [])]
        )]
        """

    lines = language_definition.split('\n')

    def process(lines, indent=0):
        line = ""
        while is_comment(line):
            line = lines.pop(0).rstrip()
        assert indent_count(line) == indent
        children = []
        while lines:
            child = lines[0]
            count = indent_count(child)
            if is_comment(child):
                lines.pop(0)
                continue
            if count == indent + 4:
                result = process(lines, indent + 4)
                children.append(result)
            elif count <= indent:
                break
            else:
                raise ValueError(
                    'Wrong indent count, expected either %d or %d. Line: %r' % (indent, indent + 4, child))
        return line.strip(), children

    result = []
    while lines:
        result.append(process(lines))
    return result


def rejoin_partitioned(partition, indent=0):
    print partition
    root, children = partition
    result = root
    if children:
        result += ' ' + ' '.join(rejoin_partitioned(child) for child in children)
    return result


def preprocess(language_definition):
    """ Calculate a dictionary of name -> definition for the language """
    result = {}
    for first_line, parts in partition(language_definition):
        name, amount = first_line.split()
        if amount == 'is' and len(parts) != 1:
            _logger.warn("Language definition for node %r has %r children"
                         "should have 1", name, len(parts))
        result[name] = [lex(rejoin_partitioned(p)) for p in parts]
    return result
