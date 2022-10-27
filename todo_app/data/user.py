from flask_login import UserMixin, current_user
from flask import abort
from functools import wraps



class User(UserMixin):

    role = ""

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated
    
    def __init__(self, user_id: str):
        self.id: str = user_id
        
        
    