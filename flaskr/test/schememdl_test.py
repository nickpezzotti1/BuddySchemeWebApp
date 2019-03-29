import flaskr.models.schememdl as testmdl

tester = testmdl.SchemeModel('testing')

def test_name_available():
	assert True == tester.check_scheme_avail('Tester')

def test_scheme():
	count = tester.create_new_scheme('Tester')
	assert count == 1

def test_active():
	get = tester.get_active_scheme_data()
	assert 0 < len(get)

def test_scheme_delete():
	get = tester.get_scheme_id('Tester')
	count = tester.delete_scheme(get)
	assert count == 1