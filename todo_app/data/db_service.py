from __future__ import annotations
from abc import ABC
from codecs import getreader
import pymongo
from bson import ObjectId
from todo_app.data.card import Card


class DatabaseAbstract(ABC):
    # interface to describe what the database class must implement

    def __init__(self, connectionString) -> None:
        pass

    @property
    def databaseName(self):
        return self._databaseName

    def connectDatabase(connectionString):
        pass


class AppDatabase(DatabaseAbstract):

    def connectDatabase(self, databaseName):

        client = pymongo.MongoClient(self._connectionString)
        applicationDB = client[databaseName]
        return applicationDB

    def get_items(self) -> list[object]:

        """
        Gets a list of documents

        Args:
            documentList: a pymongo Cursor from the database

        Returns:
            cardList: a list of Card objects with attributes added.
        """
        list_of_cards = []

        for document in self.documents:

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
            list_of_cards.append(card)

        return list_of_cards

    def get_item(self, taskId: str) -> Card:
        """
        Fetches the MongoDB document with the specified ID.

        Args:
            id: The ID of the item.
            collection: the MongoDB document collection object

        Returns:
            card: the card representation of the MongoDB document,
            or None if no items match the specified ID.
        """

        returnedDocument = self.collection.find_one({"_id": ObjectId(taskId)})

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

    def update_task(self, id, status: str) -> pymongo.results.UpdateResult:

        update = self.collection.update_one(
            {"_id": ObjectId(id)}, {"$set": {"status": f"{status}"}}
        )

        return update

    def add_item(self, document) -> pymongo.results.InsertOneResult:

        result = self.collection.insert_one(document)
        return result

    def get_user_role(self, userid):
        
        user = self.collection.find_one({'userid': userid})
        if user == None:
            new_user: pymongo.results.InsertOneResult = self.collection.insert_one({"userid": userid, "role": "reader"})
            return new_user
        else:
            return user['role']

    def __init__(self, connectionString, database_name, collection_name) -> None:

        self._connectionString = connectionString
        self.collection_name = collection_name
        self.database_name = database_name
        self.card_list = None

        app_db = self.connectDatabase(database_name)

        # after connecting to the db, decide whether we want to 
        # instaniate an AppDatabase object with the application collection
        # or the users collection. 
        if collection_name == 'todo':
            self.collection: pymongo.collection.Collection = app_db.todo
        elif collection_name == 'auth_users':
            self.collection: pymongo.collection.Collection = app_db.auth_users

        self.documents: pymongo.cursor.Cursor = self.collection.find()
  