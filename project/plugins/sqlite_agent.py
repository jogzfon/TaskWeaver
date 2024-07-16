import pandas as pd
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from taskweaver.plugin import Plugin, register_plugin

@register_plugin
class SqliteAgent(Plugin):
    db_path = None

    def __call__(self, query: str):
        api_type = self.config.get("api_type", "gemini")
        if api_type == "groq":
            model = ChatGroq(
                groq_api_key=self.config.get("api_key"),
                model_name=self.config.get("deployment_name"),
                temperature=0,
                verbose=True,
            )
        elif api_type == "gemini":
            model = ChatGemini(
                gemini_api_key=self.config.get("api_key"),
                model_name=self.config.get("deployment_name"),
                temperature=0,
                verbose=True,
            )
        else:
            raise ValueError("Invalid API type. Please check your config file.")