# Multi-stage build for OpenG2P SPAR Bene Portal API
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy all local packages
COPY openg2p-spar-models /build/openg2p-spar-models
COPY openg2p-spar-mapper-core /build/openg2p-spar-mapper-core
COPY openg2p-spar-bene-portal-api /build/openg2p-spar-bene-portal-api

# Install Python dependencies from git and local packages
RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install --no-cache-dir \
    git+https://github.com/openg2p/openg2p-fastapi-common@1.1#subdirectory=openg2p-fastapi-auth-models \
    git+https://github.com/openg2p/openg2p-fastapi-common@1.1#subdirectory=openg2p-fastapi-auth \
    git+https://github.com/openg2p/openg2p-fastapi-common@1.1#subdirectory=openg2p-fastapi-common && \
    python -m pip install --no-cache-dir -e /build/openg2p-spar-models && \
    python -m pip install --no-cache-dir -e /build/openg2p-spar-mapper-core && \
    python -m pip install --no-cache-dir -e /build/openg2p-spar-bene-portal-api

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

# Copy application code from bene-portal-api
COPY --chown=${container_user}:${container_user_group} openg2p-spar-bene-portal-api/src /app/src
COPY --chown=${container_user}:${container_user_group} openg2p-spar-bene-portal-api/main.py /app/main.py
COPY --chown=${container_user}:${container_user_group} openg2p-spar-bene-portal-api/pyproject.toml /app/pyproject.toml

# Create a minimal README.md if it doesn't exist (required by pyproject.toml)
RUN if [ ! -f /app/README.md ]; then echo "# OpenG2P SPAR Bene Portal API" > /app/README.md; fi

# Install bene-portal-api package
# Note: openg2p-spar-mapper-core and openg2p-spar-models are already installed
# from the builder stage via git dependencies
RUN python -m pip install --no-cache-dir -e /app

# Set ownership
RUN chown -R ${container_user}:${container_user_group} /app

# Switch to non-root user
USER ${container_user}

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV SPAR_BENE_PORTAL_HOST=0.0.0.0
ENV SPAR_BENE_PORTAL_PORT=8000
ENV SPAR_BENE_PORTAL_NO_OF_WORKERS=4


# Run application
CMD ["sh", "-c", "gunicorn main:app --workers ${SPAR_BENE_PORTAL_NO_OF_WORKERS} --worker-class uvicorn.workers.UvicornWorker --bind ${SPAR_BENE_PORTAL_HOST}:${SPAR_BENE_PORTAL_PORT} --access-logfile - --error-logfile -"]
