from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser
from Schemas import ResumeSchema, SkillMatch
from prompts import resume_prompt, skill_prompt
from dotenv import load_dotenv
load_dotenv()
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

resume_parser = PydanticOutputParser(pydantic_object=ResumeSchema)
skill_parser = PydanticOutputParser(pydantic_object=SkillMatch)

resume_chain = resume_prompt | llm | resume_parser
skill_chain = skill_prompt | llm | skill_parser
