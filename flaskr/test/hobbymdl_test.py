import flaskr.models.hobbymdl as testmdl

tester = testmdl.HobbyModel('testing')


def test_hobby():
	tester.insert_hobby(1, 'Besting')
	get = tester.select_hobby(1, 'Besting')
	assert 1 == len(get)

def test_select_hobby():
	get = tester.select_hobby(1, 'Besting')
	assert 'Besting' == get[0]['hobby_name']
	assert 1 == get[0]['scheme_id']

def test_delete_hobby():
	get = tester.select_hobby(1, 'Besting')
	tester.delete_hobby(1, get[0]['id'])
	get = tester.select_hobby(1, 'Besting')
	assert 0 == len(get)