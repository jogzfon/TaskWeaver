from taskweaver.plugin import Plugin, register_plugin

@register_plugin
class SchemaDatabaseManager(Plugin):
    def __call__(self, message: str):
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
                database="biblio_system",
                user="root",
                password=""
            )
            
            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)
                
                def get_schema(_):
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    schemas = []
                    
                    # Column Exceptions for each table in database
                    biblio_column_exceptions = ['medium', 'part_number', 'part_name', 'unititle', 'notes', 'serial', 'seriestile', 'copyrightdate', 'abstract'] 
                    biblioitems_column_exceptions = ['volume', 'number', 'issn', 'ean', 'publicationyear', 'publishercode', 'volumedate', 'volumedesc', 'collectiontitle', 'collectionissn', 'collectionvolume', 'editionstatement', 'editionresponsibility', 'notes', 'size', 'place', 'lccn', 'url', 'cn_class', 'cn_item', 'cn_suffix', 'cn_sort', 'agerestriction', 'totalissues']
                    items_column_exceptions = ['replacementprice', 'replacementpricedate','datelastborrowed', 'stack', 'damaged', 'damaged_on', 'itemlost', 'itemlost_on', 'withdrawn', 'withdrawn_on', 'coded_location_qualifier', 'issues', 'renewals', 'reserves', 'restricted', 'itemnotes', 'itemnotes_nonpublic', 'deleted_on', 'onloan', 'materials', 'uri', 'more_subfields_xml', 'enumchron', 'new_status', 'exclude_from_local_holds_priority']
                    
                    # List of columns to exclude (add your column names here)
                    excluded_columns = biblio_column_exceptions + biblioitems_column_exceptions + items_column_exceptions
                    
                    # Getting the schema for each table in the database    
                    for table in tables:
                        table_name = table[list(table.keys())[0]]
                        cursor.execute(f"DESCRIBE {table_name}")
                        columns = cursor.fetchall()
                        
                        # Change the limit of this to how many columns in the database you prefer or remove the limit to use all rows in the database
                        cursor.execute(f"SELECT * FROM {table_name} LIMIT 15")
                        rows = cursor.fetchall()
                        
                        # Filter out excluded columns
                        filtered_columns = [col for col in columns if col['Field'] not in excluded_columns]
                        
                        column_details = ', '.join([f'{col["Field"]} ({col["Type"]})' for col in filtered_columns])
                        
                        if rows:
                            # Filter out excluded columns from row data
                            filtered_rows = [{k: v for k, v in row.items() if k not in excluded_columns} for row in rows]
                            row_details = '\n'.join([str(row) for row in filtered_rows])
                        else:
                            row_details = "No rows available"
                        
                        table_schema = (f"Table: {table_name}\n"
                                        f"Columns: {column_details}\n"
                                        f"Rows:\n{row_details}\n")
                        schemas.append(table_schema)
                    return "\n\n".join(schemas)

                inputs = {
                    "schema": RunnableLambda(get_schema),
                    "question": itemgetter("question"),
                }
                chain = RunnableMap(inputs) | prompt | model | StrOutputParser()
                
                input_data = {"question": message}
                schema = inputs["schema"].invoke(input_data)
                question = inputs["question"](input_data)

                # Print the schema and prompt info
                # print(f"Prompt:\n{template.format(schema=schema, question=question)}")
                
                #Token counter model reference
                encoding = tiktoken.encoding_for_model("gpt-4o-mini")
                
                # Schema Token Counter
                tokens = encoding.encode(schema)
                token_count = len(tokens)
                
                # Question Token Counter
                tokens2 = encoding.encode(question)
                token_count2 = len(tokens2)
                
                result = chain.invoke(input_data)
                
                # Result Token Counter
                tokens3 = encoding.encode(result)
                token_count3 = len(tokens3)
                
                # TOKEN INFO
                print(f"TOTAL TOKEN CONSUMED: {token_count+token_count2+token_count3}")
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