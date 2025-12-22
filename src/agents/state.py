# src/agents/state.py
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    user_id: str
    database_key: str
    # 'add_messages' tells LangGraph to append to history instead of overwriting it
    messages: Annotated[List[BaseMessage], add_messages]
    data_summary: str # Stores the text result from the SQL query
    has_visual: bool # A flag to track if a chart was created