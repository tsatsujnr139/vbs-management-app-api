FROM python:3.7
LABEL maintainer="Tsatsu Adogla-Bessa Jnr"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /code
WORKDIR /code

COPY requirements ./requirements

ARG requirements=requirements/production.txt

RUN pip install -r $requirements

COPY . /code/
