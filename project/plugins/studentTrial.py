from student_manager_tester import TestSystem

if __name__ == '__main__':
    sm = TestSystem()
    result = sm("SELECT first_name, last_name FROM student_account WHERE student_id = 9;")
    print(result)
    
    