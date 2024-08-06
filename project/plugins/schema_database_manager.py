from taskweaver.plugin import Plugin, register_plugin

@register_plugin
class SchemaDatabaseManager(Plugin):
    def __call__(self, message: str):
        try:
            # import tiktoken
            
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
            template = """You are given a database schema and a user's question. Based on the schema provided below, answer the user's question directly.

            Schema:
            {schema}

            User's Question:
            {question}

            Your answer should be:
            - Based solely on the information provided in the schema.
            - Do not make assumptions or use any external data.
            - Provide a direct answer without additional explanations or step-by-step procedures.
            - If the question cannot be answered with the given schema, clearly state that.
            - Dont show Null and None values
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
                
                def get_schema(message):
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    schemas = []
                    
                    # Column Exceptions for each table in database or columns that must not be added
                    # column_exceptions = {
                    #     'biblio': ['medium', 'part_number', 'part_name', 'unititle', 'notes', 'serial', 'seriestile', 'copyrightdate', 'abstract'],
                    #     'biblioitems': ['volume', 'number', 'issn', 'ean', 'publicationyear', 'publishercode', 'volumedate', 'volumedesc', 'collectiontitle', 'collectionissn', 'collectionvolume', 'editionstatement', 'editionresponsibility', 'notes', 'size', 'place', 'lccn', 'url', 'cn_class', 'cn_item', 'cn_suffix', 'cn_sort', 'agerestriction', 'totalissues'],
                    #     'items': ['replacementprice', 'replacementpricedate','datelastborrowed', 'stack', 'damaged', 'damaged_on', 'itemlost', 'itemlost_on', 'withdrawn', 'withdrawn_on', 'coded_location_qualifier', 'issues', 'renewals', 'reserves', 'restricted', 'itemnotes', 'itemnotes_nonpublic', 'deleted_on', 'onloan', 'materials', 'uri', 'more_subfields_xml', 'enumchron', 'new_status', 'exclude_from_local_holds_priority']
                    # }
                    
                    for table in tables:
                        table_name = table[list(table.keys())[0]]
                        cursor.execute(f"DESCRIBE {table_name}")
                        columns = cursor.fetchall()
                        
                        # Initial Filter of the table columns
                        column_filter = SchemaColumnFilter(columns)
                        prefiltered_columns = column_filter(message)
                        
                        # Filter out excluded columns
                        # excluded_for_table = column_exceptions.get(table_name, [])
                        excluded_for_table = COLUMN_EXCEPTIONS.get_exceptions(table_name)
                        filtered_columns = [col for col in prefiltered_columns if col['Field'] not in excluded_for_table]
                        
                        if not filtered_columns:
                            continue  # Skip this table if no relevant columns after filtering
                        
                        column_names = [col["Field"] for col in filtered_columns]
                        column_details = ', '.join([f'{col["Field"]} ({col["Type"]})' for col in filtered_columns])
                        
                        # Fetch sample rows
                        selected_columns = ', '.join(column_names)
                        cursor.execute(f"SELECT {selected_columns} FROM {table_name} LIMIT 15") #Adjust the limit or remove it as see fit for database size, do the same for the brevity
                        rows = cursor.fetchall()
                        
                        if rows:
                            # Filter out excluded columns from row data
                            filtered_rows = [{k: v for k, v in row.items() if k not in excluded_for_table} for row in rows]
                            row_details = '\n'.join([str(row) for row in filtered_rows[:15]])  # Limit to 15 rows for brevity
                        else:
                            row_details = "No rows available"
                        
                        table_schema = (f"Table: {table_name}\n"
                                        f"Columns: {column_details}\n"
                                        f"Sample Rows:\n{row_details}\n")
                        schemas.append(table_schema)
                    
                    return "\n\n".join(schemas) if schemas else "No relevant schema information found."

                inputs = {
                    "schema": RunnableLambda(get_schema),
                    "question": itemgetter("question"),
                }
                chain = RunnableMap(inputs) | prompt | model | StrOutputParser()
                
                input_data = {"question": message}
                schema = inputs["schema"].invoke(input_data)
                question = inputs["question"](input_data)

                result = chain.invoke(input_data)
                
                # # Print the schema and prompt info
                # print(f"Prompt:\n{template.format(schema=schema, question=question)}")
                
                # #Token counter model reference
                # encoding = tiktoken.encoding_for_model("gpt-4o-mini")
                
                # # Schema Token Counter
                # tokens = encoding.encode(schema)
                # token_count = len(tokens)
                
                # # Question Token Counter
                # tokens2 = encoding.encode(question)
                # token_count2 = len(tokens2)
                
                
                # # Result Token Counter
                # tokens3 = encoding.encode(result)
                # token_count3 = len(tokens3)
                
                # # TOKEN INFO
                # print(f"TOTAL TOKEN CONSUMED: {token_count+token_count2+token_count3}")
                # print(f"The schema {token_count} tokens.\n")
                # print(f"The question {token_count2} tokens.\n")
                # print(f"The result {token_count3} tokens.\n")
                
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
                
                
class SchemaColumnExceptions:
    def __init__(self):
        self.exceptions = {}

    def add_exceptions(self, table_name, columns):
        """Add exceptions for a specific table."""
        self.exceptions[table_name] = columns

    def get_exceptions(self, table_name):
        """Get exceptions for a specific table."""
        return self.exceptions.get(table_name, [])

    def get_all_exceptions(self):
        """Get all exceptions across all tables."""
        return [col for exceptions in self.exceptions.values() for col in exceptions]

    def __str__(self):
        """String representation of all exceptions."""
        return str(self.exceptions)
    

# Create an instance and add exceptions
COLUMN_EXCEPTIONS = SchemaColumnExceptions()

COLUMN_EXCEPTIONS.add_exceptions('biblio', [
    'medium', 'part_number', 'part_name', 'unititle', 'notes', 'serial',
    'seriestile', 'copyrightdate', 'abstract'
])

COLUMN_EXCEPTIONS.add_exceptions('biblioitems', [
    'volume', 'number', 'issn', 'ean', 'publicationyear', 'publishercode',
    'volumedate', 'volumedesc', 'collectiontitle', 'collectionissn',
    'collectionvolume', 'editionstatement', 'editionresponsibility', 'notes',
    'size', 'place', 'lccn', 'url', 'cn_class', 'cn_item', 'cn_suffix',
    'cn_sort', 'agerestriction', 'totalissues'
])

COLUMN_EXCEPTIONS.add_exceptions('items', [
    'replacementprice', 'replacementpricedate', 'datelastborrowed', 'stack',
    'damaged', 'damaged_on', 'itemlost', 'itemlost_on', 'withdrawn',
    'withdrawn_on', 'coded_location_qualifier', 'issues', 'renewals',
    'reserves', 'restricted', 'itemnotes', 'itemnotes_nonpublic', 'deleted_on',
    'onloan', 'materials', 'uri', 'more_subfields_xml', 'enumchron',
    'new_status', 'exclude_from_local_holds_priority'
])

class SchemaColumnFilter:
    def __init__(self, columns_data):
        self.columns_data = columns_data
        
    def __call__(self, message: str):
        from langchain_openai import ChatOpenAI
        from langchain.prompts import ChatPromptTemplate
        from langchain.schema.output_parser import StrOutputParser
        from langchain.schema.runnable import RunnableMap
        
        model = ChatOpenAI(
                model_name="gpt-4o-mini",
                openai_api_key="sk-proj-CJlPobih142REd2ntVo5T3BlbkFJWtqE4ylEC6lnsH08gulm",
                temperature=0,
                top_p=1,
                verbose=True,
            )
        
        # Convert columns_data to a string format
        schema_str = "\n".join([f"{col['Field']} ({col['Type']})" for col in self.columns_data])

        prompt = ChatPromptTemplate.from_template(
            """You are an AI assistant for a database application.
            Given the following database schema:
            {schema}
            
            And the user's message:
            {message}
            
            Determine which columns from the schema are relevant to the user's message.
            Always include these columns regardless of the user's message itemnumber, biblionumber, biblioitemnumber
            Return only the names of the relevant columns, separated by commas.
            If no columns are relevant, return "None".
            """
        )
        
        chain = (
            RunnableMap({
                "schema": lambda _: schema_str,
                "message": lambda x: x
            })
            | prompt
            | model
            | StrOutputParser()
        )
        
        try:
            result = chain.invoke(message)
            
            # Convert the result back to a list of column dictionaries
            if result.lower() == "none":
                return []
            else:
                relevant_column_names = set(name.strip().lower() for name in result.split(','))
                return [col for col in self.columns_data if col['Field'].lower() in relevant_column_names]
        except Exception as e:
            print(f"Error in SchemaColumnFilter: {e}")
            return self.columns_data  # Return all columns if there's an error