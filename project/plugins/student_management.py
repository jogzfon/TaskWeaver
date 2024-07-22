import pandas as pd
import mysql.connector
from mysql.connector import Error
from taskweaver.plugin import Plugin, register_plugin

@register_plugin
class StudentManagement(Plugin):
    def __call__(self, query: str):
        connection = None
        cursor = None
        
        try:
            connection = mysql.connector.connect(
                host='localhost',
                port=3306,
                database='student_system',
                user='root',
                password=''
            )
            
            if connection.is_connected():            
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query)
                result = cursor.fetchall()
                
                if result:
                    df = pd.DataFrame(result)
                    print("DataFrame created successfully.")
                else:
                    df = pd.DataFrame()
                    print("Query returned no results.")
                
                return df
        
        except mysql.connector.Error as e:
            print(f"MySQL Error: {e}")
            return None
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
        
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
            print("Connection to the database closed.")
        
# @register_plugin
# class StudentManagement(Plugin):
#     def __call__(self, query: str):
#         df = pd.DataFrame()
#         db = SQLDatabase.from_uri("sqlite:///C:/OJT WORK/TaskWeaver/project/sample_data/student_system.db")
#         result = db.run(query, fetch="cursor")
#         df = pd.DataFrame(result)
#         return df

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

