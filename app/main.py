from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core import database
from app.models.ticket import Base
from app.routers import tickets
import sys
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    async with database.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown

app = FastAPI(lifespan=lifespan)

app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])

@app.get("/")
def read_root():
    return {"message": "Support Ticket API is running"}
