FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential g++ && apt-get install -y wget && apt-get clean
RUN wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin

COPY requirements/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app/app
COPY config /app/config
