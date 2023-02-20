FROM ubuntu:latest


ENV HOME /opt/app/
WORKDIR /opt/app/

ENV TZ=Europe/Rome
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get upgrade -y
RUN apt install python3-dev python3-pip -y

COPY app/requirements.txt $HOME/.
RUN pip install -r $HOME/requirements.txt 
