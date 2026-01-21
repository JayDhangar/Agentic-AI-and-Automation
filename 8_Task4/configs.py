import os
from dotenv import load_dotenv

load_dotenv()

JOB_REQUIREMENTS = [
    "Python",
    "Flask",
    "LangChain",
    "Docker",
    "REST APIs"
]

SMTP_EMAIL = os.getenv("EMAIL_USER")
SMTP_PASSWORD = os.getenv("EMAIL_PASS")

GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
