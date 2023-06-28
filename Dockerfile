FROM python:3.11.2-alpine

WORKDIR /fastapi_online_store/project

ARG BUILD_DEPS="build-base gcc libffi-dev openssl-dev libpq-dev"
ARG RUNTIME_DEPS="libcrypto1.1 libssl1.1 libpq-dev"

COPY requirements/requirements_prod.txt ./requirements.txt

RUN apk add --no-cache --virtual .build-deps ${BUILD_DEPS} \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps \
    && apk add --no-cache ${RUNTIME_DEPS}

COPY src ./
