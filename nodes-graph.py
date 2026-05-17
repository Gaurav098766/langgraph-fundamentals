from langgragh.graph import StateGraph, START, END
from typing import TypedDict
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime

class GraphState(TypedDict):
    input: str
    results: str

class ContextSchema(TypedDict):
    user_id: str


def plain_node(state:GraphState) -> GraphState:
    print("Executing plain_node with state: ", state)
    return {
        "results": f"Hello {state['input']}"
    }


def node_with_config(state: GraphState, config:RunnableConfig):
    print("Executing node_with_config with state: ", state)
    thread_id = config.get("configurable", {}).get("thread_id")

    print(f"Thread ID from config: {thread_id}")
    return {
        "results": f"Config Successful accessed"
    }


def node_with_runtime(state: GraphState, runtime: Runtime[ContextSchema]):
    print("Executing node_with_runtime with state: ", state)
    context = runtime.context['user_id']
    print("Context: ", context)
    return {
        "results": f"Runtime context accessed for user {context}"
    }

builder = StateGraph(GraphState, context_schema=ContextSchema)
builder.add_node("plain_node", plain_node)
builder.add_node("node_with_config", node_with_config)
builder.add_node("node_with_runtime", node_with_runtime)

builder.add_edge(START, "plain_node")
builder.add_edge("plain_node", "node_with_config")
builder.add_edge("node_with_config", "node_with_runtime")
builder.add_edge("node_with_runtime", END)

agent = builder.compile()
initial_state = {
    "input": "Gaurav Sharma",
}

run_config = {"configurable": {"thread_id": "thread-123"}}

graph_context = {"user_id": "user-456"}

final_state = agent.invoke(input=initial_state, config=run_config, context=graph_context)
print("Final state: ", final_state)

