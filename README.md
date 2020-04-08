# NTEU Engine

Here we provide a gateway with a fake model injected. This model has a `/mytranslation` post endpoint that is used in the file `launch_nteu_gateway.py` to connect the gateway `/translate` endpoint with the fake model.

## Instructions

### Configuration
In order to inject your translation model inside the nteu gateway you should modify:

- `launch_engine.py` to launch your translation model.

- `config.yml` docker commands section to setup your translation model inside the docker. Also indicate in the fields `host` and `port` inside `translationEngineServer` the ip address and the port to access your translation model from inside the docker.

- `launch_nteu_gateway.py` the `translate` function to connect with your translation model using its endpoints and return the list of translations.


### Building and running the docker image

- Once everything is setup, run `create_dockerfile.py` with python >= 3.7

- Then `docker build . -t <image_name>`

- Finally `docker run -p <machine_port>:<config["gatewayServer"]["port"]> -i <image_name>` where `machine_port` is the port of your machine where you want to access the gateway server.
