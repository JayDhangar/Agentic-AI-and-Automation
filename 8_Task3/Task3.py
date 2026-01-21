from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from langchain_groq import ChatGroq
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from langchain_core.tools import tool
from langchain.agents import create_agent
from typing import Annotated
import os.path
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def data():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
    
        with open("token.json", "w") as token: #for saving cred for future use
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)

service = data()
@tool
def create_event(summary:Annotated[str,"Event title"],
                 start_datetime:Annotated[str,"RFC3339 datetime with timezone"])->str:
    """Creates a Calander event."""

    event = {'summary':summary,
            'start': {
                'dateTime': start_datetime,
                'timeZone': 'Asia/Kolkata'
            },
            'end': {
                'dateTime': start_datetime,  
                'timeZone': 'Asia/Kolkata'}
            }
    
    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        return "Event created: %s" % (event.get('htmlLink'))
    
    except HttpError as error:
        return "Error"


llm= ChatGroq(model="llama-3.1-8b-instant",temperature=0,max_retries=0)

System_Prompt=f"""

You are a calendar assistant.

Rules:
- Always create Google Calendar events using RFC3339 format.
- Timezone must be Asia/Kolkata (+05:30).
- If the user does NOT specify a year, use the CURRENT year ({datetime.now().year}).
- If the user says "today" or "tomorrow", resolve the correct date.
- Always call the create_event tool.
"""
agent=create_agent(llm,tools=[create_event],system_prompt=System_Prompt)

def agent_response(user_message:str)->str:
    response=agent.invoke({"messages":[( "user",user_message)]})
    for msg in reversed(response["messages"]):
        if msg.type == "tool":
            return msg.content
    
    return response["messages"][-1].content




