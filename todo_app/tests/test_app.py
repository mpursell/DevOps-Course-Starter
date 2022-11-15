from flask import request
import pytest
import os
import requests
from dotenv import load_dotenv, find_dotenv
import mongomock
from todo_app import app
from todo_app.data.viewmodel import ViewModel


class StubResponse:
    def __init__(self, name, id, idShort, idBoard, description, listName, taskUrl):

        self.name = name
        self.id = id
        self.idShort = idShort
        self.idBoard = idBoard
        self.description = (description,)
        self.listName = listName
        self.taskUrl = taskUrl


def mock_getItems(documentList) -> list[object]:

    return [
        StubResponse("name", "1", "123", "5678", "desc", "9999", "/tasks/?taskId=1")
    ]


def mock_addItem(document, collection) -> dict:

    mockItem = {"title": "title", "description": "description", "listId": "listID"}

    return mockItem


def mock_getItem(collection, taskId):

    return StubResponse("name", "1", "123", "5678", "desc", "9999", "/tasks/?taskId=1")


@pytest.fixture
def client():

    # use the test config instead of the prod config
    file_path = find_dotenv(".env.test", usecwd=True)
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(("fakemongo.com", 27017),)):
        # create the app
        test_app = app.create_app()

        # use the app to create a test_client that be used in the tests

        with test_app.test_client() as client:
            yield client


def test_index_page(monkeypatch, client):

    # arrange

    # Note - can't use directly imported modules like:
    # todo_app.data.trello_items.get_items

    # act
    response = client.get("/")
    assert response.status == "302 FOUND"


# def test_addItem(monkeypatch, client):

#     # arrange

#     monkeypatch.setattr("todo_app.app.addItem", mock_addItem)

#     # act
#     response = client.post("/add")
#     # check for a 302 since our app redirects us to / after the POST
#     assert response.status == "302 FOUND"


# def test_getItem(monkeypatch, client):

#     # arrange

#     monkeypatch.setattr("todo_app.app.getItem", mock_getItem)

#     # act
#     response = client.get("/task/")
#     assert response.status == "200 OK"


# # def test_updateTask(monkeypatch, client):

# #     # arrange

# #     monkeypatch.setattr("todo_app.app.updateTask", mock_updateTask)

# #     # have to mock get_items for the return to the index page.
# #     monkeypatch.setattr("todo_app.app.getItems", mock_getItems)

# #     # act
# #     response = client.get("/")
# #     assert response.status == "200 OK"


# # def test_ViewModel():
# #     """check to instantiate ViewModel and that items property is there"""
# #     # Act
# #     view = ViewModel(stub_view_model)

# #     # Assert
# #     assert view.items
