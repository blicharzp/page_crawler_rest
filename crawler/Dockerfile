FROM python:alpine3.9

WORKDIR /crawler/app/
ADD requirements.txt /crawler/

RUN apk add build-base
RUN python3 -m pip install -r ../requirements.txt
