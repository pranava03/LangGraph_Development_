from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, List, Annotated
from pydantic import BaseModel, Field
import operator
import os
from dotenv import load_dotenv
load_dotenv()

model = ChatOpenAI(api_key = os.getenv("OPENAI_API_KEY"), model = 'gpt-4o-mini')

class EvaluationSchema(BaseModel):
    feedback : str = Field(description="Detailed feedback for the essay.")
    score    : int = Field(description="Score for the essay on a scale of 1 to 10.", ge = 0, le = 10)

structured_model = model.with_structured_output(EvaluationSchema)
essay            = ''

class UPSCState(TypedDict):
    essay             : str
    language_feeback  : str
    analysis_feedback : str
    clarity_feedback  : str
    overall_feedback  : str
    individual_scores : Annotated[List[int], operator.add]
    average_score     : float

def evaluate_language(state: UPSCState):
    prompt = f"Evaluate the language quality of the following essay and provide detailed feedback along with a score from 1 to 10:\n\n{state['essay']}"
    output = structured_model.invoke(prompt)
    return {'language_feedback': output.feedback, 'individual_scores': [output.score]}

def evaluate_analysis(state: UPSCState):
    prompt = f"Evaluate the analytical depth of the following essay and provide detailed feedback along with a score from 1 to 10:\n\n{state['essay']}"
    output = structured_model.invoke(prompt)
    return {'analysis_feedback': output.feedback, 'individual_scores': [output.score]}

def evaluate_thought(state: UPSCState):
    prompt = f"Evaluate the clarity of thought in the following essay and provide detailed feedback along with a score from 1 to 10:\n\n{state['essay']}"
    output = structured_model.invoke(prompt)
    return {'clarity_feedback': output.feedback, 'individual_scores': [output.score]}

def final_evaluation(state: UPSCState):
    prompt          = f"based on the following feedback create a summarized feedback \n language feedback -{state['language_feeback']} \n depth analysis feedback - {state['analysis_feedback']} \n clarity of thought feedback - {state['clarity_feedback']}"
    overall_feeback = model.invoke(prompt).content
    average_score   = sum(state['individual_scores']) / len(state['individual_scores'])
    return {'overall_feedback' : overall_feeback, 'average_score': average_score}

graph = StateGraph(UPSCState)

graph.add_node('evaluate_language', evaluate_language)
graph.add_node('evaluate_analysis', evaluate_analysis)
graph.add_node('evaluate_thought', evaluate_thought)
graph.add_node('final_feedback', final_evaluation)

graph.add_edge(START, 'evaluate_language')
graph.add_edge(START, 'evaluate_analysis')
graph.add_edge(START, 'evaluate_thought')
graph.add_edge('evaluate_language', 'final_feedback')
graph.add_edge('evaluate_analysis', 'final_feedback')
graph.add_edge('evaluate_thought', 'final_feedback')
graph.add_edge('final_feedback', END)

workflow = graph.compile()

initial_state = {'essay' : essay}
final_state   = workflow.invoke(initial_state)
print(final_state)