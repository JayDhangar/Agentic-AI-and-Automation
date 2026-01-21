from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from langchain_groq import ChatGroq
from docling.document_converter import DocumentConverter
from langchain_core.tools import tool
from langchain.agents import create_agent

load_dotenv()

@tool
def file_converter()->str:

    """
    Docstring for file_converter
    Read the predefined PDF file once and return extracted markdown text.
    :param path: Description
    :type path: str
    :return: Description
    :rtype: str
    """
    
    converter=DocumentConverter()
    result= converter.convert(r"C:\Users\sad\.vscode\MongoDB\Task8\testPDF.pdf")

    data = result.document
    output = data.export_to_markdown()

    return output

@tool
def email(subject:str,body:str,to_email:str)->str:
    """
    Docstring for email
    Send an email with given subject and body.
    :param subject: Description
    :type subject: str
    :param body: Description
    :type body: str
    :param to_email: Description
    :type to_email: str
    :return: Description
    :rtype: str
    """
    sender=os.getenv("EMAIL_USER")
    password=os.getenv("EMAIL_PASS")
    smtp_server=os.getenv("SMTP_SERVER")
    smtp_port=os.getenv("SMTP_PORT")
    
    msg=MIMEText(body)
    msg["Subject"]=subject
    msg["From"]=sender
    msg["To"]=to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg) 

    return "Email Sent"

llm= ChatGroq(model="llama-3.1-8b-instant",temperature=0,max_retries=0)

agent=create_agent(llm,tools=[file_converter,email])

response=agent.invoke({"messages":[("user", "Use file_converter to read the PDF. "
            "Summarize the document in 5–6 bullet points. "
            "Then use email with:\n"
            "- subject: 'Summary of testPDF.pdf'\n"
            "- body: the summary you created\n"
            "- to_email: example@gmail.com\n"
            "After sending the email, stop.")]})


print(response["messages"][-1].content)

