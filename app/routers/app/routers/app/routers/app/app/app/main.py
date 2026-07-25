app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import intents, queries, evidence, briefs
from app.database import engine, Base

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Briefing API")

# CORS (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(intents.router, prefix="/intents", tags=["intents"])
app.include_router(queries.router, prefix="/queries", tags=["queries"])
app.include_router(evidence.router, prefix="/evidence", tags=["evidence"])
app.include_router(briefs.router, prefix="/briefs", tags=["briefs"])

@app.get("/")
async def root():
    return {"status": "ok"}
