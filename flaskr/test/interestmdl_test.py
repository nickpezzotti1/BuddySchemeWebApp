import flaskr.models.interestmdl as testmdl

tester = testmdl.InterestModel('testing')


def test_interest():
	tester.insert_interest('Besting', 1)
	get = tester.select_interest('Besting', 1)
	assert 1 == len(get)

def test_select_():
	get = tester.select_interest('Besting', 1)
	assert 'Besting' == get[0]['interest_name']
	assert 1 == get[0]['scheme_id']

def test_delete():
	get = tester.select_interest('Besting', 1)
	tester.delete_interest(get[0]['id'],1)
	get = tester.select_interest('Besting', 1)
	assert 0 == len(get)
