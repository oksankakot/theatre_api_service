FROM python:3.12.1-alpine
LABEL maintainer="oksanka.kot@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR theatre

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .


RUN adduser \
    --disabled-password \
    --no-create-home \
    my_user

USER my_user
