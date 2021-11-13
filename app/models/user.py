from pymongo import database, mongo_client
from werkzeug.security import generate_password_hash, check_password_hash
import secrets, json
from flask_pymongo import PyMongo
from app import app

mongo = PyMongo(app)


def find_user(username):
    return list(mongo.db.users.find({"username": username}))


class User:
    def __init__(self, username, password, token = None, avatar = 'default-avatar.jpg'):
        self.username = username
        self.password = password
        self.token = token
        self.avatar = avatar

    @classmethod
    def get_user(cls, username):
        user = find_user(username)
        return cls(user[0]['username'], user[0]['password'], user[0]['token'], user[0]['avatar'])

    def generate_session(self):
        self.token = secrets.token_hex(32)
        mongo.db.users.update({"username": self.username}, {"$set": {"token": self.token}})

    @classmethod
    def update_avatar(cls, username, avatarName,fileAvatar, currentAvatar):
        if currentAvatar != 'default-avatar.jpg':
            id= mongo.db.fs.files.find_one({"filename":currentAvatar}).get('_id')
            mongo.db.fs.files.remove({'_id': id})
            mongo.db.fs.chunks.remove({"files_id": id})
        mongo.save_file(avatarName,fileAvatar)

        mongo.db.users.update({"username": username}, {"$set": {"avatar": avatarName}})
       

    
    def check_session(self, token):
        if self.token == token:
            return True
        
    def check_username(self):
        database = find_user(self.username)
        if(len(database) > 0 ):
            return True
        else: 
            return False

    def delete_session(self):
        mongo.db.users.update({"username": self.username}, {"$set": {"token": None}})

    def update_password(self,newPassword):
        mongo.db.users.update({"username": self.username}, {"$set": {"token": None, "password": generate_password_hash(newPassword)}})

    def check_password(self):
        database = list(mongo.db.users.find({"username": self.username}))
        return check_password_hash(database[0]['password'], self.password)

    def write_data(self):
        mongo.db.users.insert({"username": self.username, "password": generate_password_hash(self.password) , "token": self.token, "avatar": self.avatar})


