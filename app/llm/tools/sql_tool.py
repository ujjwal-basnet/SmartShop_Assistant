from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_openai import OpenAI

DB_PATH = "sqlite:///app/db/smartshop_assistant.db"

def get_sql_tools(llm):
    # Wrap DB
    db = SQLDatabase.from_uri(DB_PATH)
    # Create toolkit
    sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    return sql_toolkit.get_tools()
