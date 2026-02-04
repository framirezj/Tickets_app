from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

# -------------------------
# Email configuration
# -------------------------
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS") == "True",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=os.path.join(os.path.dirname(__file__), '..', 'templates')
)

# -------------------------
# Async email sender
# -------------------------
async def send_ticket_notification(
    ticket_id: int,
    subject: str,
    creator_email: EmailStr
):
    recipients = [creator_email]

    moderator = os.getenv("MODERATOR_1_EMAIL")
    if moderator:
        recipients.append(moderator)

    # Template data
    template_body = {
        "ticket_id": ticket_id,
        "subject": subject,
        "creator_email": creator_email,
        "description": "Please check the dashboard for details."
    }

    message = MessageSchema(
        subject=f"Notificación de Ticket: {subject}",
        recipients=recipients,
        template_body=template_body,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="ticket_notification.html")

# -------------------------
# Sync wrapper for BackgroundTasks
# -------------------------
def send_ticket_notification_bg(
    ticket_id: int,
    subject: str,
    creator_email: EmailStr
):
    """
    Wrapper síncrono para poder usar send_ticket_notification
    dentro de FastAPI BackgroundTasks
    """
    asyncio.run(
        send_ticket_notification(ticket_id, subject, creator_email)
    )
