from flask_sqlalchemy import SQLAlchemy
import os
import datetime
import bcrypt
import hashlib

db = SQLAlchemy()

class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    image_name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=True)
    user_found = db.relationship("user_found", back_populates="found_items", nullable=False)
    user_claimed = db.relationship("user_claimed", back_populates="claimed_items", nullable=True)
    date_found = db.Column(db.String, nullable=False)
    date_claimed = db.Column(db.String, nullable=True)

     def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "image_name": self.contact,
            "location": self.location,
            "date_found": self.date_found,
            "date_claimed": self.date_claimed
            "user": self.user_id
        }


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    netid = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password_digest = db.Column(db.String, nullable=False)
    claimed_items = db.relationship("claimed_items", back_populates="item")
    found_items = db.relationship("found_items", back_populates="item")

    # Session information
    session_token = db.Column(db.String, nullable=False, unique=True)
    session_expiration = db.Column(db.DateTime, nullable=False)
    update_token = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, email, password):
        self.email = email
        self.password_digest = bcrypt.hashpw(
            password.encode("utf8"), bcrypt.gensalt(rounds=13))
        self.renew_session()

    # Used to randomly generate session/update tokens
    def _urlsafe_base_64(self):
        return hashlib.sha1(os.urandom(64)).hexdigest()

    # Generates new tokens, and resets expiration time
    def renew_session(self):
        self.session_token = self._urlsafe_base_64()
        self.session_expiration = datetime.datetime.now() + datetime.timedelta(days=7)
        self.update_token = self._urlsafe_base_64()

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf8"), self.password_digest)

    # Checks if session token is valid and hasn't expired
    def verify_session_token(self, session_token):
        return session_token == self.session_token and datetime.datetime.now() < self.session_expiration

    def serialize(self):
        return {
            "id": self.id,
            "netid": self.netid,
            "email": self.email,
            # "lost": [l.serialize() for l in self.lost],
            # "found": [f.serialize() for f in self.found]
        }
