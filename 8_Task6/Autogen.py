from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")

model_client=OpenAIChatCompletionClient(model="gpt-4o",api_key=api_key)

assistant=AssistantAgent(name="Jay",model_client=model_client,description="A basic Agent")


async def main():
    result = await assistant.run(task="What is the name of Prime Minister of India")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
