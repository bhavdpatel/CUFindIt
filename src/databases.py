from flask_sqlalchemy import SQLAlchemy
import os
import datetime
import hashlib

db = SQLAlchemy()

class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    image_name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    id_found = db.relationship("user_found", back_populates="found_items")
    id_claimed = db.relationship("user_claimed", back_populates="claimed_items")
    date_found = db.Column(db.String, nullable=False)
    date_claimed = db.Column(db.String, nullable=True)

    def __init__(self, name, contact, image, date_found, location, id_found):
        self.name = name
        self.image_name = image
        self.location = location
        self.date_found = date_found
        self.user_found = id_found
        self.date_claimed = ""
        self.user_claimed = ""

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image_name": self.image_name,
            "location": self.location,
            "date_found": self.date_found,
            "date_claimed": self.date_claimed,
            "id_found": self.id_found,
            "id_claimed" : self.id_claimed
        }
    


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    netid = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password_digest = db.Column(db.String, nullable=False)
    claimed_items = db.relationship("claimed_items", back_populates="item")
    found_items = db.relationship("found_items", back_populates="item")

    session_token = db.Column(db.String, nullable=False, unique=True)
    session_expiration = db.Column(db.DateTime, nullable=False)
    update_token = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, email, password):
        self.email = email
        self.password_digest = bcrypt.hashpw(
            password.encode("utf8"), bcrypt.gensalt(rounds=13))
        self.renew_session()

    def _urlsafe_base_64(self):
        return hashlib.sha1(os.urandom(64)).hexdigest()


    def serialize(self):
        return {
            "id": self.id,
            "netid": self.netid,
            "email": self.email,
            "lost": [l.serialize() for l in self.lost],
            "found": [f.serialize() for f in self.found]
        }
    def subserialize(self):
        return {
            "id": self.id,
            "netid": self.netid,
            "email": self.email
        }
