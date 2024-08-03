from schema import Schema
import pandas as pd

class SchemaManager:
    def __init__(self):
        self.schemas = []

    def add_schema(self, dataframe: pd.DataFrame, name: str, allowed_columns=None):
        schema = Schema(dataframe, name)
        schema.set_allowed_columns(allowed_columns)
        self.schemas.append(schema)

    def get_all_schemas(self):
        return [schema.get_schema() for schema in self.schemas]