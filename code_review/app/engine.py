import uuid
from typing import Dict, Any
from langgraph.graph import StateGraph, START, END
from app.models import GraphDefinition
from app.registry import registry

# In-memory storage for graphs and execution runs
graphs_db: Dict[str, Any] = {}
runs_db: Dict[str, Dict[str, Any]] = {}

def build_graph(config: GraphDefinition):
    """
    Constructs a compiled LangGraph StateGraph from the JSON definition.
    """
    # 1. Initialize StateGraph with a generic dict state
    builder = StateGraph(dict)

    # 2. Add Nodes
    for node in config.nodes:
        # Fetch the actual function from the registry using the name provided in JSON
        func = registry.get_tool(node.function_name)
        builder.add_node(node.id, func)

    # 3. Add Standard Edges
    for edge in config.edges:
        src = START if edge.source == "START" else edge.source
        tgt = END if edge.target == "END" else edge.target
        builder.add_edge(src, tgt)

    # 4. Add Conditional Edges (Branching/Looping)
    if config.conditional_edges:
        for cond in config.conditional_edges:
            condition_func = registry.get_condition(cond.condition_function)
            builder.add_conditional_edges(
                cond.source,
                condition_func,
                cond.mapping
            )

    # 5. Compile the graph
    return builder.compile()

def create_graph(config: GraphDefinition) -> str:
    """
    Builds and stores a graph, returning its unique ID.
    """
    graph_id = str(uuid.uuid4())
    compiled_graph = build_graph(config)
    graphs_db[graph_id] = compiled_graph
    return graph_id

def run_graph(graph_id: str, initial_state: Dict[str, Any]) -> str:
    """
    Executes a stored graph with the given initial state.
    """
    if graph_id not in graphs_db:
        raise ValueError("Graph not found")
    
    compiled_graph = graphs_db[graph_id]
    run_id = str(uuid.uuid4())
    
    try:
        # LangGraph invoke executes the workflow and returns the final state
        result = compiled_graph.invoke(initial_state)
        
        runs_db[run_id] = {
            "status": "completed",
            "final_state": result,
            "logs": ["Execution successful"]
        }
    except Exception as e:
        runs_db[run_id] = {
            "status": "failed",
            "error": str(e),
            "logs": [f"Error: {str(e)}"]
        }
        
    return run_id