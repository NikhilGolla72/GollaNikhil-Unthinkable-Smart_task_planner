from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import planner
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Smart Task Planner API")

# Allow frontend at http://localhost:3001
origins = [
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(planner.router, prefix="/api")

@app.get("/")
def root():
    return {"status": "ok", "service": "smart-task-planner backend"}