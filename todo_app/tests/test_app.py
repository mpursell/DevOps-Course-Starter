from flask import request
import pytest
import os
import requests
from dotenv import load_dotenv, find_dotenv
from todo_app import app


class StubResponse:
    def __init__(self, name, id, idShort, idBoard, description, listName, taskUrl):

        self.name = name
        self.id = id
        self.idShort = idShort
        self.idBoard = idBoard
        self.description = (description,)
        self.listName = listName
        self.taskUrl = taskUrl


def mock_get_items() -> list[object]:

    return [
        StubResponse("name", "1", "123", "5678", "desc", "9999", "/tasks/?taskId=1")
    ]


def mock_add_item(title, description, listId) -> dict:

    mockItem = {"title": "title", "description": "description", "listId": "listID"}

    return mockItem


def mock_get_list_by_name(listName: str) -> str:

    return "listName"


def mock_get_item(taskId):

    return StubResponse("name", "1", "123", "5678", "desc", "9999", "/tasks/?taskId=1")


def mock_complete_item(taskid, listid):
    pass


@pytest.fixture
def client():

    # use the test config instead of the prod config
    file_path = find_dotenv(".env.test", usecwd=True)
    load_dotenv(file_path, override=True)

    # create the app
    test_app = app.create_app()

    # use the app to create a test_client that be used in the tests

    with test_app.test_client() as client:
        yield client


def test_index_page(monkeypatch, client):

    # arrange

    # Note - can't use directly imported modules like:
    # todo_app.data.trello_items.get_items

    monkeypatch.setattr("todo_app.app.get_items", mock_get_items)

    # act
    response = client.get("/")
    assert response.status == "200 OK"


def test_add_task(monkeypatch, client):

    # arrange

    monkeypatch.setattr("todo_app.app.get_list_by_name", mock_get_list_by_name)
    monkeypatch.setattr("todo_app.app.add_item", mock_add_item)

    # act
    response = client.post("/add")
    # check for a 302 since our app redirects us to / after the POST
    assert response.status == "302 FOUND"


def test_get_task(monkeypatch, client):

    # arrange

    monkeypatch.setattr("todo_app.app.get_item", mock_get_item)

    # act
    response = client.get("/task/")
    assert response.status == "200 OK"


def test_complete_task(monkeypatch, client):

    # arrange
    monkeypatch.setattr("todo_app.app.get_list_by_name", mock_get_list_by_name)
    monkeypatch.setattr("todo_app.app.complete_item", mock_complete_item)

    # have to mock get_items for the return to the index page.
    monkeypatch.setattr("todo_app.app.get_items", mock_get_items)

    # act
    response = client.get("/")
    assert response.status == "200 OK"
