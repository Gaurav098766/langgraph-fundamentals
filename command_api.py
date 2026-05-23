from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command


class GraphState(TypedDict):
    temperature: float
    status_message: str
    warning_sent: bool
    final_action_performed: str


def check_node(state: GraphState) -> Command[Literal["warn_user","success"]]:
    temp = state['temperature']

    if temp > 90:
        print("Temperature is too high! Sending warning to user.")
        return Command(
            update={
                "status_message": "Routing to warning handler"
            },
            goto="warn_user"
        )
    else:
        print("Temperature is normal. Proceeding to success handler.")
        return Command(
            update={
                "status_message": "Routing to success handler"
            },
            goto="success"
        )
    

def warn_user(state: GraphState):
    print("Warning user about high temperature.")
    return {
        "warning_sent": True,
        "final_action_performed": "Warning Notification Sent"
    }


def success(state: GraphState):
    print("Temperature is normal. Proceeding to success handler.")
    return {
        "warning_sent": False,
        "final_action_performed": "Success Action Performed"
    }


graph = StateGraph(GraphState)
graph.add_node(check_node)
graph.add_node(warn_user)
graph.add_node(success)
graph.add_edge(START, "check_node")
# no need to add edges from check_node to warn_user and success as they are handled by the goto in the Command


agent = graph.compile()
initial_state = {"temperature": 95.0,}
final_state = agent.invoke(input=initial_state)
print("Final state: ", final_state)
