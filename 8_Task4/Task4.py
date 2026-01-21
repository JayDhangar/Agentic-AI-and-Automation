from langgraph.graph import StateGraph, END
from Schemas import HRState, ResumeSchema, SkillMatch
from LLM import resume_chain, skill_chain, resume_parser, skill_parser
from gmail import get_mail, download_resumes
from converter import read_resume
from email_utils import send_email
from configs import JOB_REQUIREMENTS
from dotenv import load_dotenv

load_dotenv()

def intake_node(state: HRState):
    service = get_mail()
    files = download_resumes(service)
    return {"resume_files": files}

def reader_node(state: HRState):
    text = read_resume(state["resume_files"][0])
    return {"resume_text": text}

def parser_node(state: HRState):
    parsed = resume_chain.invoke({
        "resume_text": state["resume_text"],
        "format_instructions": resume_parser.get_format_instructions()
    })
    return {"parsed_resume": parsed.model_dump()}

def matcher_node(state: HRState):
    match = skill_chain.invoke({
        "resume": state["parsed_resume"],
        "job_requirements": JOB_REQUIREMENTS,
        "format_instructions": skill_parser.get_format_instructions()
    })
    return {"skill_match": match.model_dump()}

def email_node(state: HRState):
    resume = ResumeSchema(**state["parsed_resume"])
    match = SkillMatch(**state["skill_match"])

    subject = "Interview Invitation" if match.shortlisted else "Application Update"
    body = match.reason
    status = send_email(resume.email, subject, body)

    return {"email_status": status}

graph = StateGraph(HRState)
graph.add_node("intake", intake_node)
graph.add_node("reader", reader_node)
graph.add_node("parser", parser_node)
graph.add_node("matcher", matcher_node)
graph.add_node("email", email_node)

graph.set_entry_point("intake")
graph.add_edge("intake", "reader")
graph.add_edge("reader", "parser")
graph.add_edge("parser", "matcher")
graph.add_edge("matcher", "email")
graph.add_edge("email", END)

app = graph.compile()

if __name__ == "__main__":
    print(app.invoke({}))
