FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app

EXPOSE 8000

ENV UVICORN_CMD="uvicorn app.hf_main:app --host 0.0.0.0 --port 8000 --reload"

CMD ["sh", "-c", "$UVICORN_CMD"]
