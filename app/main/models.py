from app import db
from app.auth.models import User


user_lab_tables = db.Table('user_labs',
                           db.Column('user_id', db.ForeignKey('user.id'), primary_key=True),
                           db.Column('lab_id', db.ForeignKey('labs.id'), primary_key=True)
                           )


class Laboratory(db.Model):
    __tablename__ = 'labs'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(), nullable=False)
    desc = db.Column('description', db.Text())
    created_at = db.Column('created_at', db.DateTime(timezone=True))
    active = db.Column('active', db.Boolean(), default=True)
    creator_id = db.Column('creator_id', db.ForeignKey('user.id'))
    creator = db.relationship(User, backref=db.backref('user', lazy=True))
    members = db.relationship(User,
                              secondary=user_lab_tables,
                              lazy='subquery',
                              backref=db.backref('labs', lazy=True))
