from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import models
from .db.db import engine
from .router import jokes, math

app = FastAPI(title="Reto Backend")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """Creates all database tables if they do not exist."""
    models.Base.metadata.create_all(bind=engine)


app.include_router(math.router)
app.include_router(jokes.router)
