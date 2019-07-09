backend=$(shell sudo docker-compose ps -q backend)

# Create environment
create-env:
	./create_env.sh

# Init
init:
	sudo docker-compose up

# Build
build:
	sudo docker-compose build

# Access backend
access-backend:
	sudo docker exec -it $(backend) bash

# Install a module
# usage --> make backend-install-module module="MODULE NAME"
backend-install-module:
	sudo docker exec -t $(backend) pipenv install '$(module)'

# Run the tests
backend-tests:
	sudo docker exec -t $(backend) pipenv run python tests/tests.py




