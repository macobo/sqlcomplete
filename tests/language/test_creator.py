from sqlcomplete.language.creator import *

def test_simple_language():
    lang = """\
statements are
    A B
    C D
"""
    (source, sink), _ = create_graph(lang)
    seen = set()
    for node in walk(source):
        if node.value:
            assert node.value.name not in seen
            seen.add(node.value.name)
    assert seen == set('ABCD')

def test_recursive_language():
    lang = """\
statements are
    simple
    complex

simple is
    A B

complex is
    COMPLEX
"""
    (source, sink), _ = create_graph(lang)
    seen = set()
    for node in walk(source):
        if node.value:
            assert node.value.name not in seen
            seen.add(node.value.name)
    assert seen == set(['A', 'B', 'COMPLEX'])