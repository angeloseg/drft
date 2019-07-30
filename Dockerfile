FROM python:3.6

ENV PYTHONBUFFERED=1

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

