FROM python:3.12-slim
WORKDIR /app

COPY ai-agent /tmp/ai-agent
RUN pip install --no-cache-dir /tmp/ai-agent

COPY backend/pyproject.toml .
COPY backend/src ./src
RUN pip install --no-cache-dir .

ENV PYTHONUNBUFFERED=1
EXPOSE 8080
CMD ["uvicorn", "hr_interview_backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
