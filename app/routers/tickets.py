from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import ticket as crud_ticket
from app.schemas import ticket as schemas_ticket
from sqlalchemy import delete
from app.models.ticket import Ticket
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
        #funciona pero no activo para no mandar emails
        background_tasks.add_task(
            email.send_ticket_notification_bg,
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



@router.get("/{ticket_id}", response_model=schemas_ticket.TicketResponse)
async def read_ticket(ticket_id: int, db: AsyncSession=Depends(database.get_db)):
    ticket = await crud_ticket.get_ticket_by_id(db, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.put("/{ticket_id}/status", response_model=schemas_ticket.TicketResponse)
async def update_ticket_status(ticket_id: int, status_update: schemas_ticket.TicketUpdateStatus, db: AsyncSession = Depends(database.get_db)):
    ticket = await crud_ticket.update_ticket_status(db, ticket_id, status_update.status)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket












##ENDPOINTS DE PRUEBA DEV##    

@router.post("/generate-test-data", response_model=list[schemas_ticket.TicketResponse])
async def generate_test_tickets(db: AsyncSession = Depends(database.get_db)):
    test_tickets = []
    for i in range(1, 11):
        ticket_data = schemas_ticket.TicketCreate(
            subject=f"Test Ticket {i}",
            description=f"This is a generated test ticket number {i}.",
            creator_email=f"user{i}@example.com"
        )
        new_ticket = await crud_ticket.create_ticket(db=db, ticket=ticket_data)
        # Convert to Pydantic model immediately to avoid "Instance is not bound to a Session" or expiry issues
        # caused by subsequent commits in the loop.
        test_tickets.append(schemas_ticket.TicketResponse.model_validate(new_ticket))
    return test_tickets

@router.delete("/")
async def delete_all_tickets(db: AsyncSession = Depends(database.get_db)):
    await db.execute(delete(Ticket))
    await db.commit()
    return {"message": "All tickets deleted"}