import sqlite3
import pandas as pd
# from langchain_community.utilities import SQLDatabase
from taskweaver.plugin import Plugin, register_plugin

@register_plugin
class StudentManagement(Plugin):
    def __call__(self, query: str):
        db_path = r"C:\OJT WORK\TaskWeaver\project\sample_data\student_system.db"
        try:
            connection = sqlite3.connect(db_path)
            print("Connection to the database established successfully.")
        except sqlite3.Error as e:
            print(f"Failed to connect to the database at {db_path}. Error: {e}")
            return "Error connecting to database"
        
        try:
            cursor = connection.cursor()
            # ... (rest of the code for printing table names and schema remains the same)
            
            cursor.execute(query)
            result = cursor.fetchall()
            df = pd.DataFrame(result)
            # Convert result to string
            if result:
                # Create a list of strings, each representing a row
                result_strings = [' | '.join(map(str, row)) for row in result]
                # Join all rows with newlines
                result_string = '\n'.join(result_strings)
            else:
                result_string = "No results found."
            
        except sqlite3.Error as e:
            print(f"Query execution failed. Error: {e}")
            result_string = "Error executing query"
        finally:
            connection.close()
            print("Connection to the database closed.")
        
        
        return df