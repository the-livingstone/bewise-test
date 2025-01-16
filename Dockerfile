FROM python:3.11-slim-bookworm
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt -y install nano curl g++ && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip poetry

WORKDIR /opt/app

COPY bewise_test bewise_test

COPY .env poetry.lock pyproject.toml README.md ./

RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi

WORKDIR /opt/app/bewise_test


EXPOSE 8000
ENTRYPOINT ["python", "-m", "bewise_test.app.main"]