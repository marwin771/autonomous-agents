# src/agents/analyst.py
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from src.tools.sql_tools import get_db_for_user


def get_analyst_agent(user_id: str, db_key: str):
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    db = get_db_for_user(user_id, db_key)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    return create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type="openai-tools",
        handle_parsing_errors=True
    )