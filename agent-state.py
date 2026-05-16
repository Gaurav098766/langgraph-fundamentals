from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from pydantic import BaseModel, Field



def node_a(state):
    """A simple node that updates the state."""
    print("Executing Node A...")
    return {
        "messages": ["Step A Completed"],
        "step_count": 1
    }


def node_b(state):
    """A simple node that updates the state."""
    print("Executing Node B...")

    # Access and print some state information for demonstration
    if isinstance(state, dict):
        step_count = state["step_count"]
    else:
        step_count = state.step_count

    print(f"Current step count from state: {step_count}")

    return {
        "messages": ["Step B Completed"],
        "step_count": 1
    }


def build_and_run_graph(state_schema, initial_state):
    print(f"\n--- Building and Running graph with state schema: {state_schema.__name__ if hasattr(state_schema, '__name__') else 'Dictionary'}")

    # Initiate the graph
    graph = StateGraph(state_schema)

    # Add Nodes
    graph.add_node("node_a", node_a)
    graph.add_node("node_b", node_b)

    # Add Edges
    graph.add_edge(START, "node_a")
    graph.add_edge("node_a", "node_b")
    graph.add_edge("node_b", END)

    # Compile and run
    agent = graph.compile()
    final_state = agent.invoke(initial_state)

    print("\nFinal State:")
    print(final_state)
    print("-*" * 40)


# Testing with a simple dictionary state
def create_dict_state():
    return {
        "messages": [],
        "step_count": 0,
        "private_data": None
    }

build_and_run_graph(dict, create_dict_state())


# Testing with a TypedDict state
class TypedDictState(TypedDict):
    messages: list
    step_count: int
    private_data: None

build_and_run_graph(TypedDictState, TypedDictState(messages=[], step_count=0, private_data=None))


# Testing with a Pydantic BaseModel state
class BaseModelState(BaseModel):
    messages: list = Field(default_factory=list)
    step_count: int = Field(default=0)
    private_data: str = Field(default='')

build_and_run_graph(BaseModelState, BaseModelState())