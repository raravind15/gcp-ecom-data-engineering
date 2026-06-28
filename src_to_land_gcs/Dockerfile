FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["functions-framework","--source=main.py","--target=gcs_trigger","--signature-type=cloudevent","--port=8080"]