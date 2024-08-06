# TaskWeaver Plugins

## Introduction

**Plugins** are the user-defined functions that extend TaskWeaver CodeInterpreter's capabilities. More details about plugins can be found in the Plugin Introduction. In TaskWeaver, the collection of available plugins are attached to the Conversation object.

## Plugins We Made

### schema_column_exceptions.py
- This code defines a SchemaColumnExceptions class to manage and track exceptions for specific columns in database tables.
- The class has methods to add exceptions for a table, retrieve exceptions for a table, get all exceptions across tables, and provide a string representation of all exceptions.
- The COLUMN_EXCEPTIONS instance is created and populated with column exceptions for three tables: biblio, biblioitems, and items. 
- This setup helps organize and access column exceptions for different tables in a structured way.

### schema_column_filter.py
- This code defines a SchemaColumnFilter class that filters database columns based on relevance to a user’s message using the LangChain library with an OpenAI model. 
- Class: SchemaColumnFilter filters database columns based on user messages.
- Initialization: Takes columns_data, a list of column details.
- Call Method:
    - Uses LangChain and OpenAI to process user messages and schema.
    - Creates a string representation of the schema and prompts the AI model.
    - Gets relevant columns or "None" from the AI model.
- Processing: Maps the schema and message to the prompt, parses the result, and filters columns accordingly.
- Error Handling: Returns all columns if an error occurs.

### schema_database_manager.py
- SchemaDatabaseManager: Manages database interactions and uses an AI model to answer questions about the database schema.
    - Connects to MySQL, retrieves table and column information.
    - Filters columns based on the user’s message and predefined exceptions.
    - Uses LangChain to prompt the AI model for a relevant answer.

- SchemaColumnExceptions: Stores and manages column exceptions for different tables.

- Methods to add, get, and list exceptions for tables.

- SchemaColumnFilter: Filters database columns based on relevance to a user’s message using an AI model.

- Converts column data to string, sets up a prompt, and uses LangChain for processing.

### schema_database_manager.yaml
- Function: Answers questions about the database schema.
- Usage Example:
    - result = schema_database_manager("Give me the names of the authors")
- Parameters:
    - message: str (Required) – The user's question.
- Returns:
    - result: str – The answer based on schema information.
- Notes:
    - Connects to a MySQL database ("biblio_system").
    - Uses GPT-4o mini model for responses.
    - Excludes certain columns to focus on relevant data.
    - Monitors token usage and handles errors.
- Dependencies:
    - Requires taskweaver, tiktoken, mysql-connector-python, langchain, langchain_openai.

### schema_database_playground.py
- Uses the SchemaDatabaseManager class.
- Main Execution:
    - Creates an instance of SchemaDatabaseManager.
    - Continuously asks for user input until "exit" is typed.
    - Sends user input to the SchemaDatabaseManager instance.
    - Prints the response from the plugin.

### Additional Information
You can find more about how plugins are made from TaskWeaver's official documentation:
- [TaskWeaver Documentation] https://microsoft.github.io/TaskWeaver/docs/plugin/plugin_intro