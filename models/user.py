import pdb
from flask_login import UserMixin


# Fake users
USERS_DB = {}


class User(UserMixin):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'sub':
                setattr(self, 'id', value)
            else:
                setattr(self, key, value)

    @staticmethod
    def get(user_id):
        return USERS_DB.get(user_id)

    @staticmethod
    def create(**kwargs):
        user_id = kwargs.get('sub')
        USERS_DB[user_id] = User(**kwargs)


    def locate(self):
        return {
            'email': 'johndoe@mail.com',
            'zoneinfo': 'Central Daylight Time',
            'updated_at': '2021-09-26',
            'locale': 'Nashville, TN'
        }
