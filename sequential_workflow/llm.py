from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv
load_dotenv()

model = ChatOpenAI()

class LLMState(TypedDict):
    question : str
    answer   : str

def llm_qa(state: LLMState) -> LLMState:
    pass
    # Extract the question from the state
    question = state['question']
    # form a prompt
    prompt = f"Answer the following question: {question}"
    # ask that question to the LLM
    answer = model.invoke(prompt).content
    # update the answer in the state
    state['answer'] = answer
    return state

graph = StateGraph(LLMState)

graph.add_node('llm_qa', llm_qa)

graph.add_edge(START, 'llm_qa')
graph.add_edge('llm_qa', END)

workflow = graph.compile()

initial_state = {'question': 'How far is the moon from the earth?'}
final_state   = workflow.invoke(initial_state)
print(final_state)