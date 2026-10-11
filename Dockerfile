FROM python:3.13-slim AS base
WORKDIR /service
RUN useradd --create-home service

FROM base AS api
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY api/main.py .
USER service
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM base AS agent
COPY agent/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY agent/main.py .
USER service
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
