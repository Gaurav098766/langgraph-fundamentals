from langgragh.graph import StateGraph, START, END
from typing import TypedDict, Annotated,List


# without reducers

class WithoutReducers(TypedDict):
    count: int
    animals: List[str]

def node_to_update(state: WithoutReducers) -> dict:
    return {
        "count": 1,
        "animals": ["cat"]
    }

initial_state = {
    "count": 0,
    "animals": ["Lion","Buffalo"]
}

def run_example(name:str, state_schema: type, node_func: callable, initial_state: dict):

    print("running example: ", name)

    graph = StateGraph(state_schema)
    graph.add_node("update_node",node_func)
    graph.add_edge(START, "update_node")
    graph.add_edge("update_node", END)

    agent = graph.compile()

    final_state = agent.invoke(initial_state)

    print("initial state: ", initial_state)
    print("final state: ", final_state)
    print("-*" * 40)


run_example(name="without reducers",state_schema=WithoutReducers, node_func=node_to_update, initial_state=initial_state)


# with reducers
def update_count(current, update):
    return current + update

def update_animals(current, update):
    return current + update

class StateWithReducers(TypedDict):
    count: Annotated[int, update_count]
    animals: Annotated[List[str], update_animals]


run_example(name="with reducers",state_schema=StateWithReducers, node_func=node_to_update, initial_state=initial_state)