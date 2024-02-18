For Recommendation:

1. Create docker image:
docker build --no-cache --tag recommendation --build-arg config_file=<config file> --build-arg log_level=<log-level debug|error|info|critical> .
example:
	docker build --no-cache --tag recommendation --build-arg config_file="reco_config.json" --build-arg log_level="debug" .
	docker build --no-cache --tag recommendation --build-arg config_file="reco_aws_config.json" --build-arg log_level="debug" .

2. Run the docker container with the above image
$ docker run --rm --name reco -d --network="host" recommendation
