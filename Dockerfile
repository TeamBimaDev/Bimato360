# Stage 1: Build Stage
FROM python:3.9-alpine3.13 as builder

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache \
        build-base \
        postgresql-dev \
        musl-dev \
        zlib-dev \
        libjpeg \
        jpeg-dev \
        pcre-dev \
        linux-headers

WORKDIR /app

COPY ./requirements.txt .

RUN python -m venv /venv && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

RUN apt install python3-pip libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libffi-dev libjpeg-dev libopenjp2-7-dev
# Stage 2: Production Stage
FROM python:3.9-alpine3.13

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache \
        postgresql-client \
        libjpeg \
        pcre

COPY --from=builder /venv /venv
COPY ./app /app
COPY ./scripts /scripts

WORKDIR /app

RUN adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chown -R django-user:django-user ./* && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/venv/bin:/scripts:$PATH"

EXPOSE 8000

USER django-user

CMD ["sh", "/scripts/run.sh"]
