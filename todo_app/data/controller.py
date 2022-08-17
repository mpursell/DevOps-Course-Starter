from __future__ import annotations
from abc import ABC
import requests
import os
import pymongo


mongodbConnectionString = os.environ.get("MONGO_CONN_STRING")
applicationDatabase = os.environ.get("MONGO_DB_NAME")

class DatabaseAbstract(ABC):
# interface to describe what our database class must implement
    
    def __init__(self, connectionString) -> None:
        pass

    @property
    def databaseName(self):
        return self._databaseName

    def connectDatabase(connectionString):
        pass

    def getCollections():
        pass
    
    def getItemsInCollection(collectionName):
        pass
    
    def addItemToCollection(itemName, targetCollectionName):
        pass

    def moveItemToCollection(itemName, targetCollectionName):
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

    # Get collections -> list of collections
    def getCollections(self) -> list:
        #database = self.connectDatabase()
        collectionsInDatabase = self.list_collection_names()
        return collectionsInDatabase


    # Get items in collection -> pymongo iterable cursor object
    def getItemsInCollection(self):
        database = self.connectDatabase().self_.collectionName
        collection = database[collection]
        
        documentList = collection.find()
        return documentList
            

    # Add item to collection -> item in new collection
    def addItemToCollection(self, toDoItem, targetCollectionName):
        database = self.connectDatabase(self._connectionString).self_.collectionName
        existingCollectionsList = self.getCollections()

        # check if the collection name exists already because if it doesn't
        # mongoDB will just create a new collection, and we don't want to create
        # collections outside of the already specified collections
        if targetCollectionName in existingCollectionsList:
            collection = database[targetCollectionName]
            collection.insert_one(toDoItem)
            
            newItem = collection.find_one(toDoItem)
            return newItem
        else:
            return "collection not in the existing list of collections"
        

    # Move item to collection -> item in new collection

    