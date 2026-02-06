from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.connection import create_db_and_tables
from .routes import eval, mem
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables() # DB 생성 한 번만
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(eval.router)
app.include_router(mem.router)
