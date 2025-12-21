# Autonomous AI Agents for Data Analysis and Visualization

An intelligent, multi-agent system built with **LangGraph** that provides secure, natural language access to corporate databases.

## Features
- **User Controllability:** Full agent control through an intuitive Streamlit UI, enabling natural language data exploration.
- **User Restriction:** Granular access control logic that maps specific users to authorized databases, preventing unauthorized data leaks.
- **Easy Integration:** A simplified registry system allowing for the rapid addition of new SQLite databases without modifying core agent logic.
- **Automated Testing:** A comprehensive evaluation suite with 3+ automated test cases demonstrating security, SQL accuracy, and visualization correctness.
- **Multi-Agent Workflow:** Stateful orchestration using LangGraph to manage the handoff between specialized Analyst and Visualizer agents.
- **Company Styling:** Automated chart generation using company's official colors.

## Installation
1. Clone the repo: `git clone https://https://github.com/marwin771/autonomous-agents.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. Install dependencies: `pip install -r requirements.txt`

## Configuration
1. Create a `.env` file in the root and add your OpenAI key:
`OPENAI_API_KEY=your_key_here`
2. Place your SQLite files in the `/data` folder. The system expects the following names:
- `sakila.db`
- `chinook.db`
- `northwind_small.sqlite`

## Usage
To launch the interactive dashboard, run: `streamlit run ui/app.py`

## Testing
Run the evaluation suite:
`python -m pytest tests/test_system.py -v`
