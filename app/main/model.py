from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Favorite(db.Model):

    id = db.Column(db.Integer, primary_key = True)

    title = db.Column(db.String(500))

    url = db.Column(db.String, unique = True)
