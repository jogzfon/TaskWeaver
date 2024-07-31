import sqlite3

from taskweaver.plugin import Plugin, register_plugin

@register_plugin
class SqlConnect(Plugin):
    def __call__(self, connect: str):
        # if(len(name)!=0):
        #     name = "I am a Doug!"
        #     return name
        # else:
        #     name = "I am king!"
        #     return name

        def connect_to_db(db_name):
            if db_name == "student_system.db":
                db_path = "C:\\Users\\Systems\\Documents\\OJT\\TaskWeaver\\project\\sample_data\\student_system.db"
            elif db_name == "student_enrollment.db":
                db_path = "C:\\Users\\Systems\\Documents\\OJT\\TaskWeaver\\project\\sample_data\\student_enrollment.db"
            else:
                return "Invalid database name."
                
            try:
                connection = sqlite3.connect(db_path)
                print(f"Connected to {db_name}")
                return connection
            except sqlite3.Error as e:
                return f"Failed to connect to the database. Error: {e}"
            
        def execute_query(connection, query):
            try:
                cursor = connection.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
                return results
            except sqlite3.Error as e:
                return f"Failed to execute query. Error: {e}"    

        # # Example usage
        # if(connect == "student_system.db"):
        #     db_name = "student_system.db"
        #     connection_status = connect_to_db(db_name)
        #     return print(connection_status)
        # elif(connect == "student_enrollment.db"):
        #     db_name = "student_system.db"
        #     connection_status = connect_to_db(db_name)
        #     return print(connection_status)
        # else:
        #         return "Invalid database name."
        if connect in ["student_system.db", "student_enrollment.db"]:
            connection = connect_to_db(connect)
            if isinstance(connection, str):
                return connection  # If the connection is an error message
            
            query = "SELECT first_name, last_name FROM student_account;"
            query_results = execute_query(connection, query)
            
            connection.close()
            return query_results
        else:
            return "Invalid database name."