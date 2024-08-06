<<<<<<< HEAD
# Stage 1: Build Stage
FROM python:3.11-slim-bullseye as builder

ENV PYTHONUNBUFFERED 1

# Install build dependencies
RUN apt-get update && apt-get install -y \
        build-essential \
        libpq-dev \
        zlib1g-dev \
        libjpeg-dev \
        libpango1.0-dev \
        libpangoft2-1.0-0 \
        libopenjp2-7-dev \
        pango1.0 \
        libpcre3-dev \
        linux-headers-amd64 \
        fontconfig \
        fonts-dejavu-core \
        zbar-tools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt .

# Create virtual environment and install Python dependencies
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt


# Stage 2: Production Stage
FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED 1

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
        postgresql-client \
        libjpeg62-turbo \
        libpcre3 \
        libpango1.0-0 \
        libpangoft2-1.0-0 \
        fontconfig \
        fonts-dejavu-core \
        zbar-tools \
        python3-pip \
        python3-pillow \
        libffi-dev \
        libbrotli1 \
        libopenjp2-7 \
        gcc \
        musl-dev \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /venv /venv
COPY ./app /app
COPY ./scripts /scripts
COPY ./sql_mock /sql_mock

WORKDIR /app


RUN adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static

USER root

RUN chown -R django-user:django-user /vol && \
    chown -R django-user:django-user ./* && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts


ENV PATH="/venv/bin:/scripts:$PATH"

EXPOSE 8000

USER django-user

CMD ["sh", "/scripts/run.sh"]
=======
# Stage 1: Build Stage
FROM python:3.11-slim-bullseye as builder

ENV PYTHONUNBUFFERED 1

# Install build dependencies
RUN apt-get update && apt-get install -y \
        build-essential \
        libpq-dev \
        zlib1g-dev \
        libjpeg-dev \
        libpango1.0-dev \
        libpangoft2-1.0-0 \
        libopenjp2-7-dev \
        pango1.0 \
        libpcre3-dev \
        linux-headers-amd64 \
        fontconfig \
        fonts-dejavu-core \
        zbar-tools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt .

# Create virtual environment and install Python dependencies
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt


# Stage 2: Production Stage
FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED 1

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
        postgresql-client \
        libjpeg62-turbo \
        libpcre3 \
        libpango1.0-0 \
        libpangoft2-1.0-0 \
        fontconfig \
        fonts-dejavu-core \
        zbar-tools \
        python3-pip \
        python3-pillow \
        libffi-dev \
        libbrotli1 \
        libopenjp2-7 \
        gcc \
        musl-dev \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /venv /venv
COPY ./app /app
COPY ./scripts /scripts
COPY ./sql_mock /sql_mock

WORKDIR /app


RUN adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static

USER root

RUN chown -R django-user:django-user /vol && \
    chown -R django-user:django-user ./* && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts


ENV PATH="/venv/bin:/scripts:$PATH"

EXPOSE 8000

USER django-user

CMD ["sh", "/scripts/run.sh"]
>>>>>>> origin/ma-branch
