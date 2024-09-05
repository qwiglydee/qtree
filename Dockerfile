# qMax <qwiglydee@gmail.com>
#
# Features:
# - nonroot user
# - development container
# - sepearting building/devel stuff from production
#
# Stages:
# - base
# - build: requirements and environment
# - devel: for in-container development
# - prod: for deployment

####
FROM python:3.10-slim-bookworm AS base
####

# creating non-root user
# Note: for bind mounts to work, the IDs should match local user
ARG USERUID=1000
ARG USERGID=1000
RUN addgroup --system --gid=$USERGID appgroup && adduser --system --uid=$USERUID --ingroup appgroup --home /app --shell /bin/sh --disabled-password appuser
RUN chown appuser:appgroup /app

RUN apt-get update

# some general system requirements
RUN apt-get -y install --no-install-recommends \
    # libpq5 \
    # libhiredis0.14 \
    python3-poetry


# a volume to possibly share with other containers or host
# RUN mkdir -p /var/www/static && chmod 777 /var/www/static
# VOLUME var/www/static

####
FROM base AS build
####

# some requirements w/out wheels might need building
# RUN apt-get -y install --no-install-recommends \
#  build-essential \
#  python3-dev \
#  libpq-dev

COPY pyproject.toml poetry.lock /app/

USER appuser:appgroup
WORKDIR /app

ENV POETRY_VIRTUALENVS_CREATE=true
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_VIRTUALENVS_OPTIONS_ALWAYS_COPY=false
ENV POETRY_VIRTUALENVS_OPTIONS_NO_PIP=true
ENV POETRY_VIRTUALENVS_OPTIONS_NO_SETUPTOOLS=true
ENV POETRY_VIRTUALENVS_OPTIONS_SYSTEM_SITE_PACKAGES=true

RUN poetry install --no-root --without dev

####
FROM build AS devel
####

# system utilities to use inside container
#RUN apt-get -y install --no-install-recommends \
# git \
# sqlite3

USER appuser:appgroup
WORKDIR /app

RUN poetry install --no-root --only dev

ENV PATH=/app/.venv/bin:$PATH

# waiting for IDE to connect and run something
CMD sleep infinity

####
FROM base as prod
####

# a tool to wait for another service to get ready
# ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /app/wait
# RUN chmod +x /app/wait
# ENV WAIT_HOSTS=somehost:someport

COPY --from=build --chown=appuser:appgroup /app/.venv /app/.venv

USER appuser:appgroup
WORKDIR /app

COPY --chown=appuser:appgroup . .

ENV PATH=/app/.venv/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# might be redefined by heroku
ENV HOST=0.0.0.0
ENV PORT=8000

# CMD ./wait && python run.py
CMD python run.py