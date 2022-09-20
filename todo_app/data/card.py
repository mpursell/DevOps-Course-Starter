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
