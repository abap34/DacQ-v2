FROM python:3.9-slim

WORKDIR /app


COPY . .

RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential pkg-config

RUN apt-get install build-dep python-psycopg2



COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


CMD ["python", "app.py"]
