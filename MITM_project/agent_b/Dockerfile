# agent_b/Dockerfile
FROM python:3.9-slim
RUN pip install fastapi uvicorn requests
COPY . /app
WORKDIR /app

# tool_server:app 대신 agent_b:app을 실행하고, 포트를 8001로 맞춤
CMD ["uvicorn", "agent_b:app", "--host", "0.0.0.0", "--port", "8001"]