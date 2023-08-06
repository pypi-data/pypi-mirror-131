from regexify import Pattern
from regexify.pattern import Negation


def test_pattern_return_negate():
    m = Pattern('test', negates=[r'\bnot?\b']).matches('do not test this', return_negation=True)
    assert isinstance(m, Negation)
    assert m._term.group() == 'not'
    assert m.match == 'test'


def test_pattern_no_return_negate():
    m = Pattern('test', negates=[r'\bnot?\b']).matches('do not test this')
    assert m is False
