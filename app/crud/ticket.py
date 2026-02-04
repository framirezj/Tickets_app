from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate

async def create_ticket(db: AsyncSession, ticket: TicketCreate):
    db_ticket = Ticket(
        subject=ticket.subject,
        description=ticket.description,
        creator_email=ticket.creator_email
    )
    db.add(db_ticket)
    await db.commit()
    await db.refresh(db_ticket)
    return db_ticket

async def get_tickets(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Ticket).offset(skip).limit(limit))
    return result.scalars().all()


async def get_ticket_by_id(db: AsyncSession, ticket_id: int):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    return result.scalar_one_or_none()

async def update_ticket_status(db: AsyncSession, ticket_id: int, status):
    ticket = await get_ticket_by_id(db, ticket_id)
    if ticket:
        ticket.status = status
        await db.commit()
        await db.refresh(ticket)
    return ticket
