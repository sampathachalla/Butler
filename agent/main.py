from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Butler Agent")


class AgentRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/run")
def run(request: AgentRequest):
    # Placeholder transport endpoint; wire in the agent implementation here.
    return {"status": "received", "message": request.message}
