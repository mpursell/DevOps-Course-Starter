from flask_login import UserMixin, current_user
from flask import abort


class User(UserMixin):
    
    users: list[dict] = [{"id": "2429045", "role": "reader"}]
    role: str = ''

    def __init__(self, id: str):
        self.id = id

    def check_role(self, desired_role:str):

        for user in self.users:

            # need the type casting to str here
            if str(user["id"]) == str(self.id):
                assigned_role: tuple = user["role"]
                if desired_role == user["role"]:
                    self.role = user['role']
                    return str(user['role'])
                else:
                    return False
            else:
                print("User id not recognised")
                return False


def writer_required(func):
    def wrapper():
        if current_user.role == "writer":
            return func()
        else:
            abort(403)

    return wrapper


def reader_required(func):
    def wrapper():

        if current_user.role == 'reader' or current_user.role == 'writer':
            return func()
        else:
            abort(403)

    # need to return the wrapper function
    return wrapper
