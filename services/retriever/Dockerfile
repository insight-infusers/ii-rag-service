FROM python:3.10-slim
WORKDIR /app
COPY ./services/retriever /app
COPY ./schema /app/schema
COPY ./core /app/core
COPY config.py settings.yml .secret.yml /app/
RUN pip install --no-cache-dir --progress-bar=off -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
