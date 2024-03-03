#FROM python:3.12.2-slim AS builder
FROM python:3.12.2-slim
ENV PYTHONUNBUFFERED 1

RUN mkdir /rishad
WORKDIR /rishad

COPY ../poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.7.1 \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi

COPY ./src /rishad/src

CMD ["poetry", "run", "python", "src/manage.py", "runserver", "0.0.0.0:8000"]