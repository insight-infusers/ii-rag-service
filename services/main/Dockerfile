FROM python:3.10
WORKDIR /app
COPY ./services/main/app /app
COPY config.py settings.yml .secret.yml /app/
RUN pip install -r requirements.txt --no-cache-dir --progress-bar=off
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
