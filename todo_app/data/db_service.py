from __future__ import annotations
from abc import ABC
import pymongo
from bson import ObjectId
from todo_app.data.card import Card


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

        listName = document["status"]
        name = document["title"]
        description = document["description"]
        id = str(document["_id"]).strip("'")
        idShort = id[:7]

        card = Card(
            name=name,
            listName=listName,
            description=description,
            id=id,
            idShort=idShort,
        )
        cardList.append(card)

    return cardList


def getItem(collection: pymongo.cursor.Cursor, taskId: str) -> Card:
    """
    Fetches the MongoDB document with the specified ID.

    Args:
        id: The ID of the item.
        collection: the MongoDB document collection object

    Returns:
        card: the card representation of the MongoDB document,
        or None if no items match the specified ID.
    """

    returnedDocument = collection.find_one({"_id": ObjectId(taskId)})

    try:

        id = returnedDocument["_id"]
        description = returnedDocument["description"]
        name = returnedDocument["title"]
        listName = returnedDocument["status"]
        idShort = str(id)[:7]

        card = Card(
            name=name,
            description=description,
            listName=listName,
            id=id,
            idShort=idShort,
        )

        return card

    # send exception to web server console
    except Exception as e:
        print(e)
        return None


def updateTask(
    collection: pymongo.cursor.Cursor, id, status: str
) -> pymongo.results.UpdateResult:

    update = collection.update_one(
        {"_id": ObjectId(id)}, {"$set": {"status": f"{status}"}}
    )

    return update


def addItem(
    document, collection: pymongo.cursor.Cursor
) -> pymongo.results.InsertOneResult:

    result = collection.insert_one(document)
    return result
