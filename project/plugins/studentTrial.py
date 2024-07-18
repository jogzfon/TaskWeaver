from student_management import StudentManagement

if __name__ == '__main__':
    sm = StudentManagement()
    result = sm("SELECT name FROM sqlite_master WHERE type='table';")
    print(result)
    
    