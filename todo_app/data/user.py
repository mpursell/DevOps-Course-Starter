from flask_login import UserMixin, current_user
from flask import abort


class User(UserMixin):
    def __init__(self, id: str):
        self.id = id
        self.users: list[dict] = [{"id": "2429045", "role": "writer"}]
        self.role = None


    def check_role(self, desired_role: str):

        for user in self.users:

            # need the type casting to str here
            if str(user["id"]) == str(self.id):
                if desired_role == user["role"]:
                    self.role = user['role']
                    #current_user.role.append(user['role'])
                    return str(user['role'])
                else:
                    return False
            else:
                return False


def writer_required(func):
    def wrapper():
        id = current_user.id

        for user in users:

            # need the type casting to str here
            if str(user["id"]) == str(id):
                assigned_role: tuple = user["role"]
                if "writer" in user["role"]:
                    return func()
                else:
                    print(f'Assigned role: {assigned_role} does not match "writer"')
                    abort(403)

    return wrapper


def reader_required(func):
    def wrapper():
        id = current_user.id

        for user in users:

            # need the type casting to str here
            if str(user["id"]) == str(id):
                assigned_role: tuple = user["role"]
                if "reader" in user["role"]:
                    # run and return the value of the passed-in function
                    return func()
                else:
                    print(f'Assigned role: {assigned_role} does not match "reader"')
                    abort(403)

    # need to return the wrapper function
    return wrapper
