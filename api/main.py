import os

import httpx
import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Butler API")
AGENT_URL = os.environ.get("AGENT_URL", "http://agent:8001")


class AgentRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)


@app.get("/health")
async def health():
    try:
        async with await psycopg.AsyncConnection.connect(
            host=os.environ.get("DB_HOST", "db"),
            port=int(os.environ.get("DB_PORT", "5432")),
            dbname=os.environ.get("DB_NAME", "butler"),
            user=os.environ.get("DB_USER", "butler"),
            password=os.environ["DB_PASSWORD"],
            connect_timeout=3,
        ) as connection:
            await connection.execute("SELECT 1")
        async with httpx.AsyncClient(timeout=3) as client:
            response = await client.get(f"{AGENT_URL}/health")
            response.raise_for_status()
    except (psycopg.Error, httpx.HTTPError):
        raise HTTPException(status_code=503, detail="A dependency is unavailable")
    return {"status": "ok", "database": "connected", "agent": "connected"}


@app.post("/agent")
async def run_agent(request: AgentRequest):
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(f"{AGENT_URL}/run", json=request.model_dump())
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="Agent request failed")
