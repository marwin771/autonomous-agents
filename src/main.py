# src/main.py
import re
import os
from langgraph.graph import StateGraph, END
from src.agents.state import AgentState
from src.agents.analyst import get_analyst_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_experimental.utilities import PythonREPL
from langchain_openai import ChatOpenAI

# --- Node 1: The Analyst Logic ---
def run_analyst_node(state: AgentState):
    agent = get_analyst_agent(state["user_id"], state["database_key"])

    # Get the latest user message
    user_input = state["messages"][-1].content

    # Run the agent
    response = agent.invoke({"input": user_input})

    # Update state: Save the agent's text and the raw data result
    return {
        "messages": [AIMessage(content=response["output"])],
        "data_summary": response["output"]  # In a real app, you'd pass a dataframe or JSON here
    }


# --- Node 2: The Visualizer Logic ---
def run_visualizer_node(state: AgentState):
    print("--- DEBUG: Visualizer Node starting ---")
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    data_to_plot = state["data_summary"]

    style_prompt = f"""
    Write Python code using Seaborn to create a bar chart for: {data_to_plot}
    - Use a color palette based on '#003366' and '#FFCC00' but generate enough shades for all data points.
    - Save as 'output_chart.png'.
    - DO NOT use plt.show().
    - Provide ONLY the code block starting with ```python.
    """

    response = llm.invoke(style_prompt)

    # Extract code from markdown blocks
    code_match = re.search(r"```python\s*(.*?)\s*```", response.content, re.DOTALL)
    clean_code = code_match.group(1) if code_match else response.content.strip()

    from langchain_experimental.utilities import PythonREPL
    repl = PythonREPL()
    repl.run(clean_code)

    if os.path.exists("output_chart.png"):
        print("--- DEBUG: output_chart.png successfully created! ---")
        return {"has_visual": True}
    else:
        print("--- DEBUG: Visualizer failed to create file. ---")
        return {"has_visual": False}

# --- Conditional Logic ---
def should_visualize(state: AgentState):
    # Search through ALL messages in the history for plotting keywords
    full_history = " ".join([m.content.lower() for m in state["messages"]])
    keywords = ["plot", "graph", "chart", "visualize"]

    if any(word in full_history for word in keywords):
        print("--- DEBUG: Intent 'plot' found in history. Moving to Visualizer ---")
        return "yes"

    print("--- DEBUG: No plotting intent found. Ending workflow. ---")
    return "no"


# --- Define the Graph ---
workflow = StateGraph(AgentState)
workflow.add_node("analyst", run_analyst_node)
workflow.add_node("visualizer", run_visualizer_node)

workflow.set_entry_point("analyst")
workflow.add_conditional_edges("analyst", should_visualize, {"yes": "visualizer", "no": END})
workflow.add_edge("visualizer", END)

app = workflow.compile()


# --- The function the Streamlit UI calls ---
def run_agent_workflow(user_id, db_key, query):
    initial_state = {
        "user_id": user_id,
        "database_key": db_key,
        "messages": [HumanMessage(content=query)],
        "data_summary": "",
        "has_visual": False
    }
    return app.invoke(initial_state)