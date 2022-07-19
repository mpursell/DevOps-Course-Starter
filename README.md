[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

## Dependencies

### Poetry
The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

### Trello
You'll need to sign up for a a Trello account https://trello.com/.  Once you have an account, you'll need to get your API key and token at https://trello.com/app-key.  These should be added to your .env file as API_KEY and API_TOKEN.  You'll also need to setup a board on Trello, and add that board ID to your .env as TRELLO_BOARD_ID. 

The app will require the Python module "requests" to function.  Add this to the poetry virtual enviroment by running "poetry add requests"


## Pytest
Pytest is required to run the test suite - https://pypi.org/project/pytest/

#### Unit Testing
Unit tests should be launched from the root of the project and within the poetry virtual environment:

```bash
$ poetry run pytest
```

For verbose output:

```bash
$ poetry run pytest -v
```

If there is an issue running pytest, you may find that your path hasn't been added to the PYTHONPATH variable, in which case you can run:

```bash
$ poetry run python3 -m pytest -v
```
to include your path in PYTHONPATH for the duration of the test run. 


### End to End Testing

The Selenium testing framework and the web driver for your browser is required to complete the integraiton tests.  The browser drivers can be found [here](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/).

Selenium can be installed by running

```bash
$ pip install selenium
```
from inside your Poetry virtual environment. 


## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


## Vagrant

The repo has a Vagrantfile configured to allow the app to run in a vagrant virtual machine. Vagrant will map port 5000 on the host to port 5000 on the box. 

### Installing Vagrant

Vagrant will require a hypervisor.  This app has been tested with [VirtualBox](https://www.virtualbox.org/).  Once the hypervisor is installed, you will need to download and install vagrant from the [official website](https://www.vagrantup.com/). 

You can check the Vagrantfile by running:

```bash
$ vagrant validate
```

If validation is successful, you can run:

```bash
$ vagrant up
```
to provision the vagrant box. 

## Gunicorn

The vagrant box is configured to use gunicorn to serve the app.  Vagrant will provision gunicorn, map the host port 5000 to the box port 5000.  Gunicorn will run in daemon mode. 

## Ansible

An Ansible playbook and inventory are included to configure the web app on an Ansible managed node.  These need to be copied to the Ansible controller node.  In addition to this you will need to create a YAML file that contains your secrets on the controller node:

```
secret_key: <value>
trello_board_id: <value>
logfile: <value>
api_key: <value>
api_token:<value>
```
Once the secrets file has been created, you'll need to encrypt it with:

`ansible-vault encrypt <filename>`

This will ask you to enter an encryption password.  Do this and then create a new YAML file that contains only that vault password. 

Once you have: 

* The playbook 
* The inventory 
* The encrypted secrets file 
* The password file 

on the controller node, you can run the playbook with this command:

`ansible-playbook playbook.yaml -i ansible-inventory.yaml -e @<secrets_file>.yaml -e host=<managed node IP address> --vault-password-file <vault password file>.yml`

### Adding more hosts to Ansible

You can configure the inventory to run the playbook on more than one host.  In that case you would need to edit the ansible-inventory.yaml to look something like this:

```
all:
    children:
        managedhosts:
            hosts:
                "{{host1}}"
                "{{host2}}"
```

And then amend your `ansible-playbook` command to add the extra host address:

`ansible-playbook playbook.yaml -i ansible-inventory.yaml -e @<secrets_file>.yaml -e host1=<managed node IP address> -e host2=<second managed node address> --vault-password-file <vault password file>.yml`


## Docker

Both production and developement containers can be created with Docker.  As before you will need a .env file in the root folder, and the docker commands below assume you are running them from that root project folder.  

### Building Development Containers

Both production and development builds run from one multi-stage build documented in the Dockerfile.  In order to build development containers do the following:

```
$ docker-compose up development
```

This builds the "**development**" stage from the *Dockerfile*, and *docker-compose.yml* tags the image as "**todo-app:dev**"  The *docker-compose.yml* also assumes that the root folder is the build context that should be passed to docker ("**.**").

The local:container ports will be mapped to **5000:5000** by default. 

### Building Production Containers

Very similar process to building a development container, but you need to target the "**production**" build stage in the Dockerfile to build the image with docker-compose:

```
$ docker-compose up production
```
The local:container ports will be mapped to **5001:5000** by default. 

### Differences Between Production and Development Containers

* Web servers - Production runs **gunicorn** and dev runs **flask**.  
* Entrypoints - Production runs ./docker-entrypoint.sh in order to run gunicorn.  Development runs ./docker-entrypoint-dev.sh to run flask.  
* Volume mounts - Production has no volumes mounted, development will try to mount a local folder to the container to allow for code updates. 
* Local ports - Both prod and dev web servers run on port 5000 in the container.  Production is mapped 5000:5000 while development is mapped 5001:5000 so both containers can be run on the host simultaenously.

### Building Testing Containers

Very similar process to building a development container, but you need to target the "**testing**" build stage in the Dockerfile to build the image with docker-compose:

```
$ docker-compose up testing
```
This container will run automated unit / integration / e2e tests using pytest launched from the entrypoint shell script. 


### Building and Running All Containers (Production / Development / Testing)

To build and run images / containers for both prod and dev:

```
$ docker-compose up -d

```
The docker-compose command above will bring up containers for prod and dev and run them in detached mode.

### Persistent Test Running 

The repository includes a *tricks.yaml* in the root file which can be used in conjuncation with **watchdog/watchmedo** to run the docker test container everytime a change is made to a *\.py*, *\.html*, *\.env*, or *\.toml* file.  

Install **watchdog/watchmedo** using the instructions here: https://github.com/gorakhargosh/watchdog/

Once installed you can run

```
$ watchmedo tricks tricks.yaml
``` 
from the root project folder to monitor the folder.  The monitoring is recursive by default. 

## CI Pipeline Config

The project is currently setup to use4 Github Actions as the CI pipeline.  The workflows are defined in the YAML files in `.github/workflows`

* black.yaml - this lints the code with the Black code linter
* ci-pipeline - this builds and tests the code
* workflow-status-notifications - this pushes Slack notifications both when the pipeline runs and when it has succeeded / failed

## Heroku  

### Building the image 

In order to deploy to heroku, a specific set of container build instructions and content is required. Run:


```
$ docker build . --target herokubuild --tags registry.heroku.com/mike-todoapp/web:latest
``` 

or: 

```
$ docker-compose build . herokubuild
``` 
 
in order to build the image ready for heroku deployment. 

### Pushing the heroku image

You'll need to download the heroku CLI from https://devcenter.heroku.com/articles/heroku-cli.  Login with 

```
$ heroku login
``` 

When the docker image is built and ready to deploy, push the image to the heroku registry:

```
$ docker push registry.heroku.com/mike-todoapp/web
``` 

The container will be pushed but won't be ready for use until you release it via the heroku CLI:


```
$ heroku container:release web
``` 

This will make the application ready to run, but before it can run successfully, you'll need to set your configuration up. 
You need to set your environment variables in heroku by going to https://dashboard.heroku.com/apps/$appName > Settings > Config Vars

Once the configuration has been setup you can either run the app from https://dashboard.heroku.com/apps/$appName or from https://$appName.herokuapp.com


## Deploying to Azure App Service

### Create the app 

* Create the app service plan:
```
$ az appservice plan create --resource-group<resource_group_name> -n <appservice_plan_name> --sku B1 --is-linux
```
* Create the web app:
```
$az webapp create --resource-group <resource_group_name> --plan <appservice_plan_name> --name <webapp_name> --deployment-container-image-name <dockerhub_username>/todo-app:latest
```
* Setup the config / environment for the web app:
```
$ az webapp config appsettings set -g <resource_group_name> -n<webapp_name> --settings @settings.json
```
where settings.json contains the key:value pairs of your enviroment variables. 

### Configure the app

Go into the app in the Azure portal, and go to Deployment Center.  There you need to configure the docker public registry and the image you want to pull from docker. 

### Diagnostics

log files can be found in the Azure portal / your web app / Log Stream, or in the Deployment Center / Logs

