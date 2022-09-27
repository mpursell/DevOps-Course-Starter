from flask_login import UserMixin, current_user
from flask import abort


class User(UserMixin):


    def __init__(self, id: str):
        self.id = id
        
      

        
def check_role(id: str, desired_role: str):

    print(current_user.id)

    users: list[dict] = [
            {'id':'2429045', 
            'role': ('writer', 'reader')}
                ]

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



