# desigining Job Application Screening


# INVOKE
#   │
#   ▼
# fan_out(GraphState)
#   │
#   ├── Send("screen_applicant", {name: "Gaurav",  skills:[...], experience: 4})
#   ├── Send("screen_applicant", {name: "Priya",   skills:[...], experience: 2})
#   ├── Send("screen_applicant", {name: "Rahul",   skills:[...], experience: 5})
#   └── Send("screen_applicant", {name: "Sneha",   skills:[...], experience: 6})
#             │                        │                  │               │
#             ▼                        ▼                  ▼               ▼
#        score=100 ✅            score=30 ❌         score=100 ✅    score=0 ❌
#        pass                    fail               pass             fail
#             │                        │                  │               │
#             └────────────────────────┴──────────────────┘───────────────┘
#                                      │
#                         operator.add merges all evaluations
#                         into GraphState["evaluations"]
#                                      │
#                                      ▼
#                           shortlist_candidates(GraphState)
#                           filters pass → ["Gaurav", "Rahul"]



from langgraph.types import Send
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
import operator


# Graph state
class GraphState(TypedDict):
    applicants: list[dict]
    evaluations: list[str]
    shortlist: list[str]

# nodes state
class ApplicantState(TypedDict):
    skills: list[str]
    experience: int
    name: str


def screen_applicant(state: ApplicantState):
    name=state.get('name')
    skills=state.get('skills')
    experience=state.get('experience')

    score=0
    if 'django' in skills: score+=20
    if 'pyhton' in skills: score+=10
    if 'postgres' in skills: score+=30
    if 'langgraph' in skills: score+=40
    if experience>4: score+=50

    return {
        "evaluation":[{"name": name, "score": score, "verdict": "PASS" if score>100 else "FAIL"}]
    }


def shortlist_applicants(state: GraphState):
    passed=[
        x['name'] for x in state['evaluations'] if x['verdict']=='PASS'
    ]
    return {"shortlist": passed}


def fan_out(state: GraphState):
    return [
        Send("screen_applicant",{
            "name": applicant['name'],
            "skills": applicant['skills'],
            "experience": applicant['experience']
        }) for applicant in state['applicants']
    ]


graph = StateGraph(GraphState)
graph.add_node("shortlist_applicants", shortlist_applicants)
graph.add_node("screen_applicant", screen_applicant)

graph.add_conditional_edges(START, fan_out)
graph.add_edge("screen_applicant", "shortlist_candidates")
graph.add_edge("shortlist_candidates", END)

agent = graph.compile()
final_state = agent.invoke(
    input={
        "applicants": [
            {
                "name": "Gaurav Sharma", 
                "skills": ["django", "postgres", "langgraph", "pyhton"], 
                "experience": 4
            }
        ]
    }
)