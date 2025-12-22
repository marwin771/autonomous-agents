# tests/test_system.py
import pytest
import os
from dotenv import load_dotenv
from src.tools.sql_tools import get_db_for_user
from src.main import run_agent_workflow

# 1. Load API keys for the test environment
load_dotenv()


# --- TEST 1: Security / User Restriction ---
def test_unauthorized_database_access():
    print("\n[Test 1] Checking User Restriction...")
    # We use a user that EXISTS and a database that EXISTS,
    # but where the user does NOT have permission.
    with pytest.raises(PermissionError):
        # 'marketing_team' only has access to 'chinook'
        # Trying to access 'sakila' should trigger a PermissionError
        get_db_for_user("marketing_team", "sakila")
    print("✅ Success: Unauthorized access was blocked.")


# --- TEST 2: Functional Correctness (Analyst Agent) ---
def test_sql_analysis_accuracy():
    print("\n[Test 2] Checking SQL Accuracy...")
    # Using 'admin_user' who has access to 'chinook'
    query = "How many tracks are in the Chinook database?"

    result = run_agent_workflow("admin_user", "chinook", query)

    assert "messages" in result # checks that the agent actually returned a response
    final_answer = result["messages"][-1].content # grabs the last thing the AI said
    assert len(final_answer) > 0
    # Chinook has thousands of tracks, so the answer should contain digits
    assert any(char.isdigit() for char in final_answer)
    print(f"✅ Success: Agent found tracks: {final_answer}")


# --- TEST 3: Visualization Output ---
def test_visualization_generation():
    print("\n[Test 3] Checking Visualization Generation...")
    if os.path.exists("output_chart.png"):
        os.remove("output_chart.png") # delete any old version

    # We ask for a specific plot from the Sakila database
    query = "Plot the top 5 film categories by number of films."
    run_agent_workflow("admin_user", "sakila", query)

    assert os.path.exists("output_chart.png")
    assert os.path.getsize("output_chart.png") > 0
    print("✅ Success: Branded chart 'output_chart.png' generated.")