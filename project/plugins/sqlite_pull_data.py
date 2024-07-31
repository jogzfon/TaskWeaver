import re
import sqlite3
import pandas as pd
from operator import itemgetter
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnableMap
from taskweaver.plugin import Plugin, register_plugin
import sqlalchemy as sa

@register_plugin
class SqlitePullData(Plugin):
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
            
            connection = sqlite3.connect("C:\\Users\\Systems\\Documents\\OJT\\TaskWeaver\\project\\sample_data\\student_system.db")
            cursor = connection.cursor()
            
            def get_schema(_):
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                schema = []
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    schema.append(f"Table: {table_name}\nColumns: {', '.join([col[1] for col in columns])}\n")
                return "\n".join(schema)

            inputs = {
                "schema": RunnableLambda(get_schema),
                "question": itemgetter("question"),
            }
            sql_response = RunnableMap(inputs) | prompt | model | StrOutputParser()

            sql = sql_response.invoke({"question": query})

            # Check for non-read-only queries in the generated SQL query using regex
            non_readonly_keywords = r"\b(insert|update|delete|create|alter|drop)\b"
            if re.search(non_readonly_keywords, sql, re.IGNORECASE):
                return pd.DataFrame(), "The generated SQL query is not read-only and will not be executed."
            
            cursor.execute(sql)
            result = cursor.fetchall()
            
            if result:
                df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
                print("DataFrame created successfully.")
            else:
                df = pd.DataFrame()
                print("Query returned no results.")
            
            if len(df) == 0:
                return df, (
                    f"I have generated a SQL query based on `{query}`.\nThe SQL query is {sql}.\n" f"The result is empty."
                )
            else:
                return df, (
                    f"I have generated a SQL query based on `{query}`.\nThe SQL query is {sql}.\n"
                    f"There are {len(df)} rows in the result.\n"
                    f"The first {min(5, len(df))} rows are:\n{df.head(min(5, len(df))).to_markdown()}"
                )
        
        except sqlite3.Error as e:
            print(f"SQLite Error: {e}")
            return pd.DataFrame(), f"SQLite Error: {e}"

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return pd.DataFrame(), f"An unexpected error occurred: {e}"
        
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                print("Connection to the database closed.")
