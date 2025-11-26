from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import init_db
from app.routers import operators, sources, contacts, leads

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Mini CRM - simplified", lifespan=lifespan)

app.include_router(operators.router)
app.include_router(sources.router)
app.include_router(contacts.router)
app.include_router(leads.router)
