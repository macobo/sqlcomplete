from sqlcomplete.autocompleter import *


def test_parser():
    assert parse_sql('SELECT * FROM table') == ['SELECT', '*', 'FROM', 'table']
    assert parse_sql('SELECT count(*) FROM table') == [
        'SELECT', 'count', '(', '*', ')', 'FROM', 'table']
    assert parse_sql('SELECT   a ,  b,(select thing from there) as e FROM table') == [
        'SELECT', 'a', ',', 'b', ',', '(', 'select', 'thing', 'from', 'there',
        ')', 'as', 'e', 'FROM', 'table']

# TODO: test unicode
# TODO: test expressions containing other punctation: []::
