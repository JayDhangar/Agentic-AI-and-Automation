import os, base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from configs import GMAIL_SCOPES

def get_mail():
    creds = None

    if os.path.exists("gmail_token.json"):
        creds = Credentials.from_authorized_user_file("gmail_token.json", GMAIL_SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", GMAIL_SCOPES)
            creds = flow.run_local_server(port=0)

        with open("gmail_token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def download_resumes(service, max_emails=10):
    results = service.users().messages().list(userId="me", maxResults=max_emails).execute()
    files = []

    for msg in results.get("messages", []):
        message = service.users().messages().get(userId="me", id=msg["id"]).execute()
        for part in message["payload"].get("parts", []):
            filename = part.get("filename", "")
            if filename.lower().endswith(".pdf"):
                att_id = part["body"].get("attachmentId")
                data = service.users().messages().attachments().get(
                    userId="me", messageId=msg["id"], id=att_id
                ).execute()["data"]

                os.makedirs("downloads", exist_ok=True)
                path = f"downloads/{filename}"
                with open(path, "wb") as f:
                    f.write(base64.urlsafe_b64decode(data))

                files.append(path)

    return files
