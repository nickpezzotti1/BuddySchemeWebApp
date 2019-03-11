from models import helpers

def inc(x):
    return x + 1


def test_basic():
    assert inc(3) == 4


def test_string():
    assert helpers.to_str('test') == '"test"'
