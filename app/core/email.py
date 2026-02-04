from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
import os
from dotenv import load_dotenv

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS") == "True",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_ticket_notification(ticket_id: int, subject: str, creator_email: EmailStr):
    """ moderator1 = os.getenv("MODERATOR_1_EMAIL")
    moderator2 = os.getenv("MODERATOR_2_EMAIL")
    
    recipients = [creator_email]
    if moderator1:
        recipients.append(moderator1)
    if moderator2:
        recipients.append(moderator2) """

    recipients = [creator_email]
    recipients.append(os.getenv("MODERATOR_1_EMAIL"))

    html = f"""
    <p>New Ticket Created (ID: {ticket_id})</p>
    <p>Subject: {subject}</p>
    <p>Creator: {creator_email}</p>
    """

    message = MessageSchema(
        subject=f"Ticket Notification: {subject}",
        recipients=recipients,
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
