backend=$(shell sudo docker-compose ps -q backend)

# Initial Configuration
setup-environment:
	(./create_env.sh && git config core.hooksPath .githooks)

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

# Code style
code-style-verbose:
	sudo docker exec $(backend) /bin/bash -c 'find ./ -not -path "./docs*" -iname "*.py" | xargs pipenv run pycodestyle --verbose'

# Code style
code-style:
	sudo docker exec $(backend) /bin/bash -c 'find ./ -not -path "./docs*" -iname "*.py" | xargs pipenv run pycodestyle --quiet'

# Generate documentation
documentation:
	sudo docker exec $(backend) /bin/bash -c 'cd docs && pipenv run sphinx-apidoc -o . ../server/ -M --ext-autodoc -f && pipenv run make clean && pipenv run make html'


