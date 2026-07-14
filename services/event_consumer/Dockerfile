FROM python:3.12-slim

WORKDIR /app

COPY shared ./shared
COPY services/platform_jobs ./services/platform_jobs

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r services/event_consumer/requirements.txt

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "services.event_consumer.app:app"]