class SchemaDatabaseManager:
    def __call__(self, query: str):
        try:
            import tiktoken
            import mysql.connector
            from mysql.connector import Error
            from operator import itemgetter
            from langchain_openai import ChatOpenAI
            from langchain.prompts import ChatPromptTemplate
            from langchain.schema.output_parser import StrOutputParser
            from langchain.schema.runnable import RunnableLambda, RunnableMap
        except ImportError as e:
            raise ImportError("Could not load imports.") from e
        
        connection = None
        cursor = None
        
        try:
            # Initialize the AI model
            model = ChatOpenAI(
                model_name="gpt-4o-mini",
                openai_api_key="sk-proj-CJlPobih142REd2ntVo5T3BlbkFJWtqE4ylEC6lnsH08gulm",
                temperature=0,
                top_p=1,
                verbose=True,
            )
            
            # Define the prompt template
            template = """Based on the following database schema, answer the user's question:
            {schema}
            User's Question: {question}
            Provide a concise answer based only on the information available in the schema, including table structures and row counts.
            Do not make assumptions about actual data. If the question cannot be answered based solely on the schema, state that clearly.
            Answer:"""
            prompt = ChatPromptTemplate.from_template(template)
            
            # Connect to the MySQL database
            connection = mysql.connector.connect(
                host="localhost",
                port=3306,
                database="mbiblio",
                user="root",
                password=""
            )
            
            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)
                
                def get_schema(_):
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    schemas = []
                    for table in tables:
                        table_name = table[list(table.keys())[0]]
                        cursor.execute(f"DESCRIBE {table_name}")
                        columns = cursor.fetchall()
                        cursor.execute(f"SELECT * FROM {table_name}")
                        rows = cursor.fetchall()
                        column_details = ', '.join([f'{col['Field']} ({col['Type']})' for col in columns])
                        row_details = '\n'.join([str(row) for row in rows])
                        table_schema = (f"Table: {table_name}\n"
                                        f"Columns: {column_details}\n"
                                        f"Rows:\n{row_details}\n")
                        schemas.append(table_schema)
                        # print(schemas)
                    return "\n\n".join(schemas)

                inputs = {
                    "schema": RunnableLambda(get_schema),
                    "question": itemgetter("question"),
                }
                chain = RunnableMap(inputs) | prompt | model | StrOutputParser()
                
                input_data = {"question": query}
                schema = inputs["schema"].invoke(input_data)
                question = inputs["question"](input_data)

                # Print the prompt
                # print(f"Prompt:\n{template.format(schema=schema, question=question)}")
                
                encoding = tiktoken.encoding_for_model("gpt-4o-mini")
                # Schema 
                tokens = encoding.encode(schema)
                token_count = len(tokens)
                
                # Question
                tokens2 = encoding.encode(question)
                token_count2 = len(tokens2)
                
                # Result
                result = chain.invoke(input_data)
                tokens3 = encoding.encode(result)
                token_count3 = len(tokens3)
                
                print("TOKEN CONSUMED:")
                print(f"The schema {token_count} tokens.\n")
                print(f"The question {token_count2} tokens.\n")
                print(f"The result {token_count3} tokens.\n")
                
                return result
        
        except Error as e:
            return f"MySQL Error: {e}"
        
        except Exception as e:
            return f"An unexpected error occurred: {e}"
        
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()