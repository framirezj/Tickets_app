from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import ticket as crud_ticket
from app.schemas import ticket as schemas_ticket
from app.core import database, email

router = APIRouter()

@router.post("/", response_model=schemas_ticket.TicketResponse)
async def create_ticket(
    ticket: schemas_ticket.TicketCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        db_ticket = await crud_ticket.create_ticket(db=db, ticket=ticket)
        
        # Send email in background
        background_tasks.add_task(
            email.send_ticket_notification,
            db_ticket.id,
            db_ticket.subject,
            db_ticket.creator_email
        )
        
        return db_ticket
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[schemas_ticket.TicketResponse])
async def read_tickets(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)):
    tickets = await crud_ticket.get_tickets(db, skip=skip, limit=limit)
    return tickets
