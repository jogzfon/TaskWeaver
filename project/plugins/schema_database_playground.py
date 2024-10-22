# from student_manager_tester import TestSystem
# import pandas as pd

# if __name__ == '__main__':
#     test_system = TestSystem()
#     inp = "x"
#     while inp != "exit":
#         inp = input("Enter your query (type 'exit' to quit): ")
#         if inp.lower() != "exit":
#             result, description = test_system(inp)
#             print(description)
#     test_system.close_connection()

from schema_database_manager import SchemaDatabaseManager
import pandas as pd

if __name__ == '__main__':
    test_system = SchemaDatabaseManager()
    inp = "x"
    while inp != "exit":
        inp = input("Enter your query (type 'exit' to quit): ")
        if inp.lower() != "exit":
            result = test_system(inp)
            print(result)
    test_system.close_connection()