from flask import Flask, abort
from flask import render_template
from flask import request
from flask_login import LoginManager, login_required, login_user, current_user

from todo_app.flask_config import Config
from todo_app.data.db_service import *
from todo_app.data.user import User, writer_required, reader_required
from todo_app.data.viewmodel import ViewModel

from werkzeug.utils import redirect

import logging
import os
import requests


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config())
    # logFile = os.environ.get('LOGFILE')
    logFile = ""

    if logFile:
        logging.basicConfig(
            filename=logFile,
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(name)s %(threadName)s: %(message)s",
        )

    # OAuth Login
    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        # logic to redirect to GH auth flow if unauthed

        client_id: str = os.environ.get("GH_CLIENTID")
        callback_uri = os.environ.get("CALLBACK_URI")

        return redirect(
            f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={callback_uri}"
        )

    @login_manager.user_loader
    def load_user(user_id: str) -> User:
        app_user = User(user_id)
        return app_user

    login_manager.init_app(app)

    # MongoDB connection and setup
    mongodbConnectionString = os.environ.get("MONGO_CONN_STRING")
    applicationDatabase = os.environ.get("MONGO_DB_NAME")

    todo = AppDatabase(mongodbConnectionString).connectDatabase(applicationDatabase)

    @app.route("/")
    @login_required
    def index():

        # MongoClient document finding
        collection = todo.todo
        documents = collection.find()
        #

        cardList: list = getItems(documents)
        cardList_view_model = ViewModel(cardList)

        return render_template("index.html", view_model=cardList_view_model)

    @writer_required
    @app.route("/add", methods=["POST"])
    @login_required
    def add_Task():

        title = request.form.get("title")
        description = request.form.get("description")
        listName = request.form.get("listName")

        document = {"title": title, "description": description, "status": listName}

        addItem(document, collection=todo.todo)

        return redirect("/")

    @reader_required
    @app.route("/task/", methods=["GET"])
    @login_required
    def get_Task():

        taskId = request.args.get("taskId")
        task = getItem(collection=todo.todo, taskId=taskId)

        return render_template("task.html", task=task, taskId=task.id)

    @writer_required
    @app.route("/update/", methods=["GET", "PUT"])
    @login_required
    def update_Task():
        """
        Updates a task to a given status
        """
        if current_user.role == 'writer':
            updateTask(
                collection=todo.todo,
                id=request.args.get("taskId"),
                status=request.args.get("taskStatus"),
            )
            return redirect("/")
        else:
            print(current_user.role)
            abort(403)
    

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

        app_user = User(id=github_user["id"])

        login_user(app_user)

        if app_user.check_role('reader') or app_user.check_role('writer'):
            current_user.role = app_user.role
            return redirect('/')
        else:
            abort(403)

    return app
