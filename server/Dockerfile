FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get -y install python3-pip
RUN apt-get install python3-dev -y
RUN apt-get install libpq-dev -y
COPY . /server
WORKDIR /server
RUN pip3 install -r requirements.txt