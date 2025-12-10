# Code_Review  
Tredence Project

# Minimal Workflow Engine: Code Review Agent

A lightweight, graph-based workflow engine built with **FastAPI** and **LangGraph**.  
This implementation features an autonomous **Code Review Agent** powered by **Anthropic Claude 3.5 Sonnet**, capable of performing static analysis, complexity scoring, and issue detection on Python code.

---

## System Architecture

- **Engine Core:** Manages graph compilation, workflow execution, and state transitions using LangGraph.  
- **API Layer:** FastAPI endpoints for creating workflow graphs and executing workflows.  
- **Tool Registry:** Centralized registry system for managing agent functions (workflow nodes).  
- **Agent Logic:** Contains prompt engineering and code review logic using Claude 3.5 Sonnet.  

---

## Workflow Steps

1. **Extraction:** Parses input Python code and identifies all function definitions.  
2. **Complexity Analysis:** Computes cyclomatic complexity and readability scores.  
3. **Review & Suggestions:** Detects vulnerabilities, logic errors, security risks, and style issues; then provides actionable improvements.  

---

## Prerequisites

- Python **3.9+**  
- An **Anthropic API Key**  

---

# Installation

Run the following commands to install and configure the project:

```bash
git clone <repository-url>
cd <project-directory>

python -m venv venv

# macOS/Linux
source venv/bin/activate
# Windows
# .\venv\Scripts\activate

pip install -r requirements.txt

echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
