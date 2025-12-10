import os
import time
from typing import Dict, Any, List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from app.registry import registry

# Load environment variables
load_dotenv()

# --- Initialize Claude ---
# "claude-3-5-sonnet-20241022" is excellent for code review.
# Use "claude-3-5-haiku-20241022" for a faster/cheaper option.
llm = ChatAnthropic(
    model="claude-3-haiku-20240307",
    temperature=0
)

# --- Pydantic Models ---

class FunctionList(BaseModel):
    functions: List[str] = Field(description="List of function names found in the code")

class ComplexityAnalysis(BaseModel):
    score: int = Field(description="Complexity score from 1 (simple) to 10 (very complex)")
    reasoning: str = Field(description="Brief explanation of the score")

class CodeIssue(BaseModel):
    severity: str = Field(description="low, medium, or high")
    description: str = Field(description="What the issue is")
    suggestion: str = Field(description="How to fix it")

class CodeReviewResult(BaseModel):
    issues: List[CodeIssue] = Field(description="List of detected issues")

# --- Node Functions ---

def extract_functions(state: Dict[str, Any]) -> Dict[str, Any]:
    """Step 1: Extract function names using Claude."""
    time.sleep(1) # Small buffer for rate limits
    code = state.get("code", "")
    if not code: return state
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a static analysis tool. Extract all function names from the provided Python code."),
        ("user", "{code}")
    ])
    
    # Claude natively supports structured output
    chain = prompt | llm.with_structured_output(FunctionList)
    
    try:
        result = chain.invoke({"code": code})
        # Preserve existing state!
        return {**state, "extracted_functions": result.functions}
    except Exception as e:
        return {**state, "error_extractor": str(e)}

def check_complexity(state: Dict[str, Any]) -> Dict[str, Any]:
    """Step 2: Complexity analysis."""
    time.sleep(1)
    code = state.get("code", "")
    if not code: return state
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Analyze the cyclomatic complexity and readability of this code. Rate it 1-10."),
        ("user", "{code}")
    ])
    
    chain = prompt | llm.with_structured_output(ComplexityAnalysis)
    
    try:
        result = chain.invoke({"code": code})
        return {
            **state, 
            "complexity_score": result.score, 
            "complexity_reasoning": result.reasoning
        }
    except Exception as e:
         return {**state, "error_complexity": str(e)}

def detect_issues_and_suggestions(state: Dict[str, Any]) -> Dict[str, Any]:
    """Step 3: Detect bugs and suggestions."""
    time.sleep(1)
    code = state.get("code", "")
    if not code: return state
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a senior code reviewer. Find bugs, security risks, or style issues. Provide a suggestion for each."),
        ("user", "{code}")
    ])
    
    chain = prompt | llm.with_structured_output(CodeReviewResult)
    
    try:
        result = chain.invoke({"code": code})
        issues_data = [issue.model_dump() for issue in result.issues]
        return {**state, "review_issues": issues_data}
    except Exception as e:
         return {**state, "error_reviewer": str(e)}

# --- Registration ---

def register_code_review_tools():
    registry.register_tool("extract_functions", extract_functions)
    registry.register_tool("check_complexity", check_complexity)
    registry.register_tool("detect_basic_issues", detect_issues_and_suggestions)