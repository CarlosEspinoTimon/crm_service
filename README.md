# CRM_service
This is an example of a backend CRM Service that is composed of:
- Server: developed in Python with the Flask framework
- Database: a MySQL 5.7 database
## __Getting Started__
To start developing in this project, you just have to clone the repository, meet the prerequisites and run the command shown in the Run the server section.
### __Prerequisites__
You need to have installed:
- docker-compose 
- docker

You need to create a .env file in the `app` directory with some variables:
```
FLASK_APP=server:create_app('config.Dev')
FLASK_ENV=development
DATABASE_URI=YOUR_PRODUCTION_DATABASE 
PYTHONUNBUFFERED=1
GOOGLE_LOGIN_CLIENT_ID=YOUR_CLIENT_ID
GOOGLE_LOGIN_CLIENT_SECRET=YOUR_CLIENT_SECRET
GOOGLE_APPLICATION_CREDENTIALS=.credentials/crm-service-storage-key.json
GOOGLE_PROJECT=PROJECT_NAME
GOOGLE_BUCKET=BUCKET_NAME
```

This file is in the gitignore, so no credentials are going to be uploaded to the repository.

The `DATABASE_URI` is just for production, the config.Dev file configures by default the URI to the local database of the docker-compose, so you can leave it like it is in the example.

You have to create a `.credentials/` folder in the `app` directory where you have to put the Google Cloud Storage bucket key and it has to be named `crm-service-storage-key.json`.

### __Run the server__
The server runs by default in development mode. The first time you have to run (from the `development_environmet` directory):

`make setup-environment`

This will create a `.env` file, untracked by git, with the host GID and UID. This information is used by Docker while creating the container to create a user with the same privileges that your user. 

It will also configure the githooks, see the Githooks section to see more information about it.

To start it, you have to run (from the `development_environmet` directory):

`make init`

### __Running the tests__
The test are run in a test database, to run them you can just execute (from the `development_environmet` directory):

`make backend-tests`

## __Working in the project__
As this project is build in a dockerized environment, the developers have to adapt to work with it.

### __Makefile__
As you have seen, as it is a dockerized environment, to interact with it, you have to use a `make` command. There is a Makefile in the `development_environment` directory with a few make commands that will help the developer, as everything must be done inside the container this Makefile simplifies each action that must be done.

### __GitHooks__
In this project I have configured a githook that is runned before each commit to ensure that the code to be commited passes all the test, has no codestyle errors (regarding the PEP8) and in the end, if everything has gone ok, it generates the API documentation with Sphinx. After all this, the commit is done.

This githook is configured the first time when you run `setup-environment`.

### __Install new modules__
The modules have to be installed in the server that is inside the container, so if a developer needs to install a new module, it must be installed with the following command:

`make backend-install-module module='Name of the module'`

This will install the module in the container and it will be added to the Pipfile which is shared with the host and tracked in the repository.

## __Documentation__
As you can see in the GitHooks section, this proyect is configured to automatically generate the documentation for the API with Sphinx before each commit. The generated html code is in `app/docs/_build/html/` you can open the `index.html` and navigate through the documentation.

If you want to see the documentation without doing any commit you can run (from the `development_environment`):

`make documentation`

## __Deployment__
### __Automated deployment__
This repository is integrated within a CI/CD jenkins pipeline. This pipeline builds the environment for the tests and runs them, also, when changes are made in the master branch it deploys the code to App Engine Flexible.
### __Manual deployment__
This server is prepared to be deployed in Google App Engine Flexible, if you wish to deploy it manually, you need to configure the `app.yaml` file and generate the latest `requirements.txt`.
#### __Configure app.yaml__
In the repository there is an `app.yaml` example, in this file you have to change the environment variables for the real ones. For security, to avoid uploading credentials to the repository, you should create a copy of the file and call it `real_app.yaml` which is already in the .gitignore, put the real environment variables there and deploy it with this file.
#### __Generate requirements.txt__
To generate the latest `requirements.txt`, you have to get into the container:

`make access-backend`

and generate the file:

`pipenv lock -r >  requirements.txt`

it is also needed the gunicorn module:

`echo "gunicorn==19.9.0" >> requirements.txt`

we have to remove the first line created by the pipenv lock -r

`echo "$(tail -n +2 requirements.txt)" > requirements.txt`

This file will be created inside the container and in the folder shared with the host.
#### __Deploy it__
Once you have it, you can deploy the app by running: `gcloud app deploy real_app.yaml` in the `app` directory. Beware that you have to have [initiated the cloud SDK](https://cloud.google.com/sdk/docs/initializing "Initializing Cloud SDK")
