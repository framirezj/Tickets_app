from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.ticket import TicketStatus

class TicketBase(BaseModel):
    subject: str
    description: str
    creator_email: EmailStr

class TicketCreate(TicketBase):
    model_config = {
        "json_schema_extra": {
            "example": {
                "subject": "Printer Malfunction",
                "description": "The printer on the 2nd floor is smoking.",
                "creator_email": "employee@company.com"
            }
        }
    }

class TicketResponse(TicketBase):
    id: int
    status: TicketStatus
    created_at: datetime

    class Config:
        from_attributes = True
