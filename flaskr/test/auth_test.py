import auth_token


def test_token():
    temp = auth_token.generate_token('1234','K1234')
    assert 'K1234' == auth_token.verify_token('1234', temp)

def test_largetoken():
    temp = auth_token.generate_token('12341245325','K123442343245124')
    assert 'K123442343245124' == auth_token.verify_token('12341245325', temp)