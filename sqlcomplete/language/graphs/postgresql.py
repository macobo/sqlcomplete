from os.path import join, dirname, abspath
from sqlcomplete.language.parser import parse
from sqlcomplete.language.graph import transform_syntax_list, EmptyNode
__all__ = ['graph']

definition_path = join(dirname(dirname(abspath(__file__))), 'definition', 'postgresql')

with open(definition_path) as f:
    language = f.read()

parsed = parse(language)
graph, root = transform_syntax_list(parsed, root_node=EmptyNode())

from sqlcomplete.parse import *
autocomplete('sel', graph)