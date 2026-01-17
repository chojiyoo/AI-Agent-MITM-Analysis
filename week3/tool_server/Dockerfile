FROM python:3.9-slim
RUN pip install fastapi uvicorn
WORKDIR /app
COPY . .
CMD ["uvicorn", "tool_server:app", "--host", "0.0.0.0", "--port", "8000"]