from dataclass import dataclass
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.runtime import Runtime

class GraphState(TypedDict):
    input: str
    result: str


@dataclass
class GraphContext:
    user_agent: str
    docs_url: str = "https://docs.langchain.com"
    db_connection: str = "mysql://<user>:<password>@localhost:3306/langchaindb"



def context_access_node(state: GraphState, runtime: Runtime[GraphContext]):
    db_string = runtime.context.db_connection
    docs_url = runtime.context.docs_url
    user_agent = runtime.context.user_agent

    return {
        "result": f"Context accessed DB: {db_string.split("//")[0]}"
    }


builder = StateGraph(GraphState, context_schema=GraphContext)
builder.add_node(context_access_node)
builder.add_edge(START, "context_access_node")
builder.add_edge("context_access_node", END)

graph = builder.compile()

initial_state={
    "input": "Start Process"
}

final_state=graph.invoke(input=initial_state, context={"user_agent": "Default-Platform"})