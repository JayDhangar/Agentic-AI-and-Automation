from typing import TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"),model_name="llama-3.1-8b-instant")

class AgentState(TypedDict):
    question: str
    research: str
    answer: str

def researcher_agent(state: AgentState):
    response = llm.invoke(f"Answer this question factually:\n{state['question']}")
    return {"research": response.content}

def writer_agent(state: AgentState):
    response = llm.invoke(f"Rewrite this in a clear, friendly way:\n{state['research']}")
    return {"answer": response.content}

graph = StateGraph(AgentState)

graph.add_node("researcher", researcher_agent)
graph.add_node("writer", writer_agent)

graph.set_entry_point("researcher")
graph.add_edge("researcher", "writer")
graph.add_edge("writer", END)

app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({"question": "Who is the Prime Minister of India and who is Lalit Modi?"})
    print("Result:", result["answer"])
