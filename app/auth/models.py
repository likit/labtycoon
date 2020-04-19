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

    def __init__(self, firstname, lastname, email, password, license_id):
        self.firstname = firstname
        self.lastname = lastname
        self.license_id = license_id
        self.email = email
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    @property
    def fullname(self):
        return '{} {}'.format(self.firstname, self.lastname)

    def __str__(self):
        return self.fullname

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def is_affiliated_with(self, lab_id):
        return lab_id in [affil.lab.id for affil in self.lab_affils]
