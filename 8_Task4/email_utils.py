import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configs import SMTP_EMAIL, SMTP_PASSWORD

def send_email(to_email: str, subject: str, body: str) -> str:
    msg = MIMEMultipart()
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)

    return "Email sent"
