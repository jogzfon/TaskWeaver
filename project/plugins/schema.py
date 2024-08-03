import pandas as pd

class Schema:
    def __init__(self, dataframe: pd.DataFrame, name: str):
        self.dataframe = dataframe
        self.name = name

    def set_allowed_columns(self, allowed_columns=None):
        self.allowed_columns = allowed_columns
        
    def get_schema(self):
        if self.allowed_columns is None:
            self.allowed_columns = self.dataframe.columns

        schema = {
            "table_name": self.name,
            "columns": []
        }

        for column in self.dataframe.columns:
            if column in self.allowed_columns:
                col_info = {
                    "column_name": column,
                    "data_type": str(self.dataframe[column].dtype)
                }
                schema["columns"].append(col_info)

        return schema