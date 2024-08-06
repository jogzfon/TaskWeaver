# TaskWeaver Plugins

## Introduction

**Plugins** are the user-defined functions that extend TaskWeaver CodeInterpreter's capabilities. More details about plugins can be found in the Plugin Introduction. In TaskWeaver, the collection of available plugins are attached to the Conversation object.

# TaskWeaver default plugins
- anomaly_detection
- ascii_render
- image2text
- klarna_search
- paper_summary
- sql_pull_data
- text_classification

## ================================================== Plugins We Made ===================================================================

# == Test Plugins ==
- animal_planet - a simple plugin we made to familiarize how taskweaver plugins work.
- database_manager - **Issue:** Allowing the AI to decide the SQL code to be executed based on user requests poses significant security risks. However, it serves as a useful reference for developing future plugins that can modify database tables according to user requests in a controlled and secure manner.


# == Final Plugin ==
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
- Runs only when the following is removed from the class:

    from taskweaver.plugin import Plugin, register_plugin - This line

    @register_plugin - This line
    class SchemaDatabaseManager(Plugin): - The "Plugin" word

- Main Execution:
    - Creates an instance of SchemaDatabaseManager.
    - Continuously asks for user input until "exit" is typed.
    - Sends user input to the SchemaDatabaseManager instance.
    - Prints the response from the plugin.

### Additional Information
You can find more about how plugins are made from TaskWeaver's official documentation:
- [TaskWeaver Documentation] https://microsoft.github.io/TaskWeaver/docs/plugin/plugin_intro
- Before running the TaskWeaver be sure to install the requirements:
    pip install -r requirements.txt

- In installing additional requirements when "pip install <libraryname>" does not work, use "py -m pip install <libraryname>"
- Plugins must consist the yaml file and the py file. 
- In the yaml file here are some notes:
    
    name: name of the plugin
    enabled: false            - sets the availability of the plugin to use in taskweaver 
    required: false           - sets it so it will be executed no matter what request the user makes to the TaskWeaver
    plugin_only: true         - sets the py code as a plugin only and will not be used when taskweaver generates a custom code
    description: >-           - this is what taskweaver reads to determine if it has to use this plugin based on the user request 
    examples:                 - sets the format for what code to be generated and executed when taskweaver decides to use this plugin 
    
    parameters:               - you can set multiple parameters / inputs depending on how many inputs your class plugin requires
    - name: 
        type:
        required: 
        description: >-       - this further clarifies what the taskweaver passes on as inputs to the class


    returns:                  - you can set multiple parameters / inputs depending on how many outputs your class plugin requires
    - name: 
        type: 
        description: >-       - this sets the requirement of what the final output when the plugin is run should be

- In the py file here are some notes:
    To register the py class as a plugin this should be done:

        from taskweaver.plugin import Plugin, register_plugin

        @register_plugin
        class NameOfTheClass(Plugin): 

    Else you can run it normally like a python file to test the code.

- If the python file does not work when normally run and not registered as a plugin in taskweaver. It will display something similar to these:      "<Name of the plugin> module does not exist" / "<Name of the plugin> module is not found"

- AI model configuration or changes must be done in taskweaver_config.json and a few notes on it:
    
    "llm.response_format": "json_object"
        - This tells the Language Model (LLM) to format its responses as JSON objects. This structured format can make it easier to parse and process the LLM's outputs programmatically.

    "execution_service.kernel_mode": "local"
        - This setting specifies that the execution environment for running code should be local, rather than remote or in a cloud environment. 

    "execution_service.timeout": 300
        - This sets a timeout of 300 seconds (5 minutes) for code execution. If a task takes longer than this, it will be terminated.

    "log.level": "INFO"
        - This sets the logging level to INFO, which means it will log general information about the system's operation, but not detailed debug information.

        - You can set it to any of the following:
            DEBUG: Most detailed logging level, useful for development and troubleshooting.
            INFO: General information about the system's operation (as we saw in the previous configuration).
            WARNING: Logs warnings and all higher severity events.
            ERROR: Only logs error events.
            CRITICAL: Logs only critical errors.
    
    "planner.max_retry": 3
        - This allows the planner component to retry a failed operation up to 3 times before giving up.

    "human_input_mode": "NEVER"
        - This setting prevents the system from ever prompting for human input during its operation. It will attempt to complete all tasks autonomously.

        - You can set it to any of the following:
            NEVER: As we saw, this mode never prompts for human input.
            AUTO: The system decides when to ask for human input based on its confidence in handling a task.
            ALWAYS: The system always asks for human input at certain points in its operation.

            These modes allow you to control the level of human interaction with the system:

            NEVER is useful for fully automated scenarios.
            AUTO provides a balance, allowing the system to operate autonomously when confident but seek help when needed.
            ALWAYS is useful for scenarios where you want to ensure human oversight at key points in the process.

- For debugging you can access the project/taskweaver.log for more info

