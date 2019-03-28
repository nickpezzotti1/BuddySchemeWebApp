import flaskr.models.studentmdl as testmdl
import datetime

tester = testmdl.StudentModel('testing')


def test_student():
	count = tester.insert_student(1, 'k00000000', 'Bai', 'Ganyo', 'BSc Comp Sci', 1, 'Male', 0, 'pbkdf2:sha256:50000$igDdtEIs$17ab89312192f317e44bd9b29f2e04346519a6a06e79e4bfffc0156f44c7a13b', 0, 3)
	assert count == 1

def test_hash():
	get = tester.get_user_hashed_password(1,'k00000000')
	assert get == 'pbkdf2:sha256:50000$igDdtEIs$17ab89312192f317e44bd9b29f2e04346519a6a06e79e4bfffc0156f44c7a13b'

def test_user_exist():
	get = tester.user_exist(1,'k00000000')
	assert get == True

def test_admin_status():
	tester.alter_admin_status(1,'k00000000', 1)
	get = tester.get_user_data(1,'k00000000')
	assert get['is_admin'] == 1

def test_activate():
	tester.activateAccount(1,'k00000000')
	get = tester.get_user_data(1,'k00000000')
	assert get['email_confirmed'] == 1

def test_date_change():
	tester.update_date_of_birth(1,'k00000000', '1991-02-21')
	get = tester.get_user_data(1,'k00000000')
	assert get['date_of_birth'] == datetime.date(1991, 2, 21)

def test_gender_change():
	tester.update_gender(1,'k00000000','Female')
	get = tester.get_user_data(1,'k00000000')
	assert get['gender'] == 'Female'

def test_buddy_change():
	tester.update_buddy_limit(1,'k00000000',1)
	get = tester.get_user_data(1,'k00000000')
	assert get['buddy_limit'] == 1

def test_hash_change():
	tester.update_hash_password(1,'k00000000', 'kkkkkkkkkkk')
	get = tester.get_user_hashed_password(1,'k00000000')
	assert get == 'kkkkkkkkkkk'

def test_column_size():
	get = tester.get_user_data(1,'k00000000')
	assert len(get) == 12

	
def test_delete():
	count = tester.delete_students(1, 'k00000000')
	assert count == 1