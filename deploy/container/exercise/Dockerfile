FROM ubuntu:xenial

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev vim
WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

