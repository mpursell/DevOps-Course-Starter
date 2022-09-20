from __future__ import annotations
from abc import ABC
import requests
import os
import pymongo
from bson import ObjectId
from todo_app.data.card import Card
from todo_app.data.viewmodel import ViewModel


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

    # Connect to database
    def connectDatabase(self, databaseName):
        client = pymongo.MongoClient(self._connectionString)
        applicationDB = client[databaseName]
        return applicationDB


def getItems(documentList: pymongo.cursor.Cursor) -> list[object]:

    """
    Gets a list of documents

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
        card.idShort = card.id[:7]
        cardList.append(card)

    return cardList


def getItem(collection: pymongo.cursor.Cursor, id: str) -> object:
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
        card.listName = returnedDocument["status"]

        return card

    except:
        return None


def updateTask(
    collection: pymongo.cursor.Cursor, id, status: str
) -> pymongo.results.UpdateResult:

    update = collection.update_one(
        {"_id": ObjectId(id)}, {"$set": {"status": f"{status}"}}
    )

    return update

def addItem(document, collection: pymongo.cursor.Cursor) -> pymongo.results.InsertOneResult:
     result = collection.insert_one(document)
     return result