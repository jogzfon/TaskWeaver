from student_manager_tester import TestSystem
import pandas as pd

if __name__ == '__main__':
    # Make the query
    inp = "x"
    while inp != "exit":
        inp = input()
        result, description = TestSystem()(inp)
        print(description)