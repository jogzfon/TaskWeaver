import re
import mysql.connector
import pandas as pd
from mysql.connector import Error
from operator import itemgetter
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnableMap
from taskweaver.plugin import Plugin, register_plugin

@register_plugin
class StudentManagement(Plugin):
    def __call__(self, query: str):
        connection = None
        cursor = None
        
        try:
            model = GoogleGenerativeAI(
                model="gemini-pro",
                google_api_key="AIzaSyA0fCGtlAyxF_s_dBObsnL70xocI3GJlTE",
                temperature=0,
                top_p=1,
                verbose=True,
            )
            
            template = """Based on the table schema below, write a SQL query that would answer the user's question:
                {schema}

                Question: {question}
                Please only write the sql query.
                Do not add any query on sensitive informations like passwords and emails.
                Do not add any comments or extra text.
                Do not wrap the query in quotes or ```sql.
                SQL Query:"""
            prompt = ChatPromptTemplate.from_template(template)
            
            connection = mysql.connector.connect(
                host="localhost",
                port="3306",
                database="student_system",
                user="root",
                password=""
            )
            
            if connection.is_connected():            
                cursor = connection.cursor(dictionary=True)
                
                def get_schema(_):
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    schema = []
                    for table in tables:
                        table_name = table[list(table.keys())[0]]
                        cursor.execute(f"DESCRIBE {table_name}")
                        columns = cursor.fetchall()
                        schema.append(f"Table: {table_name}\nColumns: {', '.join([col['Field'] for col in columns])}\n")
                    return "\n".join(schema)

                inputs = {
                    "schema": RunnableLambda(get_schema),
                    "question": itemgetter("question"),
                }
                sql_response = RunnableMap(inputs) | prompt | model | StrOutputParser()

                sql = sql_response.invoke({"question": query})
                # Check for sensitive information in the generated SQL query
                sensitive_keywords = ["password", "email"]
                if any(keyword in sql.lower() for keyword in sensitive_keywords):
                    return pd.DataFrame(), "The generated SQL query contains sensitive information and will not be executed."

                 # Check for non-read-only queries in the generated SQL query using regex
                non_readonly_keywords = r"\b(insert|update|delete|create|alter|drop)\b"
                if re.search(non_readonly_keywords, sql, re.IGNORECASE):
                    return pd.DataFrame(), "The generated SQL query is not read-only and will not be executed."
                
                cursor.execute(sql)
                # cursor.commit()
                result = cursor.fetchall()
                
                if result:
                    df = pd.DataFrame(result)
                    df.index = range(1, len(df) + 1)  # Set the index to start at 1
                else:
                    df = pd.DataFrame()
                
                if len(df) == 0:
                    return df, (
                        f"I have generated a SQL query based on `{query}`.\nThe SQL query is {sql}.\n" f"The result is empty."
                    )
                else:
                    return df, (
                        f"I have generated a SQL query based on `{query}`.\nThe SQL query is {sql}.\n"
                        f"There are {len(df)} rows in the result.\n"
                        f"The rows are:\n{df.to_markdown()}"
                    )
        
        except mysql.connector.Error as e:
            return pd.DataFrame(), f"MySQL Error: {e}"

        except Exception as e:
            return pd.DataFrame(), f"An unexpected error occurred: {e}"
        
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()