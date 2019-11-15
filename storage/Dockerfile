FROM python:alpine3.9

ARG STORAGE_SERVICE_PORT

WORKDIR /storage/app/
ADD requirements.txt /storage/

EXPOSE ${STORAGE_SERVICE_PORT}

RUN python3 -m pip install -r ../requirements.txt
