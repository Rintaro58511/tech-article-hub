from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Favorite(db.Model):

    id = db.Column(db.Integer, primary_key = True)

    title = db.Column(db.String(500))

    url = db.Column(db.String, unique = True)

    regist_date = db.Column(db.DateTime, default = datetime.now)
