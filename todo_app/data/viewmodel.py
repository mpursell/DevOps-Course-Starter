class ViewModel:
    def __init__(self, items):
        self._items = items
        self.user_role = None

    @property
    def items(self):
        return self._items
