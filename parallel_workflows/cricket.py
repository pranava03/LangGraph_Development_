# Non llm based workflow...
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class batsmanState(TypedDict):
    runs                : int
    balls               : int
    fours               : int
    sixes               : int
    sr                  : float
    bpb                 : float
    boundary_percentage : float
    summary             : str

def calculate_sr(state: batsmanState) -> batsmanState:
    sr         = (state['runs'] / state['balls']) * 100
    return {'sr' : sr}

def calculate_bpb(state: batsmanState) -> batsmanState:
    bpb          = (state['balls'] / (state['fours'] + state['sixes']))
    return {'bpb' : bpb}

def calculate_boundary_percentage(state: batsmanState) -> batsmanState:
    boundary_percentage          = ((state['fours'] * 4) + (state['sixes'] * 6) / state['runs']) * 100
    return {'boundary_percentage' : boundary_percentage}

def summary(state: batsmanState) -> batsmanState:
    summary = f"""
    Strike Rate - {state['sr']} \n
    Balls Per Boundary - {state['bpb']} \n
    Boundary Percentage - {state['boundary_percentage']} \n
    """
    return {'summary' : summary}

graph = StateGraph(batsmanState)

graph.add_node('calculate_sr', calculate_sr)
graph.add_node('calculate_bpb', calculate_bpb)
graph.add_node('calculate_boundary_percentage', calculate_boundary_percentage)
graph.add_node('summary', summary)

graph.add_edge(START, 'calculate_sr')
graph.add_edge(START, 'calculate_bpb')
graph.add_edge(START, 'calculate_boundary_percentage')
graph.add_edge('calculate_sr', 'summary')
graph.add_edge('calculate_bpb', 'summary')
graph.add_edge('calculate_boundary_percentage', 'summary')
graph.add_edge('summary', END)

workflow = graph.compile()

initial_state = {'runs' : 100, 'balls' : 50, 'fours' : 6, 'sixes' : 4}
final_state   = workflow.invoke(initial_state)
print(final_state)