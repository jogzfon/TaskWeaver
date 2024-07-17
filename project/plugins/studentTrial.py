from student_management import StudentManagement

if __name__ == '__main__':
    sm = StudentManagement()
    result = sm("SELECT first_name, last_name FROM student_account WHERE student_id = 9;")
    print(result)
    
    