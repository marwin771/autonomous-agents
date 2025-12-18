# Autonomous AI Agents for Data Analysis and Visualization

An intelligent, multi-agent system built with **LangGraph** that provides secure, natural language access to corporate databases.

## Features
- **Multi-Agent Workflow:** Orchestrates a 'Data Analyst' and a 'Brand Visualizer'.
- **Security-First:** Middleware permission layer restricts users to specific databases.
- **Corporate Branding:** Automated chart generation using corporate HEX palettes.
- **SQL Expert:** Handles complex joins and circular dependencies (e.g., Sakila schema).

## Installation
1. Clone the repo: `git clone https://https://github.com/marwin771/autonomous-agents.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. Install dependencies: `pip install -r requirements.txt`

## Configuration
Create a `.env` file in the root and add your OpenAI key:
`OPENAI_API_KEY=your_key_here`

## Testing
Run the evaluation suite:
`python -m pytest tests/test_system.py -v`
