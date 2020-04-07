#!/usr/bin/env python3.7

import os
from config import Config


config = Config("config.yml")

if os.path.exists("supervisord.conf"):
    print("Supervisor config file already exists.")
else:
    with open("supervisord.conf", "w") as supervisor_conf:
        supervisor_conf.write(config.seg_template())

if os.path.exists("Dockerfile"):
    print("Dockerfile already exists.")
else:
    with open("Dockerfile", "w") as dockerfile:
        dockerfile.write(config.docker_template())
