"""module contains ORM classes definitions for User and Result tables"""


from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    digits = db.relationship('Result', backref='user', lazy=True)


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.PickleType)
    prediction = db.Column(db.Integer)
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
