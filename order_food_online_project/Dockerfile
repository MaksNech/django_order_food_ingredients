FROM ubuntu:bionic

RUN apt-get update

RUN apt-get install -y \
    ca-certificates \
    python3-all-dev \
    python3-venv \
    postgresql-server-dev-all \
    build-essential

RUN python3 -m venv /venv

ENV PATH="/venv/bin:$PATH"

WORKDIR /app

COPY . /app

RUN pip install -U pip wheel

RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN pip install gunicorn

RUN pip install uwsgi

EXPOSE 8000

RUN useradd \
    -g users \
    myuser

USER myuser

CMD uwsgi wsgi.ini

ENV PYTHONUNBUFFERED 1