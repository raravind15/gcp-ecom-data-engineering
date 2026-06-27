FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["functions-framework","--source=src_to_land_gcs.py","--target=gcs_trigger","--signature-type=cloudevent","--port=8080"]