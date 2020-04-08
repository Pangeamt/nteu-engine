import yaml


class Config:
    def __init__(self, path: str):
        with open(path, "r") as config_file:
            self._config = yaml.safe_load(config_file)

    def seg_template(self):
        seg_host = self._config["segmenterServer"]["host"]
        seg_port = self._config["segmenterServer"]["port"]
        return f"""
[supervisord]
nodaemon=true

[program:engine]
command=sh -c 'python3.7 /launch_engine.py && kill 1'

[program:segmenter]
command=sh -c 'rackup --host {seg_host} -p {seg_port} && kill 1'

[program:gateway]
command=sh -c 'python3.7 /launch_nteu_gateway.py && kill 1'
"""

    def docker_template(self):
        commands = ""
        for command in self._config["docker_commands"]:
            commands += command + "\n"
        gateway_version = self._config["nteuGatewayVersion"]
        return f"""
FROM ubuntu:18.04

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
RUN export DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-get install -y gcc
RUN apt-get install -y make
RUN apt-get install -y git

# Install python3.7
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.7
RUN apt-get -y install python3-pip

# Install ruby
RUN apt-get install -y ruby-full
RUN apt-get install -y supervisor
RUN rm -rf /var/lib/apt/lists/*

RUN gem install bundler
RUN gem install pragmatic_segmenter_server

COPY requirements.txt /home/requirements.txt
RUN python3.7 -m pip install pip
RUN python3.7 -m pip install -r /home/requirements.txt

RUN python3.7 -m pip install https://github.com/Pangeamt/nteu_gateway/archive/{gateway_version}.tar.gz
RUN git clone https://github.com/Pangeamt/nteu_ui

RUN mv /nteu_ui/ui /

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY launch_nteu_gateway.py /launch_nteu_gateway.py
COPY config.ru config.ru
COPY config.yml /config.yml

{commands}

CMD ["/usr/bin/supervisord"]
"""
