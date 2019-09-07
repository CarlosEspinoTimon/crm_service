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

# Run only one test
# usage --> make backend-one-test test="TEST NAME"
backend-one-test:
	sudo docker exec -t $(backend) pipenv run python tests/tests.py '$(test)'

# Code style
code-style-verbose:
	sudo docker exec $(backend) /bin/bash -c 'find ./ -not -path "./docs*" -not -path "./migrations*" -iname "*.py" | xargs pipenv run pycodestyle --verbose'

# Code style
code-style:
	sudo docker exec $(backend) /bin/bash -c 'find ./ -not -path "./docs*" -not -path "./migrations*" -iname "*.py" | xargs pipenv run pycodestyle --quiet'

# Generate documentation
documentation:
	# sudo docker exec $(backend) /bin/bash -c 'cd docs && pipenv run sphinx-apidoc -o . ../server/ -M --ext-autodoc -f && pipenv run make clean && pipenv run make html'
	sudo docker exec $(backend) /bin/bash -c 'cd docs && pipenv run sphinx-apidoc -o . ../server/ --ext-autodoc && pipenv run make clean && pipenv run make html'

# Init database
db_init:
	sudo docker exec -t $(backend) pipenv run flask db init

# Generate database migrations
db_migrate:
	sudo docker exec -t $(backend) pipenv run flask db migrate -m '$(comment)'

# Merge two heads
db_merge:
	sudo docker exec -t $(backend) pipenv run alembic -c migrations/alembic.ini merge heads

# Apply database upgrade
db_upgrade:
	sudo docker exec -t $(backend) pipenv run flask db upgrade

# Apply database downgrade
db_downgrade:
	sudo docker exec -t $(backend) pipenv run flask db downgrade

