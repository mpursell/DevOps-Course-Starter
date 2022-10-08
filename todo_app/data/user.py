from flask_login import UserMixin, current_user
from flask import abort
from functools import wraps


class User(UserMixin):


    def __init__(self):
        self.id = None
        self.role = None
