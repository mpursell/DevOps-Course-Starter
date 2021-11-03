from flask import Flask
from flask import render_template

from todo_app.flask_config import Config
from todo_app.data.session_items import get_items
from todo_app.data.session_items import add_item


app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():

    taskList = get_items()
        
    return render_template('index.html', taskList=taskList)    
    

@app.route('/add', methods = ['POST'])
def add_Task():
    
    newItem = add_item('')