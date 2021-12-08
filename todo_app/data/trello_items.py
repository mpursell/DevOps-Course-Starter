import requests
import os

apiKey = os.environ.get('API_KEY')
apiToken = os.environ.get('API_TOKEN')
boardID = os.environ.get('TRELLO_BOARD_ID')


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

    def make_call(self, url):
        url = self._url

        return requests.get(self.url, params=self.requestAuthPayload)

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

    cardList =[]
    for item in returnedList:
        card = Card()
        card.name = item['name']
        card.id = item['id']
        card.idShort = item['idShort']
        card.idBoard = item['idBoard']
        card.description = item['desc']
        card.listName = get_list(card.id)
        
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
    apiCall = Api_request()
    apiCall.url = 'https://api.trello.com/1/cards/{}/list'.format(cardID)

    response = requests.get(apiCall.url, params=apiCall.requestAuthPayload)
    returnedDict = response.json()

    list = List()
    list.name = returnedDict['name']

    return list.name
    
def get_list_by_name(listName: str) -> str:

    apiCall = Api_request()
    apiCall.url = 'https://api.trello.com/1/boards/{}/lists'.format(boardID)

    response = requests.get(apiCall.url, params=apiCall.requestAuthPayload)
    returnedList = response.json()

    for trelloList in returnedList:
        if trelloList['name'] == listName:
            return trelloList['id']
        



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

    title = title.replace(" ", "%20")
    description = description.replace(" ", "%20")

    apiCall = Api_request()
    apiCall.url = 'https://api.trello.com/1/cards/?idList={}&name={}&desc={}'.format(idList, title, description)

    response = requests.post(apiCall.url, params=apiCall.requestAuthPayload)
    item = response.json()

    return item


def complete_item(id:str) -> dict:

    """
    Allows a task to be marked as "Done", or moved to the "Done" Trello list
    
    Args: id: the id of the item to be moved
    """

    idList = get_list_by_name('Done')

    apiCall = Api_request()
    apiCall.url = 'https://api.trello.com/1/cards/{}}?idList={}'.format(id, idList)
    response = requests.get(apiCall.url, params=apiCall.requestAuthPayload)
    #apiCall.make_call('https://api.trello.com/1/cards/{}}?idList={}'.format(id, idList))

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