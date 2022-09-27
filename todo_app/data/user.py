from flask_login import UserMixin, current_user
from flask import abort


class User(UserMixin):


    def __init__(self, id: str):
        self.id = id


users: list[dict] = [
            {'id':'2429045', 
            'role': ('writer', 'reader')}
                ] 

        
def check_role(id: str, desired_role: str):

    for user in users:

        # need the type casting to str here
        if str(user['id']) == str(id):
            assigned_role: tuple = user['role']
            if desired_role in user['role']:
                return str(desired_role)
            else:
                print(f'Assigned role: {assigned_role} and desired role {desired_role} do not match')
                abort(403)
        else:
            print('User id not recognised')
            abort(403)
            #return "not authorised"



def writer_required(func):
    def wrapper():
        id = current_user.id

        for user in users:

            # need the type casting to str here
            if str(user['id']) == str(id):
                assigned_role: tuple = user['role']
                if 'writer' in user['role']:
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
            if str(user['id']) == str(id):
                assigned_role: tuple = user['role']
                if 'reader' in user['role']:
                    # run and return the value of the passed-in function
                    return func()
                else:
                    print(f'Assigned role: {assigned_role} does not match "reader"')
                    abort(403)   

    # need to return the wrapper function       
    return wrapper

