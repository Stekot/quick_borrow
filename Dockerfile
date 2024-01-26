FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.6.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    PATH="/opt/poetry/bin:${PATH}"

RUN apk add build-base libffi-dev postgresql-dev

COPY wait-for /usr/local/bin/wait-for
RUN chmod +x /usr/local/bin/wait-for

WORKDIR /app

# Copying the project files into the container
COPY requirements.txt /app/

# Installing Python dependencies using poetry
RUN pip install -r /app/requirements.txt

EXPOSE 8080

# ENTRYPOINT ["python", "manage.py"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]