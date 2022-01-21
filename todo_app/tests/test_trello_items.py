import string
import pytest
import requests
from todo_app.data.trello_items import *

class StubResponse():
    def json(self):
        return {'name':'foobar',
                'id': '999',
                'desc':'describe me'}

class StubResponseList():
    """class to return a list of dicts rather than a dict"""
    def json(self):
        return [
            {'name':'foobar',
             'id':'123',
             'idShort':'2',
             'idBoard':'board',
             'desc':'describe me'}
            ]

    def get_list(self):
        return {'name':'foobar'}

class StubViewModel():
    def items(self):
        return [{'listName':'Doing'}]



def stub(url, params): 
    #return an object of type StubResponse
    return StubResponse()

def stub_add_item(url, params, data):
    return StubResponse()

def stub_list(url, params):
    return StubResponseList()

def stub_view_model():
    return [{'listName':'Doing'}]


def test_get_items(monkeypatch):
    
    #Arrange
    monkeypatch.setattr(requests, 'get', stub_list)

    # mock the function call to get_list() from inside get_items()
    # then monkeypatch the mock_get_list over the actual get_list()
    def mock_get_list(cardId):
        return '9999'
    monkeypatch.setattr('todo_app.data.trello_items.get_list', mock_get_list)
    
    #Act
    items = get_items()

    #Assert
    assert isinstance(items, list)

def test_get_item(monkeypatch):

    #Arrange
    id = '123'
    monkeypatch.setattr(requests, 'get', stub)

    #Act
    item = get_item(id)

    #Assert
    assert isinstance(item, object)

def test_get_list(monkeypatch):

    #Arrange
    cardID = "1"

    # mock api request
    monkeypatch.setattr(requests, 'get', stub)

    #Act
    listName = get_list(cardID)

    #Assert 
    assert listName == "foobar"

def test_add_item(monkeypatch):

    #Arrange
    title = "title"
    description = "description"
    idList = "12345"
    monkeypatch.setattr(requests, 'post', stub_add_item)
    
    #Act
    addedItem = add_item(title, description, idList)

    #Assert
    assert isinstance(addedItem, dict)
    assert addedItem['name'] == 'foobar'

def test_get_list_by_name(monkeypatch):

    #Arrange
    listName = 'foobar'
    monkeypatch.setattr(requests, 'get', stub_list)

    #Act
    listByName = get_list_by_name(listName)

    #Assert
    assert listByName == '123'
    assert isinstance(listByName, str)    

def test_ViewModel():
    """check to instantiate ViewModel and that items property is there"""
    #Act
    view = ViewModel(stub_view_model)

    #Assert
    assert view.items 
    
