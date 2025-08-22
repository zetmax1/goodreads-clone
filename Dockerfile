FROM python:3.13-slim as base

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  make \
  cron \
  procps \
  netcat-openbsd \
  gettext \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install --no-cache -U pip setuptools


WORKDIR /opt/app/


COPY requirements.txt /opt/app/requirements.txt
COPY manage.py /opt/app/manage.py

RUN chmod +x manage.py

RUN pip install -r /opt/app/requirements.txt

COPY . /opt/app/

CMD ["./manage.py", "runserver", "0.0.0.0:8001"]