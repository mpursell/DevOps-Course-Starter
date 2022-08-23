from __future__ import annotations
from abc import ABC
import requests
import os
import pymongo
from bson import ObjectId


class DatabaseAbstract(ABC):
    # interface to describe what our database class must implement

    def __init__(self, connectionString) -> None:
        pass

    @property
    def databaseName(self):
        return self._databaseName

    def connectDatabase(connectionString):
        pass


class AppDatabase(DatabaseAbstract):
    def __init__(self, connectionString) -> None:

        self._connectionString = connectionString

    @property
    def databaseName(self):
        return self._databaseName

    @databaseName.setter
    def databaseName(self, value):
        self._databaseName = value
        return self._databaseName

    @property
    def collectionName(self):
        return self._collectionName

    @collectionName.setter
    def collectionName(self, value):
        self._collectionName = value
        return self._collectionName

    # Connect to database
    def connectDatabase(self, databaseName):
        client = pymongo.MongoClient(self._connectionString)
        applicationDB = client[databaseName]
        return applicationDB


class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items


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


def getItems(documentList: pymongo.cursor.Cursor) -> list[object]:
    
    """
    Gets a list of documents as a 
    
    Args:
        documentList: a pymongo Cursor from the database 
    
    Returns: 
        cardList: a list of Card objects with attributes added. 
    """
    cardList = []

    for document in documentList:
        card = Card()
        card.listName = document["status"]
        card.name = document["title"]
        card.description = document["description"]
        card.id = str(document["_id"]).strip("'")
        card.idShort = card.id[:5]
        cardList.append(card)

    return cardList

def get_item(collection, id: str) -> object:
    """
    Fetches the MongoDB document with the specified ID.

    Args:
        id: The ID of the item.
        collection: the MongoDB document collection object

    Returns:
        card: the card representation of the MongoDB document, 
        or None if no items match the specified ID.
    """

    returnedDocument = collection.find_one({"_id": ObjectId(id)})

    try:
        card = Card()
        card.id = returnedDocument["_id"]
        card.description = returnedDocument["description"]
        card.name = returnedDocument["title"]
        card.listName = returnedDocument['status']

        return card
    except:
        return None