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
                try:
                    connection = sqlite3.connect(db_path)
                    return "Connected to the database successfully."
                except sqlite3.Error as e:
                    return f"Failed to connect to the database. Error: {e}"
            

        # Example usage
        if(connect == "student_system.db"):
            db_name = "student_system.db"
            connection_status = connect_to_db(db_name)
            return print(connection_status)
        else:
                return "Invalid database name."
            

