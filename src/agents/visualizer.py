# src/agents/visualizer.py
import re
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.utilities import PythonREPL
from src.agents.state import AgentState
from langchain_core.messages import AIMessage

COMPANY_STYLE_PROMPT = """
You are the Data Visualization Agent. 
You MUST follow these branding guidelines:
- Use 'Seaborn' for all plots.
- Colors: Create a color palette using shades between #003366 (Deep Blue) and #FFCC00 (Gold) so that every data point has a unique but brand-consistent color.
- All plots must have a title in 'Arial' and gridlines enabled.
- Save the final plot as 'output_chart.png'.
- DO NOT use plt.show().

Provide ONLY the code block starting with ```python.
"""


def visualizer_node(state: AgentState):
    """
    Node function to generate charts from data.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # 1. Prepare the prompt with the data found by the Analyst + system rules (company style)
    prompt = ChatPromptTemplate.from_messages([
        ("system", COMPANY_STYLE_PROMPT),
        ("human", f"Create a chart for this data: {state['data_summary']}")
    ])

    # 2. Get the Python code from the LLM
    chain = prompt | llm # simple pipeline where the prompt is fed directly into the AI
    # the AI generates the response, which usually looks like
    # "Sure, here is your code: ```python ... ```".
    response = chain.invoke({})

    # 3. Clean and Execute the code
    code_match = re.search(r"```python\s*(.*?)\s*```", response.content, re.DOTALL) # strip away everything except the code
    clean_code = code_match.group(1) if code_match else response.content.strip()

    repl = PythonREPL() # initializes the code execution tool
    repl.run(clean_code) # executes the Python code (creates the chart)

    # 4. Check results and update state
    success = os.path.exists("output_chart.png")

    # updates the graph's memory
    # if success is True, the UI will know it's time to show the image to the user
    return {"has_visual": success}