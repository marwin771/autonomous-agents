from langchain_experimental.utilities import PythonREPL
from langchain_core.prompts import ChatPromptTemplate

# Requirement: Company Style
COMPANY_STYLE_PROMPT = """
You are the Data Visualization Agent for 'AI Corp'. 
You MUST follow these branding guidelines:
- Use 'Seaborn' for all plots.
- Colors: Use #003366 (Deep Blue) for primary bars/lines and #FFCC00 (Gold) for accents.
- All plots must have a title in 'Arial' and gridlines must be enabled.
- Save the final plot as 'output_chart.png'.

You will be given data in a CSV-like format. Convert it to a DataFrame and plot it.
"""

def visualizer_node(state: AgentState):
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    # logic to take state["data_summary"] and generate plot...
    # (Implementation details below)