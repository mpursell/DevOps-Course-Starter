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
