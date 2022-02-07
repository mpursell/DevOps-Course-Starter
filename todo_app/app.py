from flask import Flask
from flask import render_template
from flask import request

from todo_app.flask_config import Config
from todo_app.data.trello_items import *
from werkzeug.utils import redirect

import logging
import os                    

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config())
    #logFile = os.environ.get('LOGFILE')
    logFile = ''

    if logFile:
        logging.basicConfig(filename=logFile, level=logging.INFO,
                            format='%(asctime)s %(levelname)s %(name)s %(threadName)s: %(message)s')

    @app.route('/')
    def index():

        cardList = get_items()
        card_view_model = ViewModel(cardList)
        
        return render_template('index.html', view_model=card_view_model)    

    @app.route('/add', methods = ['POST'])
    def add_Task():
        
        title = request.form.get('title')
        description = request.form.get('description')
        list = request.form.get('listName')
        listId = get_list_by_name(list)
        
        add_item(title, description, listId) 
        
        return redirect('/')

    @app.route('/task/', methods =['GET'])
    def get_Task():

        taskId = request.args.get('taskId')
        task = get_item(taskId)
        

        return render_template('task.html', task=task)

    @app.route('/update/', methods=['GET','PUT'])
    def complete_Task():
        
        updateTaskListName = request.args.get('taskStatus')
        listId = get_list_by_name(updateTaskListName)

        taskId = request.args.get('taskId')
    
        complete_item(taskId, listId)

        return redirect('/')

    @app.route('/update/', methods=['GET','PUT'])
    def update_Task():
        """
        Not required for module 2 task, just added for practice
        """
        
        updateTaskListName = request.args.get('taskStatus')
        listId = get_list_by_name(updateTaskListName)

        taskId = request.args.get('taskId')
    
        complete_item(taskId, listId)

        return redirect('/')

    return app
