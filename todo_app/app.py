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


        categoryNameList: list = ['To-Do', 'Doing', 'Done']
        filteredCollectionList: list = []
        
        for categoryName in categoryNameList:
            filteredCollectionList.append(todo.list_collection_names(filter={'name': f'{categoryName}'})[0])
        
        collection_view_model = ViewModel(filteredCollectionList)
        

        return render_template("index.html", view_model=collection_view_model)

    @app.route("/add", methods=["POST"])
    def add_Task():

        title = request.form.get("title")
        description = request.form.get("description")
        listName = request.form.get("listName")

        document = {
            "title": title,
            "description": description,
        }

        collection = todo[listName]
        collection.insert_one(document)

        # listId = get_list_by_name(list)
        # add_item(title, description, listId)

        return redirect("/")

    @app.route("/task/", methods=["GET"])
    def get_Task():

        taskId = request.args.get("taskId")
        task = get_item(taskId)

        return render_template("task.html", task=task, taskId=task.id)

    @app.route("/update/", methods=["GET", "PUT"])
    def update_Task():
        """
        Not required for module 2 task, just added for practice
        """

        updateTaskListName = request.args.get("taskStatus")
        listId = get_list_by_name(updateTaskListName)

        taskId = request.args.get("taskId")

        complete_item(taskId, listId)

        return redirect("/")

    return app
