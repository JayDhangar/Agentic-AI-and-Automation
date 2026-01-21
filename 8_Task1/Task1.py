from dotenv import load_dotenv

load_dotenv()
# from crewai import Task,Agent,Crew
# from crewai_tools import SerperDevTool
from langchain_groq import ChatGroq
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import create_agent
# from langchain_core.tools import tool

Wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=2000))

llm = ChatGroq(model="llama-3.1-8b-instant",temperature=0)

agent = create_agent(llm, [Wikipedia])

response = agent.invoke({"messages": [("user", "Who is Jonny Depp")]})

print(response["messages"][-1].content)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# search = SerperDevTool()

# researcher =Agent(llm = "groq/llama-3.1-8b-instant"
# ,
#                   role="Actor Information Retrieval Agent",
#                   goal="Identify and provide accurate information about a given actor by extracting verified data from Wikipedia using an LLM.",
#                   backstory="Trained as a digital research assistant with expertise in searching and validating biographical information from trusted knowledge sources like Wikipedia, ensuring accurate and concise actor profiles.",
#                   allow_delegation=False,
#                   tools=[search],
#                   verbose=1)

# Task1=Task(
#     description="Search Wikipedia to identify the given actor and extract verified, information about their background, major achievements, and famous works.",
#     expected_output="A structured summary containing exactly 5 bullet points with Actor's background,one major career achievements,One award or recognition and one contribution or impact in the film industry",
#     output_file="output.txt",
#     agent=researcher
# )

# crew =Crew(agents=[researcher],tasks=[Task1],verbose=True)
# result = crew.kickoff(inputs={"question": "Who is Akshay Kumar?"})

# print(result)
#-------------------------------------------------------------------------------------------------------------------------------------------

