from __future__ import annotations
from abc import ABC
import requests
import os
import pymongo


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