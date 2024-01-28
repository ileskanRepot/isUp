# syntax=docker/dockerfile:1
   
FROM python:3.9

WORKDIR /isUp

COPY . .

RUN apt-get update && apt-get install -y postgresql-client

RUN pip install --no-cache --upgrade -r /isUp/requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "trace", "--workers", "1"]
