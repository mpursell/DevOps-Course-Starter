from flask import Flask
from flask import render_template
from flask import request

from todo_app.flask_config import Config
from todo_app.data.trello_items import get_items
from todo_app.data.trello_items import add_item
from werkzeug.utils import redirect


app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():

    cardList = get_items()
    
        
    return render_template('index.html', cardList=cardList)    
    

@app.route('/add', methods = ['POST'])
def add_Task():
    
    # get the title data from the Add Task form field in index.html
    # add it to the list
    title = request.form.get('title')
    description = request.form.get('description')
    add_item(title, description, "61ade84dfee5c95cfb92ec05") # currently using To-Do List ID
    
    # send user back to starting app route
    return redirect('/')
    