# NTEU Engine

Here we provide a gateway with a fake translation engine server injected. This model has a `/mytranslation` post endpoint that is used in the file `launch_nteu_gateway.py` to connect the gateway `/translate` endpoint with the fake translation engine.

## Instructions

### Configuration
In order to inject your translation model inside the nteu gateway you should modify:

- replace `launch_engine.py` with your script to launc the translation engine server.

- `config.yml` in the section `translationEngineServer`, you may modify `installDockerCmds` to setup the launch of the translation engine, copying every necesary file into the docker and any additional operation. You should also modify `startCmd` with the command line order to launch your translation engine server.

- `launch_nteu_gateway.py` the `translate` function to connect with your translation engine server using its endpoints and returning the list of translations.

- You can also replace the texts in the folder `test_texts` to do a bleu evaluation with a get endpoint in `/test`


### Building and running the docker image

- Once everything is setup, run `create_dockerfile.py` with python >= 3.7

- Then `docker build . -t <image_name>`

- Finally `docker run -p <machine_port>:<config["gatewayServer"]["port"]> -i <image_name>` where `machine_port` is the port of your machine where you want to access the gateway server.


### Testing

- In order to test the docker image, once it's running you can use this command: `curl -d '{"texts": ["test"]}' http://0.0.0.0:10000/translate`
