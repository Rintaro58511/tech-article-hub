from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


db = SQLAlchemy()

class Favorite(db.Model):

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    title = db.Column(db.String(500))

    url = db.Column(db.String, unique = True)

    regist_date = db.Column(db.DateTime, default = datetime.now)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    user_name = db.Column(db.String(50), nullable = False, unique = True)

    password = db.Column(db.String(255), nullable = False)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)