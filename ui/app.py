# ui/app.py
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
st.sidebar.title("User Access Control")
user_id = st.sidebar.selectbox("Select User ID", options=list(USER_DB_PERMISSIONS.keys()))

# Dynamically filter databases based on selected user
allowed_dbs = USER_DB_PERMISSIONS.get(user_id, [])
db_key = st.sidebar.selectbox("Select Database", options=allowed_dbs)

st.sidebar.info(f"Logged in as: **{user_id}**\nAccessing: **{db_key}**")

# --- Main Interface ---
st.title("Autonomous Data Analyst & Visualizer")
st.markdown("Ask questions about your data. The agents will handle the SQL and the styling.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ex: 'Find the top 5 genres by revenue, then plot them in a bar chart.'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing data and generating visuals..."):
            # 1. Execute the LangGraph workflow
            result = run_agent_workflow(user_id, db_key, prompt)
            ans_text = result["messages"][-1].content

            # 2. Display Text Result
            st.markdown(ans_text)

            # 3. Handle the image safely
            if result.get("has_visual") and os.path.exists("output_chart.png"):
                # Display the image to the user
                st.image("output_chart.png", caption="Company Style Visualization")

                # Update history with the text and the IMAGE DATA (not just the path)
                # Opening as bytes ensures the image stays in history even after deletion
                with open("output_chart.png", "rb") as f:
                    img_bytes = f.read()

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ans_text,
                    "image": img_bytes
                })

                # CLEANUP: Delete the file so it doesn't show up in the next turn
                os.remove("output_chart.png")
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ans_text
                })