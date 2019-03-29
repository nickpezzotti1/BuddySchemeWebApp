import flaskr.models.allocationmdl as testmdl
import flaskr.models.studentmdl as studentmdl

tester = testmdl.AllocationModel('testing')
student = studentmdl.StudentModel('testing')

def test_make_allocation():
	student.insert_student(1, 'k00000000', 'Bai', 'Ganyo', 'BSc Comp Sci', 1, 'Male', 0, 'kkkkkkkk', 0, 3)
	student.insert_student(1, 'k99999999', 'Dai', 'Manyo', 'BSc Comp Sci', 1, 'Male', 1, 'kkkkkkkk', 0, 3)
	tester.insert_mentor_mentee(1, 'k00000000', 'k99999999')
	get = tester.get_allocation(1, 'k00000000', 'k99999999')
	assert 0 == len(get)


def test_delete_allocation():
	tester.remove_allocation(1, 'k00000000', 'k99999999')
	student.delete_students(1, 'k00000000')
	student.delete_students(1, 'k99999999')
	get = tester.get_allocation(1, 'k00000000', 'k99999999')
	assert 0 == len(get)

