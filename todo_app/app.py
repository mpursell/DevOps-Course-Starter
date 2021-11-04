from flask import Flask
from flask import render_template
from flask import request

from todo_app.flask_config import Config
from todo_app.data.session_items import get_items
from todo_app.data.session_items import add_item
from werkzeug.utils import redirect


app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():

    taskList = get_items()
        
    return render_template('index.html', taskList=taskList)    
    

@app.route('/add', methods = ['POST'])
def add_Task():
    
    # get the title data from the Add Task form field in index.html
    # add it to the list
    newTask = request.form.get('newTask')
    add_item(newTask)

    # get all the list items again, including the new item
    taskList = get_items()

    # send user back to starting app route
    return redirect('/')
    