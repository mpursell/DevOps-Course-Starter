from __future__ import annotations
from abc import ABC
import requests
import os


apiKey = os.environ.get("API_KEY")
apiToken = os.environ.get("API_TOKEN")
boardID = os.environ.get("TRELLO_BOARD_ID")

class Card:
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value
        return self._name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value: str):
        self._id = value
        return self._id

    @property
    def idShort(self):
        return self._idShort

    @idShort.setter
    def idShort(self, value: str):
        self._idShort = value
        return self._idShort

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value
        if not self._description:
            self._description = "No description available"
        return self._description

    @property
    def idBoard(self):
        return self._idBoard

    @idBoard.setter
    def idBoard(self, value: str):
        self._idBoard = value
        return self._idBoard

    @property
    def listName(self):
        return self._listName

    @listName.setter
    def listName(self, value: str):
        self._listName = value
        if not self._listName:
            self._listName = "No Name Found"
        return self._listName

    @property
    def taskUrl(self):
        return self._taskUrl

    @taskUrl.setter
    def taskUrl(self, value):
        self._taskUrl = value
        return self._taskUrl


class List:
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value
        return self._name


class Api_handler:
    def __init__(self):
        # self.requestAuthPayload = {'key': apiKey, 'token': apiToken}
        self.requestAuthPayload = {
            "key": os.environ.get("API_KEY"),
            "token": os.environ.get("API_TOKEN"),
        }

        @property
        def url(self):
            return self._url

        @url.setter
        def url(self, value):
            self._url = value
            return self._url

        @property
        def body(self):
            return self._body

        @body.setter
        def body(self, value):
            self._body = value
            return self._body

    def make_get_call(self):
        return requests.get(self.url, params=self.requestAuthPayload)

    def make_post_call_with_body_data(self):
        return requests.post(self.url, params=self.requestAuthPayload, data=self.body)


class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items


def get_items() -> list[object]:
    """
    Fetches all cards on the given Trello board ID.

    Returns:
        list: JSON from the API parsed to a list of dictionaries.
    """

    apiCall = Api_handler()
    apiCall.url = "https://api.trello.com/1/boards/{}/cards?".format(boardID)
    response = apiCall.make_get_call()

    returnedList = response.json()

    cardList = []
    for item in returnedList:
        card = Card()
        card.name = item["name"]
        card.id = item["id"]
        card.idShort = item["idShort"]
        card.idBoard = item["idBoard"]
        card.description = item["desc"]
        card.listName = get_list(card.id)
        card.taskUrl = f"/tasks/?taskId={card.id}"

        cardList.append(card)

    # return list of objects with required attributes
    return cardList


def get_list(cardID: str) -> str:
    """
    Gets the parent list for a given Trello card ID
    Trello cards are tasks for our purposes: Board -> List -> Cards/tasks

    Args:
        cardID: The ID of the card / task
    """
    apiCall = Api_handler()
    apiCall.url = "https://api.trello.com/1/cards/{}/list".format(cardID)

    response = apiCall.make_get_call()
    returnedDict = response.json()

    list = List()
    list.name = returnedDict["name"]

    return list.name


def get_list_by_name(listName: str) -> str:

    apiCall = Api_handler()
    apiCall.url = "https://api.trello.com/1/boards/{}/lists".format(boardID)

    response = apiCall.make_get_call()
    returnedList = response.json()

    for trelloList in returnedList:
        if trelloList["name"] == listName:
            return trelloList["id"]


def get_item(id: str) -> object:
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """

    apiCall = Api_handler()
    apiCall.url = "https://api.trello.com/1/cards/{}".format(id)

    response = apiCall.make_get_call()
    returnedDict = response.json()

    card = Card()
    card.id = returnedDict["id"]
    card.description = returnedDict["desc"]
    card.name = returnedDict["name"]
    card.listName = get_list(card.id)

    return card


def add_item(title: str, description: str, idList: str) -> dict:
    """
    Adds a new card with the specified title and description to the Trello board.

    Args:
        title: The title of the item.
        description: The task description.
        listName: The id of the list you want to add the card to

    Returns:
        item: The saved item.
    """

    apiCall = Api_handler()
    apiCall.url = "https://api.trello.com/1/cards/?idList={}&name={}&desc={}".format(
        idList, title, description
    )

    apiCall.body = {"title": title, "description": description}

    response = apiCall.make_post_call_with_body_data()
    item = response.json()

    return item


def complete_item(id: str, idList: str) -> None:

    """
    Allows a task to be moved to a given Trello list

    Args: id: the id of the item to be moved
          idList : the id of the list to move the item to
    """

    apiCall = Api_handler()
    # ID ISN'T BEING PASSED IN CORRECTLY FROM APP.PY
    apiCall.url = f"https://api.trello.com/1/cards/{id}?idList={idList}"
    response = requests.put(apiCall.url, params=apiCall.requestAuthPayload)

    return response
