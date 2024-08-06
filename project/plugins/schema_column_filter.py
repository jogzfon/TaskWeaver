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