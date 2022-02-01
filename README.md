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
Unittests should be launched from the root of the project and within the poetry virtual environment:

```bash
$ poetry run pytest
```

For verbose output:

```bash
$ poetry run pytest -v
```

If there is an issue running pytest, you may find that your path hasn't been added to the PYTHONPATH variable, in which case you can run:

```bash
$ python3 -m pytest -v
```
to include your path in PYTHONPATH for the duration of the test run. 


### Integration Testing

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
