# FROM redis
FROM sameersbn/redis

LABEL maintainer="Darío López Padial <dariolopezpadial@gmail.com>"

RUN set -xe
RUN apt-get update
RUN apt-get --assume-yes install python3-pip
RUN apt-get update -y
RUN apt-get install -y python3-setuptools python3-dev

COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir --requirement /tmp/requirements.txt

COPY ./test test
RUN python3 -m unittest test