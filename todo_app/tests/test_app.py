import pytest
import os
import requests
from dotenv import load_dotenv, find_dotenv
from todo_app import app


class StubResponse():
    
    def __init__(self, name, id, idShort, idBoard, description, listName, taskUrl):

        self.name = name
        self.id = id
        self.idShort = idShort
        self.idBoard = idBoard
        self.description = description,
        self.listName = listName
        self.taskUrl = taskUrl

def mock_get_items() -> list[object]:
    
    return [StubResponse('name','1','123','5678','desc','9999', '/tasks/?taskId=1')]

class MockViewModel():

    def __init__(self, cardList):
        self.cardList = cardList

@pytest.fixture
def client():

    # use the test config instead of the prod config
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # create the app
    test_app = app.create_app()

    # use the app to create a test_client that be used in the tests

    with test_app.test_client() as client:
        yield client


def test_index_page(monkeypatch, client):

    # arrange
    
    # I think this should be patching the get_items() function and the ViewModel object
    # but I'm still getting a JSON error when running the test, 
    # the test looks like it's still trying to use variables from the get_items() function
    # in trello_items.py
    cardList = mock_get_items()
    monkeypatch.setattr('todo_app.data.trello_items.get_items', mock_get_items())
    monkeypatch.setattr('todo_app.data.trello_items.ViewModel', MockViewModel(cardList))
    
    # act
    response = client.get('/')
    
    
    
    