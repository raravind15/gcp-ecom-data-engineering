FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# CMD ["python", "landing_to_bqraw.py"]
CMD ["functions-framework","--source=landing_to_bqraw.py","--target=gcs_trigger","--signature-type=cloudevent","--port=8080"]