FROM python:3.12-slim

WORKDIR /app

COPY shared ./shared
COPY services/platform_jobs ./services/platform_jobs

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r services/platform_jobs/requirements.txt

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "services.platform_jobs.app:app"]