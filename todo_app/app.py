from flask import Flask
from flask import render_template
from flask import request

from todo_app.flask_config import Config
from todo_app.data.trello_items import get_items, get_list_by_name
from todo_app.data.trello_items import add_item
from todo_app.data.trello_items import complete_item
from werkzeug.utils import redirect


app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():

    cardList = get_items()
     
    return render_template('index.html', cardList=cardList)    
    

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
    taskName = request.args.get('taskName')
    taskDescription = request.args.get('taskDescription')
    taskListName =  request.args.get('taskListName')

    return render_template('task.html', taskId=taskId, taskName=taskName, taskListName=taskListName, taskDescription=taskDescription)


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