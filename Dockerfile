FROM ubuntu:latest


ENV HOME /opt
WORKDIR /opt/

ENV TZ=Europe/Rome
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get upgrade -y
RUN apt install bash python3-dev python3-pip -y

COPY . /opt/

COPY app/requirements.txt $HOME/.
RUN pip install -r $HOME/requirements.txt 

COPY config.yml /opt/app/config.yml

RUN chmod u+x "/opt/app/run.sh"

WORKDIR /opt/app

CMD ["./run.sh"]
