import logging
import os
import requests
import logging.config
import time
import loggly.handlers

from flask import Flask, abort
from flask import render_template
from flask import request
from flask_login import LoginManager, login_required, login_user, current_user

from functools import wraps
from todo_app.flask_config import Config
from todo_app.data.db_service import *
from todo_app.data.user import User
from todo_app.data.viewmodel import ViewModel
from loggly.handlers import HTTPSHandler
from logging import Formatter

from werkzeug.utils import redirect

# Setup loggly log aggregation via a conf file
# configure logging level in conf file.
logging.config.fileConfig("python.conf")
logging.Formatter.converter = time.gmtime


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config())
    logFile = os.environ.get("LOGFILE")
    logger = logging.getLogger("myLogger")

    logging.basicConfig(
        filename=logFile,
        level=logging.os.environ.get("LOG_LEVEL"),
        format="%(asctime)s %(levelname)s %(name)s %(threadName)s: %(message)s",
    )

    # OAuth Login
    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():

        # logic to redirect to GH auth flow if unauthed
        client_id: str = os.environ.get("GH_CLIENTID")
        callback_uri = os.environ.get("CALLBACK_URI")
        logging.info("User not logged in, redirecting to %s", callback_uri)

        return redirect(
            f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={callback_uri}"
        )

    # MongoDB connection and setup
    mongodbConnectionString = os.environ.get("MONGO_CONN_STRING")
    applicationDatabase = os.environ.get("MONGO_DB_NAME")
    logger.info("Connecting to database: %s", applicationDatabase)

    try:
        app_db = AppDatabase(
            mongodbConnectionString,
            database_name=applicationDatabase,
            collection_name="todo",
        )
    except:
        logger.error(
            "Exception thrown when connecting to todo collection in database: %s ",
            applicationDatabase,
        )
        raise Exception("database connection exception")

    try:
        user_db = AppDatabase(
            mongodbConnectionString,
            database_name=applicationDatabase,
            collection_name="auth_users",
        )
    except:
        logger.error(
            "Exception thrown when connecting to users collection in database: %s ",
            applicationDatabase,
        )
        raise Exception("database connection exception")

    @login_manager.user_loader
    def load_user(user_id: str) -> User:

        user_lookup: dict = user_db.get_user(user_id)

        if user_lookup:
            app_user = User(user_id)
            app_user.role = user_lookup["role"]
        else:
            app_user = User(user_id)
            app_user.role = user_db.get_user_role(user_id)

        return app_user

    login_manager.init_app(app)

    @app.route("/")
    @login_required
    def index():

        app_db = AppDatabase(
            mongodbConnectionString,
            database_name=applicationDatabase,
            collection_name="todo",
        )
        card_list: list = app_db.get_items()
        card_list_view_model = ViewModel(card_list)
        card_list_view_model.user_role = current_user.role

        return render_template("index.html", view_model=card_list_view_model)

    def writer_required(func):
        @wraps(func)
        def wrapper():
            if current_user.role == "writer":
                return func()
            else:
                abort(403)

        return wrapper

    @app.route("/add", methods=["POST"])
    @writer_required
    @login_required
    def add_Task():

        title = request.form.get("title")
        description = request.form.get("description")
        listName = request.form.get("listName")

        document = {"title": title, "description": description, "status": listName}

        app_db.add_item(document)
        logging.info("adding task: %s to: %s", document["title"], document["status"])

        return redirect("/")

    @app.route("/task/", methods=["GET"])
    @login_required
    def get_Task():

        taskId = request.args.get("taskId")

        try:
            logger.info("Fetching task: %s", taskId)
            task = app_db.get_item(taskId)
        except:
            logger.error("Error fetching task: %s", taskId)

        return render_template(
            "task.html", task=task, taskId=task.id, user=current_user
        )

    @writer_required
    @app.route("/update/", methods=["GET", "PUT"])
    @login_required
    def update_Task():
        """
        Updates a task to a given status
        """
        try:
            logger.info("Updating task %s", request.args.get("taskId"))
            app_db.update_task(
                id=request.args.get("taskId"),
                status=request.args.get("taskStatus"),
            )
        except:
            logger.error("Error updating task %s", request.args.get("taskId"))

        return redirect("/")

    @app.route("/login/callback", methods=["GET", "POST"])
    def authenticate():

        returned_github_code: str = request.args.get("code")
        client_id: str = os.environ.get("GH_CLIENTID")
        client_secret: str = os.environ.get("GH_ClIENTSECRET")

        fetch_token_headers: dict = {"Accept": "application/json"}

        fetch_token_params: dict = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": returned_github_code,
        }

        access_token_response = requests.post(
            "https://github.com/login/oauth/access_token",
            headers=fetch_token_headers,
            params=fetch_token_params,
        )
        access_token: str = access_token_response.json()["access_token"]

        fetch_user_headers: dict = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {access_token}",
        }

        github_user = requests.get(
            "https://api.github.com/user", headers=fetch_user_headers
        ).json()

        app_user = User(github_user["id"])
        app_user.role = user_db.get_user_role(userid=github_user["id"])
        logger.info("user ID is %s", app_user.id)
        logger.info("user is authenticated as a: %s", app_user.role)

        login_user(app_user)

        return redirect("/")

    return app
