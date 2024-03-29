# models.py

from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class FilmList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Date())
    title = db.Column(db.String(251), unique=True)
    description = db.Column(db.String(9999))
    film_list = db.Column(db.String(999))
