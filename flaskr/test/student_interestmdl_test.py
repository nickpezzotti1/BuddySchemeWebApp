import flaskr.models.student_interestmdl as testmdl
import flaskr.models.studentmdl as studentmdl
import flaskr.models.interestmdl as interestmdl

tester = testmdl.StudentInterestModel('testing')
student = studentmdl.StudentModel('testing')
interest = interestmdl.InterestModel('testing')

def test_student_interest():
	student.insert_student(1, 'k00000000', 'Bai', 'Ganyo', 'BSc Comp Sci', 1, 'Male', 0, 'kkkkkkkk', 0, 3)
	interest.insert_interest('Besting', 1)
	id = interest.select_interest('Besting', 1)
	id = id[0]['id']
	tester.insert_interest(1, 'k00000000', id)
	get = tester.get_interests(1, 'k00000000')
	assert 1 == len(get)

def test_delete():

	tester.delete_interests(1, 'k00000000')
	get = tester.get_interests(1, 'k00000000')
	assert 0 == len(get)

	student.delete_students(1, 'k00000000')
	get = interest.select_interest('Besting', 1)
	interest.delete_interest(get[0]['id'],1)
