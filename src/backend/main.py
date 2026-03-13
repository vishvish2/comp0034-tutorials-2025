from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
from sqlmodel import Session

from backend.core.db import engine, init_db
from backend.routes import games_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events.

    Handles startup and shutdown events for the FastAPI application.
    On startup, initializes the database by creating tables if they don't exist.
    """
    with Session(engine) as session:
        init_db(session)
        yield


app = FastAPI(
    title="Paralympics API",
    lifespan=lifespan
)

# Allow requests from front end apps running on localhost
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:8050",  # dash default
    "http://localhost:5000",  # flask default
    "http://localhost:8501",  # streamlit default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the router after you app = FastAPI() the CORSMiddleware is registered.
app.include_router(games_router.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}