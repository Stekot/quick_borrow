# Using official Python image
FROM python:3.11-slim

# Setting environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.6.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    PATH="/opt/poetry/bin:${PATH}"

# Installing system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd libpq-dev gcc libc-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Installing poetry via pip
RUN pip install "poetry==$POETRY_VERSION"

# Copy the wait-for script
COPY wait-for /usr/local/bin/wait-for
RUN chmod +x /usr/local/bin/wait-for

# Setting work directory
WORKDIR /app

# Copying the project files into the container
COPY . /app/

# Installing Python dependencies using poetry
RUN poetry install -n
