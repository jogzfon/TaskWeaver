import pandas as pd
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chat_models import ChatGoogleGenerativeAI
from langchain.chains import create_sql_query_chain
from taskweaver.plugin import Plugin, register_plugin
from langchain.utilities import SQLDatabase

@register_plugin
class SqliteAgent(Plugin):

    db_path = SQLDatabase.from_uri("sqlite:///sample_data/student_enrollment.db")
    model = None

    def __call__(self, query: str):
        api_type = self.config.get("api_type", "gemini")
        
        if api_type == "groq":
            model = ChatGroq(
                groq_api_key=self.config.get("api_key"),
                model_name=self.config.get("llama3-8b-8192"),
                temperature=0,
                verbose=True,
            )
        elif api_type == "gemini":
            model = ChatGoogleGenerativeAI(
                google_genai_api_key=self.config.get("api_key"),
                google_genai_api_version=self.config.get("api_version"),
                temperature=0,
                verbose=True,
            )
        else:
            raise ValueError("Invalid API type. Please check your config file.")

        prompt=PromptTemplate(
                """
                If the user asks about any queries, use the student_enrollment.db.
                {schema}

                Question: {question}
                If the user asks 
                Please only write the sql query.
                Do not add any query on sensitive informations like passwords and emails.
                Do not add any comments or extra text.
                Do not wrap the query in quotes or ```sql.
                SQL Query:"""
        )

        chain = create_sql_query_chain(
            model=model,
            db=self.db_path,
            question=query,
            prompt=prompt
            )
        
        response = chain.invoke({query: query})
        
        print(response)

        
