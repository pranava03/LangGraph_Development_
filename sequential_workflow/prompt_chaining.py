from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv
import os
load_dotenv()

model = ChatOpenAI(api_key = os.getenv("OPENAI_API_KEY"))

class BlogState(TypedDict):
    title   : str
    outline : str
    content : str

def create_outline(state: BlogState) -> BlogState:
    # Fetch title
    title            = state['title']
    # Call llm generate outline
    prompt           = f"Generate an detailed outline for a blog on the topic: {title}"
    outline          = model.invoke(prompt).content
    # Update state   
    state['outline'] = outline
    return state

def create_blog(state: BlogState) -> BlogState:
    title            = state['title']
    outline          = state['outline']
    prompt           = f"Write a detailed blog on the title - {title} using the following outline \n {outline}"
    content          = model.invoke(prompt).content
    state['content'] = content
    return state

graph = StateGraph(BlogState)

graph.add_node('create_outline', create_outline)
graph.add_node('create_blog', create_blog)

graph.add_edge(START, 'create_outline')
graph.add_edge('create_outline', 'create_blog')
graph.add_edge('create_blog', END)

workflow = graph.compile()

initial_state = {'title': 'Rise of AI in INDIA'}
final_state   = workflow.invoke(initial_state)
print(final_state)