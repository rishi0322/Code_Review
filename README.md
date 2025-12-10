# Code_Review
Tredence Project 
# Minimal Workflow Engine: Code Review Agent

A lightweight, graph-based workflow engine built with FastAPI and LangGraph. This implementation features an autonomous Code Review Agent that utilizes Anthropic's Claude 3.5 Sonnet to perform static analysis, complexity scoring, and issue detection on Python code.

## System Architecture

The project is structured as a modular engine where the workflow logic is decoupled from the execution core.

- *Engine Core:* Handles graph compilation, state management, and execution orchestration using LangGraph.
- *API Layer:* A FastAPI interface exposing endpoints to create graphs and execute runs.
- *Tool Registry:* A centralized registry pattern to manage available agent functions (nodes).
- *Agent Logic:* A dedicated module containing the specific prompt engineering and processing steps for code review.

### Workflow Steps
1. *Extraction:* Parses the input code to identify function definitions.
2. *Complexity Analysis:* Calculates cyclomatic complexity and readability scores.
3. *Review & Suggestions:* Detects security vulnerabilities, logic errors, and style issues, providing actionable fixes.

## Prerequisites

- Python 3.9+
- An Anthropic API Key

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd code_review
