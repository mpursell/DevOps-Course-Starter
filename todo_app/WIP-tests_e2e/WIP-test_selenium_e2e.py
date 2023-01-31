import os
from threading import Thread

import pytest
import requests
from dotenv import find_dotenv, load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from todo_app import app

pytest.skip(
    "Skipping... need to fix selenium geckodriver and binary location issues",
    allow_module_level=True,
)


def create_trello_board(api_key, api_token):

    # create the board with testboard as the name
    board_name = "testBoard"
    url = f"https://api.trello.com/1/boards/?name={board_name}"

    requestAuthPayload = {"key": {api_key}, "token": {api_token}}
    response = requests.post(url, params=requestAuthPayload)

    new_board = response.json()
    new_board
    # get the board's id and return it
    board_id = new_board["id"]

    return board_id


def delete_trello_board(api_key, api_token, board_id):

    url = f"https://api.trello.com/1/boards/{board_id}"

    requestAuthPayload = {"key": {api_key}, "token": {api_token}}
    response = requests.delete(url, params=requestAuthPayload)


@pytest.fixture(scope="module")
def app_with_temp_board():

    file_path = find_dotenv(".env")
    load_dotenv(file_path, override=True)

    api_key = os.environ.get("API_KEY")
    api_token = os.environ.get("API_TOKEN")
    board_id = create_trello_board(api_key, api_token)
    os.environ["TRELLO_BOARD_ID"] = board_id

    # construct the new app
    application = app.create_app()

    # start the app in it's own thread
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    # tear down
    thread.join(1)
    delete_trello_board(api_key, api_token, board_id)


@pytest.fixture(scope="module")
def driver():

    binaryLocation = os.environ.get("FIREFOX_BINARY_LOCATION")
    geckoLocation = os.environ.get("GECKODRIVER_LOCATION")

    s = Service(f"{geckoLocation}")
    options = Options()
    options.binary_location = f"{binaryLocation}"

    with webdriver.Firefox(service=s, options=options) as driver:
        yield driver


def test_task_journey(driver, app_with_temp_board):
    driver.get("http://localhost:5000/")

    assert driver.title == "To-Do App"
