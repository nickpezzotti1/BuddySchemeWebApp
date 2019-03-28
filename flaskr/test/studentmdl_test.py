import flaskr.models.studentmdl as testmdl
import datetime

tester = testmdl.StudentModel('testing')


def test_student():
	count = tester.insert_student(1, 'k00000000', 'Bai', 'Ganyo', 'BSc Comp Sci', 1, 'Male', 0, 'pbkdf2:sha256:50000$igDdtEIs$17ab89312192f317e44bd9b29f2e04346519a6a06e79e4bfffc0156f44c7a13b', 0, 3)
	assert count == 1

	get = tester.get_user_hashed_password(1,'k00000000')
	assert get == 'pbkdf2:sha256:50000$igDdtEIs$17ab89312192f317e44bd9b29f2e04346519a6a06e79e4bfffc0156f44c7a13b'

	get = tester.user_exist(1,'k00000000')
	assert get == True

	tester.alter_admin_status(1,'k00000000', 1)
	tester.activateAccount(1,'k00000000')
	tester.update_date_of_birth(1,'k00000000', '1991-02-21')
	tester.update_gender(1,'k00000000','Female')
	tester.update_buddy_limit(1,'k00000000',1)
	tester.update_hash_password(1,'k00000000', 'kkkkkkkkkkk')

	get = tester.get_user_data(1,'k00000000')
	assert len(get) == 12

	assert get['is_admin'] == 1
	assert get['email_confirmed'] == 1
	assert get['date_of_birth'] == datetime.date(1991, 2, 21)
	assert get['gender'] == 'Female'
	assert get['buddy_limit'] == 1

	get = tester.get_user_hashed_password(1,'k00000000')
	assert get == 'kkkkkkkkkkk'

	count = tester.delete_students(1, 'k00000000')
	assert count == 1