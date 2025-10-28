# Multi-stage build for OpenG2P SPAR Mapper API
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install --no-cache-dir \
    git+https://github.com/openg2p/openg2p-fastapi-common@1.1#subdirectory=openg2p-fastapi-auth-models \
    git+https://github.com/openg2p/openg2p-fastapi-common@1.1#subdirectory=openg2p-fastapi-auth \
    git+https://github.com/openg2p/openg2p-fastapi-common@1.1#subdirectory=openg2p-fastapi-common

# Production stage
FROM python:3.11-slim

ARG container_user=openg2p
ARG container_user_group=openg2p
ARG container_user_uid=1001
ARG container_user_gid=1001

# Create non-root user
RUN groupadd -g ${container_user_gid} ${container_user_group} && \
    useradd -mN -u ${container_user_uid} -G ${container_user_group} -s /bin/bash ${container_user}

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    gunicorn \
    && rm -rf /var/lib/apt/lists/*

# Copy built packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=${container_user}:${container_user_group} . /app/src
COPY --chown=${container_user}:${container_user_group} main.py /app

# Install local packages
RUN cd /app/src && python -m pip install --no-cache-dir -e .

# Set ownership
RUN chown -R ${container_user}:${container_user_group} /app

# Switch to non-root user
USER ${container_user}

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV SPAR_MAPPER_API_HOST=0.0.0.0
ENV SPAR_MAPPER_API_PORT=8000
ENV SPAR_MAPPER_API_NO_OF_WORKERS=4


# Run application
CMD gunicorn "main:app" \
    --workers ${SPAR_MAPPER_API_NO_OF_WORKERS} \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind ${SPAR_MAPPER_API_HOST}:${SPAR_MAPPER_API_PORT} \
    --access-logfile - \
    --error-logfile -
