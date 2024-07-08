FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential pkg-config

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "home.py", "--server.port=5001"]
