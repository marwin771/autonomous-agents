# src/agents/analyst.py
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from src.tools.sql_tools import get_db_for_user
from langchain_core.messages import AIMessage
from src.agents.state import AgentState


def analyst_node(state: AgentState):
    """
    Node function to run the SQL Analyst Agent.
    """
    # 1. Initialize Agent
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    db = get_db_for_user(state["user_id"], state["database_key"]) # get the authorized database connection

    # toolkit provides the AI with tools to: list tables, check schemas, execute queries
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # create_sql_agent is a pre-built LangChain agent that knows how to
    # use those tools in a loop until it finds the answer.
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type="openai-tools",
        handle_parsing_errors=True
    )

    # 2. Execute query based on the last message
    user_input = state["messages"][-1].content
    response = agent.invoke({"input": user_input})

    # 3. Return the state update
    return {
        "messages": [AIMessage(content=response["output"])],
        "data_summary": response["output"]
    }