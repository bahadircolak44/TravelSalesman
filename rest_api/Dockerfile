FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /rest_api
COPY requirements.txt /rest_api/
RUN apt-get -y install libpq-dev gcc
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
