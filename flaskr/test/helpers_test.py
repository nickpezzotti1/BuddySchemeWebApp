from flaskr.models import helpers



def test_string():
    assert helpers.to_str('test') == '"test"'
    assert helpers.to_str('ASADASF') == '"ASADASF"'

def test_list():
    assert helpers.to_str(['test','best','jest']) == '"test","best","jest"'

def test_int():
    assert helpers.to_str(15) == '15'

def test_bool():
    assert helpers.to_str(True) == 1

def test_sanity():
    assert helpers.sanity_check(True) == True
    assert helpers.sanity_check(12) == True
    assert helpers.sanity_check('abc') == True
    assert helpers.sanity_check("a 4 1 bg") == True
