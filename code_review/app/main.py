from fastapi import FastAPI, HTTPException
from app.models import GraphDefinition, RunRequest, RunResponse
from app.engine import create_graph, run_graph, runs_db
from app.tools.code_review import register_code_review_tools

# Initialize App and Registry
app = FastAPI(title="Minimal Workflow Engine")
register_code_review_tools()

@app.post("/graph/create")
def api_create_graph(config: GraphDefinition):
    """
    Create a new workflow definition.
    """
    try:
        graph_id = create_graph(config)
        return {"graph_id": graph_id, "message": "Graph created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/graph/run")
def api_run_graph(request: RunRequest):
    """
    Run an existing workflow with initial state.
    """
    try:
        run_id = run_graph(request.graph_id, request.initial_state)
        # Retrieve immediate result since our engine is synchronous for this demo
        run_data = runs_db[run_id]
        return {
            "run_id": run_id, 
            "status": run_data["status"],
            "final_state": run_data.get("final_state"),
            "logs": run_data.get("logs")
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Graph not found")

@app.get("/graph/state/{run_id}")
def api_get_state(run_id: str):
    """
    Get the state of a specific run.
    """
    if run_id not in runs_db:
        raise HTTPException(status_code=404, detail="Run ID not found")
    return runs_db[run_id]

@app.get("/")
def health_check():
    return {"status": "online", "engine": "LangGraph"}