import auth_token


def test_token():
    temp = auth_token.generate_token('1234','K1234')
    assert 'K1234' == auth_token.verify_token('1234', temp)