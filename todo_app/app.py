from flask import Flask
from flask import render_template
from flask import request

from todo_app.flask_config import Config
from todo_app.data.trello_items import *
from todo_app.data.controller import *
from werkzeug.utils import redirect

import logging
import os


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

    mongodbConnectionString = os.environ.get("MONGO_CONN_STRING")
    applicationDatabase = os.environ.get("MONGO_DB_NAME")

    todo = AppDatabase(mongodbConnectionString).connectDatabase(applicationDatabase)

    @app.route("/")
    def index():

        # MongoClient document finding
        collection = todo.todo
        documents = collection.find()
        #

        cardList = []

        for document in documents:
            card = Card()
            card.listName = document["status"]
            card.name = document["title"]
            card.description = document["description"]
            card.id = str(document["_id"]).strip("'")
            card.idShort = card.id[:5]
            cardList.append(card)

        cardList_view_model = ViewModel(cardList)

        return render_template("index.html", view_model=cardList_view_model)

    @app.route("/add", methods=["POST"])
    def add_Task():

        title = request.form.get("title")
        description = request.form.get("description")
        listName = request.form.get("listName")

        document = {"title": title, "description": description, "status": listName}

        collection = todo.todo
        collection.insert_one(document)

        return redirect("/")

    @app.route("/task/", methods=["GET"])
    def get_Task():

        documentCollection = todo.todo
        taskId = request.args.get("taskId")
        task = getItem(documentCollection, taskId)

        return render_template("task.html", task=task, taskId=task.id)

    @app.route("/update/", methods=["GET", "PUT"])
    def update_Task():
        """
        Not required for module 2 task, just added for practice
        """
        collection = todo.todo
        newStatus = request.args.get("taskStatus")
        taskId = request.args.get("taskId")

        updateTask(collection, taskId, newStatus)

        return redirect("/")

    return app
