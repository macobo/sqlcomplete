# Parser for the language definition
from .tokens import *

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
        subpart = parse(pop_until(tokens, ']', '['))
        return Optional(subpart)
    elif token == '{':
        sub_tokens = pop_until(tokens, '}', '{')
        # print '\t\t%s' % ' '.join(sub_tokens)
        return Either.split_and_parse(sub_tokens)
    if token in '*()' or token.isupper():
        return Keyword(token)
    elif token.islower():
        return Variable(token)
    else:
        raise ValueError("Could not parse %r" % token)

def consume(tokens):
    var = consume_single(tokens)
    if tokens and tokens[0] == '|':
        tokens.pop(0)
        next_var = consume_single(tokens)
        if isinstance(next_var, Either):
            return Either(tuple([var]+next_var.things))
        else:
            return Either(tuple([var, next_var]))
    if tokens and tokens[0] == '[,':
        tokens.pop(0)
        assert tokens.pop(0) == '...]'
        return ManyTimes(var)
    return var

def parse(expression):
    if isinstance(expression, str):
        tokens = expression.split()
    else:
        tokens = expression
    result = []
    while tokens:
        # print "I", len(tokens), tokens[:5]
        result.append(consume(tokens))
    return tuple(result)

if __name__ == "__main__":
    syntax_parsed = parse(syntax)