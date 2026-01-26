from crewai import Agent,Task,Crew
from crewai.llm import LLM
from dotenv import load_dotenv
load_dotenv()

llm = LLM(model="groq/llama-3.1-8b-instant",temperature=0)

researcher = Agent(
    role="AI Researcher",
    goal="Find the latest trends in Artificial Intelligence",
    backstory="You are an expert AI researcher who follows industry papers, tools, and startups.",
    llm=llm, 
    verbose=True
)

writer = Agent(
    role="Technical Writer",
    goal="Write a clear and concise summary of AI trends",
    backstory="You are a professional writer skilled at simplifying complex AI topics.",
    llm=llm,
    verbose=True
)

Query = "Latest Agentic AI frameworks in 2025"

task1 = Task(
    description=f"Research the following topic in detail:\n{Query}",
    agent=researcher,
    expected_output="A detailed bullet-point list of current AI trends."
)

task2 = Task(
    description="Summarize the research into a short, easy-to-read explanation.",
    agent=writer,
    expected_output="A concise paragraph summarizing the AI trends."
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    verbose=True
)

result=crew.kickoff()
print(result)