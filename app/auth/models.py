from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from app import db


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    email = db.Column('email', db.String(128), nullable=False, unique=True)
    firstname = db.Column('firstname', db.String())
    lastname = db.Column('lastname', db.String())
    license_id = db.Column('license_id', db.String())
    pwdhash = db.Column('pwdhash', db.String())

    def __init__(self, email, password):
        self.email = email
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)