from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

llm = Groq(id="llama-3.1-8b-instant")

planner = Agent(
    name="Planner",
    role="Break down the user's question into steps",
    tools=[DuckDuckGoTools()],
    # markdown=True,
    model=llm)

researcher = Agent(
    name="Researcher",
    role="Find accurate factual information",
    tools=[DuckDuckGoTools()],
    # markdown=True,
    model=llm)

coder = Agent(
    name="Coder",
    role="Provide technical or logical explanations if needed",
    tools=[DuckDuckGoTools()],
    # markdown=True,
    model=llm)

reviewer = Agent(
    name="Reviewer",
    role="Check correctness and improve clarity",
    tools=[DuckDuckGoTools()],
    # markdown=True,
    model=llm)


chat_manager = Agent(
    name="ChatManager",
    role="Combine all inputs and reply to the user clearly",
    tools=[DuckDuckGoTools()],
    # markdown=True,
    model=llm)

def run_chat():
    print("Multi-Agent Chat")
    print("Type 'exit' to quit")

    while True:
        user_input = input("Me: ")
        if user_input.lower() == "exit":
            break

        plan = planner.run(user_input).content
        research = researcher.run(plan).content
        code_help = coder.run(research).content
        review = reviewer.run(code_help).content

        final_answer = chat_manager.run(
            f"""User question: {user_input}
            Planner output: {plan}
            Researcher output: {research}
            Coder output: {code_help}
            Reviewer output: {review}
            Give a final clear answer to the user.
            """)

        print("\nAgent:", final_answer)

if __name__ == "__main__":
    run_chat()
