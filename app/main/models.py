from app import db
from app.auth.models import User


class Laboratory(db.Model):
    __tablename__ = 'labs'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(), nullable=False)
    desc = db.Column('description', db.Text())
    created_at = db.Column('created_at', db.DateTime(timezone=True))
    active = db.Column('active', db.Boolean(), default=True)
    creator_id = db.Column('creator_id', db.ForeignKey('user.id'))
    creator = db.relationship(User, backref=db.backref('user', lazy=True))

    @property
    def num_pending_members(self):
        return len([m for m in self.lab_members if not m.approved])

    @property
    def num_approved_members(self):
        return len([m for m in self.lab_members if m.approved])

    def __str__(self):
        return self.name


class UserLabAffil(db.Model):
    __tablename__ = 'user_lab_affils'
    user_id = db.Column('user_id', db.ForeignKey('user.id'), primary_key=True)
    lab_id = db.Column('lab_id', db.ForeignKey('labs.id'), primary_key=True)
    joined_at = db.Column('joined_at', db.DateTime(timezone=True))
    approved = db.Column('approved', db.Boolean(), default=False)
    user = db.relationship(User, backref=db.backref('lab_affils', lazy=True))
    lab = db.relationship(Laboratory, backref=db.backref('lab_members'))

