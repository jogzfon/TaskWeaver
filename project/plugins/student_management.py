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
            print("Cursor created successfully.")
            
            cursor.execute(query)
            result = cursor.fetchall()
            print("Query executed successfully.")
            
            # Fetch column names
            column_names = [description[0] for description in cursor.description]
            print("Column names fetched successfully:", column_names)
            
            df = pd.DataFrame(result, columns=column_names)
            print("DataFrame created successfully.")
            
            # # Convert result to string if needed
            # if not df.empty:
            #     result_string = df.to_string(index=False)
            # else:
            #     result_string = "No results found."
            
        except sqlite3.Error as e:
            print(f"Query execution failed. Error: {e}")
            # result_string = "Error executing query"
        finally:
            connection.close()
            print("Connection to the database closed.")
        
        return df
        
# @register_plugin
# class StudentManagement(Plugin):
#     def __call__(self, query: str):
#         value = ""
#         db = SQLDatabase.from_uri("sqlite:///C:/OJT WORK/TaskWeaver/project/sample_data/student_system.db")
#         result = db.run(query, fetch="cursor")
#         result_list = list(result.mappings())
#         value = str(result_list)
#         return value

# import sqlalchemy
# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker
# import pandas as pd
# from taskweaver.plugin import Plugin, register_plugin


# @register_plugin
# class StudentManagement(Plugin):
#     def __call__(self, query: str):
#         db_path = r"C:\OJT WORK\TaskWeaver\project\sample_data\student_system.db"
#         engine = create_engine(f"sqlite:///{db_path}")
#         Session = sessionmaker(bind=engine)
#         try:
#             session = Session()
#             print("Connection to the database established successfully.")
#         except sqlalchemy.exc.SQLAlchemyError as e:
#             print(f"Failed to connect to the database at {db_path}. Error: {e}")
#             return "Error connecting to database"
        
#         try:
#             result = session.execute(text(query))
#             df = pd.DataFrame(result)
#             # if result.returns_rows:
#             #     result_string = '\n'.join([str(row) for row in result])
#             # else:
#             #     result_string = "No results found."
            
#             session.commit()
#         except sqlalchemy.exc.SQLAlchemyError as e:
#             print(f"Query execution failed. Error: {e}")
#             result_string = "Error executing query"
#         finally:
#             session.close()
#             print("Connection to the database closed.")
        
#         return df
