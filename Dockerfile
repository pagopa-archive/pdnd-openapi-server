FROM vaeum/ubuntu-python3-pip3

RUN apt-get update

RUN apt-get install -y curl
RUN apt-get install -y apt-transport-https
RUN apt-get install -y git-core

RUN git clone https://github.com/teamdigitale/pdnd-openapi-server.git

WORKDIR /pdnd-openapi-server

RUN pip3 install tox

EXPOSE 8080

CMD ["tox", "-e run"]