import requests
import os

apiKey = os.environ.get('API_KEY')
apiToken = os.environ.get('API_TOKEN')
boardID = os.environ.get('TRELLO_BOARD_ID')

"""
_DEFAULT_ITEMS = [
    { 'id': 1, 'status': 'Not Started', 'title': 'List saved todo items' },
    { 'id': 2, 'status': 'Not Started', 'title': 'Allow new items to be added' }
]
"""
class Task:
        
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

class List:

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value
        return self._name

class Api_request:

    def __init__(self):
        self.requestAuthPayload = {'key': apiKey, 'token': apiToken}

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
        return self._url


def get_items() -> list:
    """
    Fetches all cards on the given Trello board ID.

    Returns:
        list: JSON from the API parsed to a list of dictionaries.
    """

    apiCall = Api_request()
    apiCall.url = 'https://api.trello.com/1/boards/{}/cards?'.format(boardID)
    
    response = requests.get(apiCall.url, params=apiCall.requestAuthPayload)

    returnedList = response.json()

    taskList =[]
    for item in returnedList:
        task = Task()
        task.name = item['name']
        task.id = item['id']
        task.idShort = item['idShort']
        task.idBoard = item['idBoard']
        task.description = item['desc']
        task.listName = get_list(task.id)
        
        taskList.append(task)

    # return list of objects with required attributes
    return taskList

def get_list(cardID: str) -> str:
    """
    Gets the parent list for a given Trello card ID
    """
    apiCall = Api_request()
    apiCall.url = 'https://api.trello.com/1/cards/{}/list'.format(cardID)

    response = requests.get(apiCall.url, params=apiCall.requestAuthPayload)
    returnedDict = response.json()

    list = List()
    list.name = returnedDict['name']

    return list.name
    


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == str(id)), None)


def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    items = get_items()

    # Determine the ID for the item based on that of the previously added item
    id = items[-1]['id'] + 1 if items else 0

    item = { 'id': id, 'title': title, 'status': 'Not Started' }

    # Add the item to the list
    items.append(item)
    session['items'] = items

    return item


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    existing_items = get_items()
    updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]

    session['items'] = updated_items

    return item