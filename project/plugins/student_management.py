import sqlite3
import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from taskweaver.plugin import Plugin, register_plugin

@register_plugin
class StudentManagement(Plugin):
    def __call__(self, query: str):
        try:          
            # Try to establish a connection to the database
            db_path = "C:\OJT WORK\TaskWeaver\project\sample_data\student_enrollment.db"
            connection = sqlite3.connect(db_path)
            print("Connection to the database established successfully.")
        except sqlite3.Error as e:
            # Handle the error if the connection fails
            print(f"Failed to connect to the database at {db_path}. Error: {e}")
            return []

        try:
            # Create a cursor object
            cursor = connection.cursor()

            # Print the names of all tables in the database
            cursor.execute(query)
            tables = cursor.fetchall()
            print("Tables in the database:")
            for table in tables:
                print(table[0])

            # If no tables are found, log a message
            if not tables:
                print("No tables found in the database.")

            # Print the schema for each table
            for table in tables:
                print(f"\nSchema for table {table[0]}:")
                cursor.execute(f"PRAGMA table_info({table[0]});")
                columns = cursor.fetchall()
                for column in columns:
                    print(f"Column: {column[1]}, Type: {column[2]}, Not Null: {bool(column[3])}, Default: {column[4]}")

            # Execute the provided query
            cursor.execute(query)
            result = cursor.fetchall()
        except sqlite3.Error as e:
            # Handle any errors that occur during query execution
            print(f"Query execution failed. Error: {e}")
            result = []
        finally:
            # Ensure the connection is closed
            connection.close()
            print("Connection to the database closed.")

        return result

class Main():
    if __name__ == "__main__":
        resp = StudentManagement("SELECT name FROM sqlite_master WHERE type='table'")
        print(resp)
