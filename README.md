# Butler

All Docker configuration lives at the project root. `compose.yaml` manages all
three containers, networking, startup order, and database storage. The single
`Dockerfile` has separate `api` and `agent` build targets; PostgreSQL uses its
official image. The `app/`, `api/`, and `agent/` folders contain application code.

## Start

```powershell
Copy-Item .env.example .env
docker compose up --build -d
```

Set `POSTGRES_PASSWORD` in `.env` before using this outside local development.

- `app/`: frontend placeholder.
- `api/`: FastAPI service at http://localhost:8000 (interactive docs at `/docs`).
- `agent/`: internal agent service with a placeholder message endpoint.
- `butler-db`: PostgreSQL database named `butler`, persisted in a Docker volume.

Compose provides a private network. The API connects to PostgreSQL at `db:5432`
and the agent at `http://agent:8001`. Only the API is published to the host,
bound to localhost. Health checks verify both dependencies before API startup.

## Verify

```powershell
docker compose ps
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/agent -Method Post -ContentType 'application/json' -Body '{"message":"Hello Butler"}'
```

The health endpoint checks a database query and agent HTTP connectivity.
The agent currently acknowledges messages; it does not run an AI model yet.

Stop containers with `docker compose down`. Database data is retained unless
you explicitly remove the volume.
