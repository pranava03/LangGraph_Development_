# Non llm based workflow...
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal

class QuadState(TypedDict):
    a            : int
    b            : int
    c            : int
    equation     : str
    discriminant : float
    result       : str

def show_equation(state: QuadState):
    equation = f"{state['a']}x² + {state['b']}x + {state['c']}"
    return {'equation': equation}

def calculate_discriminant(state: QuadState):
    discriminant = state['b'] ** 2 - (4 * state['a'] * state['c'])
    return {'discriminant': discriminant}

def real_roots(state: QuadState):
    root1 = (-state['b'] + state['discriminant'] ** 0.5) / (2 * state['a'])
    root2 = (-state['b'] - state['discriminant'] ** 0.5) / (2 * state['a'])
    return {'result' : f"Real roots: {root1} and {root2}"}

def complex_roots(state: QuadState):
    real_part      = -state['b'] / (2 * state['a'])
    imaginary_part = (-state['discriminant'] ** 0.5) / (2 * state['a'])
    return {'result' : f"Complex roots: {real_part} + {imaginary_part}i and {real_part} - {imaginary_part}i"}

def repeated_roots(state: QuadState):
    root = -state['b'] / (2 * state['a'])
    return {'result' : f"Repeated root: {root}"}

def check_condition(state: QuadState) -> Literal["real_roots", "complex_roots", "repeated_roots"]:
    if state['discriminant'] > 0:
        return 'real_roots'
    elif state['discriminant'] < 0:
        return 'complex_roots'
    else:
        return 'repeated_roots'

graph = StateGraph(QuadState)

graph.add_node('show_equation', show_equation)
graph.add_node('calculate_discriminant', calculate_discriminant)
graph.add_node('real_roots', real_roots)
graph.add_node('complex_roots', complex_roots)
graph.add_node('repeated_roots', repeated_roots)

graph.add_edge(START, 'show_equation')
graph.add_edge('show_equation', 'calculate_discriminant')
graph.add_conditional_edges('calculate_discriminant', check_condition)
graph.add_edge('real_roots', END)
graph.add_edge('complex_roots', END)
graph.add_edge('repeated_roots', END)

workflow = graph.compile()

initial_state = {'a': 4, 'b': -5, 'c': -4}
final_state   = workflow.invoke(initial_state)
print(final_state)