import streamlit as st
import sys
import os
# Adds the project root directory to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import run_agent_workflow # This is our LangGraph entry point
from src.config.permissions import USER_DB_PERMISSIONS
from dotenv import load_dotenv
load_dotenv()
st.set_page_config(page_title="AI Data Agent", layout="wide")

# --- Sidebar: User Authentication Simulator ---
st.sidebar.title("🔐 User Access Control")
user_id = st.sidebar.selectbox("Select User ID", options=list(USER_DB_PERMISSIONS.keys()))

# Dynamically filter databases based on selected user
allowed_dbs = USER_DB_PERMISSIONS.get(user_id, [])
db_key = st.sidebar.selectbox("Select Database", options=allowed_dbs)

st.sidebar.info(f"Logged in as: **{user_id}**\nAccessing: **{db_key}**")

# --- Main Interface ---
st.title("📊 Autonomous Data Analyst & Visualizer")
st.markdown("Ask questions about your data. The agents will handle the SQL and the styling.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ex: 'Show me the top 5 customers by revenue and plot a bar chart'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing data and generating visuals..."):
            # Execute the LangGraph workflow
            result = run_agent_workflow(user_id, db_key, prompt)
            
            # Display Text Result
            st.markdown(result["messages"][-1].content)
            
            # Check for generated chart
            if os.path.exists("output_chart.png"):
                st.image("output_chart.png", caption="Company Style Visualization")
                # Store for history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": result["messages"][-1].content,
                    "image": "output_chart.png"
                })
            else:
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": result["messages"][-1].content
                })