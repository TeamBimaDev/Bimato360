# Stage 1: Build Stage
FROM python:3.9-alpine3.13 as builder

ENV PYTHONUNBUFFERED 1

# Install build dependencies
RUN apk add --no-cache \
        build-base \
        postgresql-dev \
        musl-dev \
        zlib-dev \
        libjpeg \
        jpeg-dev \
        pcre-dev \
        linux-headers \
        fontconfig \
        ttf-dejavu \
        pango-dev

WORKDIR /app

COPY ./requirements.txt .

# Create virtual environment and install Python dependencies
RUN python -m venv /venv && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt && \
    /venv/bin/pip install celery==5.3.1


# Stage 2: Production Stage
FROM python:3.9-alpine3.13

ENV PYTHONUNBUFFERED 1

# Install runtime dependencies
RUN apk add --no-cache \
        postgresql-client \
        libjpeg \
        pcre \
        py3-pip \
        py3-pillow \
        py3-cffi \
        py3-brotli \
        gcc \
        musl-dev \
        python3-dev \
        pango \
        fontconfig \
        ttf-dejavu

COPY --from=builder /venv /venv
COPY ./app /app
COPY ./scripts /scripts

WORKDIR /app

# Add user and set permissions
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
