FROM python:3.11.13-alpine3.22

ARG container_user=openg2p
ARG container_user_group=openg2p
ARG container_user_uid=1001
ARG container_user_gid=1001

RUN apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers make
RUN apk add --no-cache bash git gettext libpq-dev postgresql16-client

RUN addgroup -g ${container_user_gid} ${container_user_group} \
  && adduser -D -u ${container_user_uid} -G ${container_user_group} -s /bin/bash ${container_user}

WORKDIR /app

ADD . /app/src
RUN mv /app/src/main.py /app

RUN pip install git+https://github.com/openg2p/openg2p-fastapi-common@1.1\#subdirectory=openg2p-fastapi-common  # to_be_removed_on_tag
RUN pip install git+https://github.com/openg2p/openg2p-g2pconnect-common-lib@1.1\#subdirectory=openg2p-g2pconnect-common-lib # to_be_removed_on_tag
RUN pip install git+https://github.com/openg2p/openg2p-g2pconnect-common-lib@1.1\#subdirectory=openg2p-g2pconnect-mapper-lib # to_be_removed_on_tag
RUN pip install -e /app/src

RUN apk del --no-network .build-deps

USER ${container_user}

ENV PYTHONUNBUFFERED=1
ENV SPAR_MAPPER_WORKER_TYPE=local
ENV SPAR_MAPPER_HOST=0.0.0.0
ENV SPAR_MAPPER_PORT=8000
ENV SPAR_MAPPER_NO_OF_WORKERS=8

CMD python3 main.py migrate; \
    gunicorn "main:app" --workers ${SPAR_MAPPER_NO_OF_WORKERS} --worker-class uvicorn.workers.UvicornWorker --bind ${SPAR_MAPPER_HOST}:${SPAR_MAPPER_PORT}
