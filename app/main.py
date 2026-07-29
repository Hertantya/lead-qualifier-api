"""FastAPI app entrypoint. Run with: uvicorn app.main:app --reload"""
from fastapi import FastAPI

from app.routers import agent, ask, qualify

app = FastAPI(
    title="Lead Qualifier API",
    description="LLM-powered lead qualification, document Q&A, and a sales-research agent.",
    version="0.1.0",
)

app.include_router(qualify.router)
app.include_router(ask.router)
app.include_router(agent.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
