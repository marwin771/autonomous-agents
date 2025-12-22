# src/main.py
from langgraph.graph import StateGraph, END
from src.agents.state import AgentState
from src.agents.analyst import analyst_node
from src.agents.visualizer import visualizer_node
from langchain_core.messages import HumanMessage


# --- Conditional Routing Logic ---
def should_visualize(state: AgentState):
    full_history = " ".join([m.content.lower() for m in state["messages"]]) # combines all messages in the conversation
    keywords = ["plot", "graph", "chart", "visualize"] # words that indicate the user wants a visual

    if any(word in full_history for word in keywords):
        return "yes"
    return "no"


# --- Graph Assembly ---
workflow = StateGraph(AgentState) # creates graph

# Add our imported specialized nodes
workflow.add_node("analyst", analyst_node)
workflow.add_node("visualizer", visualizer_node)

# --- Define the flow ---
workflow.set_entry_point("analyst") # always start at the Analyst station

# After the analyst is done, run the should_visualize logic.
# If the answer is 'yes', go to the visualizer. If 'no', stop immediately (END).
workflow.add_conditional_edges(
    "analyst",
    should_visualize,
    {"yes": "visualizer", "no": END}
)
workflow.add_edge("visualizer", END) # once a chart is created, there are no more steps

app = workflow.compile()


# --- Entry Point for UI ---
def run_agent_workflow(user_id, db_key, query):
    initial_state = {
        "user_id": user_id,
        "database_key": db_key,
        "messages": [HumanMessage(content=query)],
        "data_summary": "",
        "has_visual": False
    }
    return app.invoke(initial_state) # kicks off the graph and runs the logic from start to finish